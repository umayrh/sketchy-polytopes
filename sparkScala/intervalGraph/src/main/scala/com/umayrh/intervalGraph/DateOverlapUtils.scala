package com.umayrh.intervalGraph

import java.nio.ByteBuffer

import com.google.common.base.Preconditions
import org.apache.commons.lang.StringUtils
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.LongType
import org.joda.time.DateTimeConstants
import org.roaringbitmap.{IntConsumer, RoaringBitmap}

/**
  * Utilities for [[DateOverlap]]
  */
object DateOverlapUtils {

  /**
    * @param df - a data frame containing a date columns
    * @param inputCols - a pair of date columns, representing the start and end dates
    *                  (inclusive) of a range
    * @param outputCols - names of output columns appended to the data frame. Each output
    *                   column represents the normalized epoch time of the corresponding
    *                   input column. Normalization is done by offseting to the minimum
    *                   date across input columns.
    * @return the input data frame with new columns containing unix timestamp (in days)
    */
  def mapDateToInt(df: DataFrame,
                   inputCols: (String, String),
                   outputCols: (String, String)): DataFrame = {
    var outDf: DataFrame = df;
    // TODO: normalize the input's range e.g. subtract the min value from all
    // this requires an aggregation and a broadcast-join

    val input = Seq(inputCols._1, inputCols._2)
    val output = Seq(outputCols._1, outputCols._2)

    //var minDf = df
    //val minDates = input.map(inCol => )

    (0 to input.size).foreach({ idx =>
      outDf = outDf.withColumn(
        output(idx),
        (unix_timestamp(outDf(input(idx))) / DateTimeConstants.SECONDS_PER_DAY)
          .cast(LongType))
    })
    outDf
  }

  /**
    * Add a new column to given dataframe. Each row corresponds to a bitmap
    * that has the bits indexed by the given range set.
    * @param df table
    * @param inputStart input range start column name
    * @param inputEnd input range end column name
    * @param outputCol name of the column containing bitmap for given range
    * @return a [[DataFrame]] with a new column with given name
    */
  def mapIntRangeToBitmap(df: DataFrame,
                          inputStart: String,
                          inputEnd: String,
                          outputCol: String): DataFrame = {
    val serializeBitmap = (start: Long, end: Long) => {
      val map = new RoaringBitmap()
      // TODO: each date must be mapped to two bit positions
      map.add(start, end)
      // possibly use org.apache.spark.sql.Encoders.kryo[RoaringBitmap]
      RoaringBitmapSerde.serialize(map)
    }
    val serializeBitmapUdf = udf(serializeBitmap)
    df.withColumn(outputCol, serializeBitmapUdf(df(inputStart), df(inputEnd)))
  }

  /**
    * @param df a dataframe containing bitmaps
    * @param dfCol name of the 'df' column containing bitmaps
    * @param aggDf an aggregated dataframe that represents bitwise-OR across df(dfCol) bitmaps
    * @param aggCol name of the 'aggDf' column containing a single bitmap. This must be different
    *               from dfCol
    * @return 'df' with a new column that represents the group id of bitmaps. Bitmaps have the
    *         same group id iff they overlap
    * @throws IllegalArgumentException if input column names are blank or equal
    */
  def intersectBitmaps(df: DataFrame,
                       dfCol: String,
                       aggDf: DataFrame,
                       aggCol: String,
                       outputCol: String): DataFrame = {
    Preconditions.checkArgument(StringUtils.isNotBlank(dfCol))
    Preconditions.checkArgument(StringUtils.isNotBlank(aggCol))
    Preconditions.checkArgument(!dfCol.equals(aggCol))

    // map aggDf to a bitmap of indices.
    val indexCol = "TMP_index"
    val indexDf = makeIndexDf(aggDf, aggCol, df, indexCol)
    val joinedDf = df.crossJoin(broadcast(indexDf))
    val intersectUdf = getInterectUdf()

    joinedDf
      .withColumn(
        outputCol,
        intersectUdf(joinedDf(dfCol), joinedDf(aggCol), joinedDf(indexCol)))
      .drop(aggCol)
      .drop(indexCol)
  }

  /**
    * @return a [[UserDefinedFunction]] that takes two serialized [[RoaringBitmap]]s
    *         and a serialized int array as input. if the two bitmaps have a non-
    *         empty intersection, then it return the index of the first bit in the
    *         intersection. Otherwise, returns 0.
    */
  private def getInterectUdf(): UserDefinedFunction = {
    val intersectFn =
      (range: Array[Byte], or: Array[Byte], index: Array[Byte]) => {
        val bitmap = RoaringBitmapSerde.deserialize(range)
        val orBitmap = RoaringBitmapSerde.deserialize(or)
        val indexMap = toIntArray(index)
        val andMap = RoaringBitmap.and(bitmap, orBitmap)
        if (andMap.getCardinality() > 0) {
          indexMap(andMap.first())
        } else {
          0
        }
      }
    udf(intersectFn)
  }

  /**
    * @param arr a byte array
    * @return the byte array as an int array
    */
  private def toIntArray(arr: Array[Byte]): Array[Int] = {
    val buf = ByteBuffer.allocate(arr.length)
    buf.put(arr)
    buf.flip()
    buf.asIntBuffer().array()
  }

  /**
    * @param aggDf an aggregated dataframe that represents bitwise-OR across df bitmaps
    * @param col name of bitmap col in 'aggDf'
    * @param df a dataframe containing bitmaps
    * @param indexCol name of the output column
    * @return 'aggDf' with a new column named 'indexCol' appended to it. The new column
    *         contains an Array[Int] of the same size as the number of rows in 'df'.
    */
  def makeIndexDf(aggDf: DataFrame,
                  col: String,
                  df: DataFrame,
                  indexCol: String): DataFrame = {
    // taking pain to avoid Dataframe.count()
    val sizeCol = "TMP_size"
    val joinedDf = aggDf.crossJoin(
      broadcast(
        df.withColumn(sizeCol, lit(1))
          .agg(sum(sizeCol).as(sizeCol))))
    val indexUdf = getIndexUdf()

    joinedDf
      .withColumn(indexCol, indexUdf(joinedDf(col), joinedDf(sizeCol)))
      .drop(sizeCol)
  }

  /**
    * @return a [[UserDefinedFunction]] that takes a serialized [[RoaringBitmap]]
    *         and an int as inputs. It assigns a unique id to subsequences of
    *         consecutive 1's, and stores that id in a new array at the same
    *         position as a set bit in the bitmap. This array is the output of
    *         the function.
    * TODO: optimize the size of the index array by mapping log_2(data size)
    * to an appropriate integral type. Is it strange that
    */
  private def getIndexUdf(): UserDefinedFunction = {
    val indexFn = (bits: Array[Byte], size: Int) => {
      val indexMap = new Array[Int](size)
      val bitmap = RoaringBitmapSerde.deserialize(bits)
      var groupCnt = 1
      var prevIdx = -1
      val consumerFn: IntConsumer = new IntConsumer() {
        override def accept(idx: Int): Unit = {
          // increment group id iff there're unset bits between
          // current and previous indices, and previous index
          // has been reset once (i.e. not on the first iteration)
          if (prevIdx >= 0 && idx > prevIdx + 1) {
            groupCnt += 1
          }
          indexMap(idx) = groupCnt
          prevIdx = idx
        }
      }
      bitmap.forEach(consumerFn)
      indexMap
    }

    udf(indexFn)
  }
}
