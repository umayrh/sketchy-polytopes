package com.umayrh.intervalGraph

import java.nio.ByteBuffer

import com.google.common.base.Preconditions
import org.apache.commons.lang.StringUtils
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.{broadcast, lit, sum, udf, unix_timestamp}
import org.apache.spark.sql.types.LongType
import org.joda.time.DateTimeConstants
import org.roaringbitmap.RoaringBitmap
import org.roaringbitmap.IntConsumer

/**
  * Utilities for [[DateOverlap]]
  */
object DateOverlapUtils {

  /**
    * @param df - a data frame containing a date column
    * @param inputCols - names of date columns
    * @param outputCols - names of output columns appended to the data frame
    * @return the input data frame with new columns containing unix timestamp (in days)
    */
  def mapDateToInt(df: DataFrame,
                   inputCols: Seq[String],
                   outputCols: Seq[String]): DataFrame = {
    Preconditions.checkArgument(inputCols.size == outputCols.size)
    var outDf: DataFrame = df;
    // TODO: normalize the input's range e.g. subtract the min value from all
    // this requires an aggregation and a broadcast-join

    (0 to inputCols.size).foreach({ idx =>
      outDf = outDf.withColumn(
        outputCols(idx),
        (unix_timestamp(outDf(inputCols(idx))) / DateTimeConstants.SECONDS_PER_DAY)
          .cast(LongType))
    // TODO: each date must be mapped to two bit positions
    })
    outDf
  }

  /**
    * Add a new column to given dataframe. Each row corresponds to a bitmap
    * that has the bits indexed by the given range set.
    * @param df table
    * @param inputStart input range start column name
    * @param inputEnd input range end column name
    * @param outputCol output column name
    * @return a [[DataFrame]] with a new column with given name
    */
  def mapIntRangeToBitSet(df: DataFrame,
                          inputStart: String,
                          inputEnd: String,
                          outputCol: String): DataFrame = {
    val serializeBitmap = (start: Long, end: Long) => {
      val map = new RoaringBitmap()
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
    Preconditions.checkArgument(dfCol.equals(aggCol))

    // map aggDf to a bitmap of indices.
    val indexCol = "TMP_index"
    val indexDf = makeIndexDf(aggDf, aggCol, df, indexCol)

    val joinedDf = df.crossJoin(broadcast(indexDf))

    val intersect =
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

    val intersectUdf = udf(intersect)

    joinedDf
      .withColumn(
        outputCol,
        intersectUdf(joinedDf(dfCol), joinedDf(aggCol), joinedDf(indexCol)))
      .drop(indexCol)
  }

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
  private def makeIndexDf(aggDf: DataFrame,
                          col: String,
                          df: DataFrame,
                          indexCol: String): DataFrame = {
    // taking pain to avoid Dataframe.count()
    val sizeCol = "TMP_size"
    val joinedDf = aggDf.crossJoin(
      broadcast(
        df.withColumn(sizeCol, lit(1))
          .agg(sum(sizeCol).as(sizeCol))))

    // TODO: optimize the size of the index array by mapping log_2(data size)
    // to an appropriate integral type. Is it strange that
    val dfToIndex = (bits: Array[Byte], size: Int) => {
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

    val dfToIndexUdf = udf(dfToIndex)

    joinedDf
      .withColumn(indexCol, dfToIndexUdf(joinedDf(col), joinedDf(sizeCol)))
      .drop(sizeCol)
  }
}
