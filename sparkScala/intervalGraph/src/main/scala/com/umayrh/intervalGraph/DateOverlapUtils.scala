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
  *
  * TODO: should crossJoin be replaced with broadcast variable?
  * TODO: worry about timezone a little bit more for correctness
  */
object DateOverlapUtils {

  /**
    * @param df - a data frame containing a date columns
    * @param inputCols - a pair of date columns, representing the start and end dates
    *                  (inclusive) of a range. Dates are assumed to be in the same timezone,
    *                  non-null, and the range non-negative (i.e. start date <= end date)
    * @param outputCols - names of output columns appended to the data frame. Each output
    *                   column represents the normalized epoch time of the corresponding
    *                   input column. Normalization is done by offseting to the minimum
    *                   date across input columns.
    * @return the input data frame with new columns containing unix timestamp (in days)
    */
  def mapDateToInt(df: DataFrame,
                   inputCols: (String, String),
                   outputCols: (String, String)): DataFrame = {
    val minDateCol = "minDate"
    var outDf: DataFrame = df;

    val input = Seq(inputCols._1, inputCols._2)
    val output = Seq(outputCols._1, outputCols._2)

    // Find minimum date to, later, normalize the input's range
    // e.g. subtract the min value from all
    val minDatesDf = df.agg(min(inputCols._1).as(inputCols._1),
                            min(inputCols._2).as(inputCols._2))
    val minDateDf = minDatesDf
      .withColumn(minDateCol,
                  when(col(inputCols._1).gt(col(inputCols._2)),
                       col(inputCols._2))
                    .otherwise(col(inputCols._1)))
      .drop(inputCols._1)
      .drop(inputCols._2)

    outDf = outDf.crossJoin(broadcast(minDateDf))

    // normalize the input date, and round to a day
    (0 until input.size).foreach({ idx =>
      outDf =
        outDf.withColumn(
          output(idx),
          ((unix_timestamp(outDf(input(idx))) - unix_timestamp(
            outDf(minDateCol))) / DateTimeConstants.SECONDS_PER_DAY)
            .cast(LongType))
    })
    outDf.drop(minDateCol)
  }

  /**
    * @param df a dataframe containing bitmaps
    * @param dfCol name of the 'df' column representing the start of an range
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
    val intersectUdf = getIntersectUdf()

    joinedDf
      .withColumn(outputCol, intersectUdf(joinedDf(dfCol), joinedDf(indexCol)))
      .drop(aggCol)
      .drop(indexCol)
  }

  /**
    * @return a [[UserDefinedFunction]] that takes two serialized [[RoaringBitmap]]s
    *         and a serialized int array as input. The first bitmap has a single
    *         range of bits sets while the second represents the union of all such
    *         bitmaps. Thus, the intersection is always non-empty, and we can use
    *         the index of the first set bit to find the range map's group id.
    */
  private def getIntersectUdf(): UserDefinedFunction = {
    val intersectFn =
      (rangeStart: Long, index: Array[Byte]) => {
        val indexMap = toIntArray(index)
        // TODO: sure you want to cast long as int?
        indexMap(RoaringBitmapUDAF.toStartIndex(rangeStart).intValue())
      }
    udf(intersectFn)
  }

  /**
    * @param aggDf an aggregated dataframe that represents bitwise-OR across df bitmaps
    * @param col name of bitmap col in 'aggDf'
    * @param df a dataframe containing bitmaps
    * @param indexCol name of the output column
    * @return a dataframe with a column named 'indexCol' appended to it. The new column
    *         contains an Array[Int] of the same size as the number of rows in 'df'.
    * TODO: maybe compress this array using e.g. https://github.com/lemire/JavaFastPFOR
    * While the compression ratio may be high since the index array has incrementing
    * integers, decompression may be slow. Maybe delta encoding?
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
      .drop(col)
  }

  /**
    * @return a [[UserDefinedFunction]] that takes a serialized [[RoaringBitmap]]
    *         and an int as inputs. It assigns a unique id to sub-sequences of
    *         consecutive 1's, and stores that id in a new array at the same
    *         position as a set bit in the bitmap. This array is the output of
    *         the function.
    * TODO: optimize the size of the index array by mapping log_2(data size)
    * to an appropriate integral type.
    */
  private def getIndexUdf(): UserDefinedFunction = {
    val indexFn = (bits: Array[Byte], size: Int) => {
      val bitmap = RoaringBitmapSerde.deserialize(bits)
      val indexMap = new Array[Int](bitmap.last() + 1)
      var groupCnt = 1
      var prevIdx = -1
      // TODO: convert to single abstract method
      val consumerFn: IntConsumer = new IntConsumer() {
        override def accept(idx: Int): Unit = {
          // increment group id iff there're unset bits between
          // current and previous indices, and previous index
          // has been reset once (i.e. after the first iteration)
          if (prevIdx >= 0 && idx > prevIdx + 1) {
            groupCnt += 1
          }
          indexMap(idx) = groupCnt
          prevIdx = idx
        }
      }
      bitmap.forEach(consumerFn)
      toByteArray(indexMap)
    }

    udf(indexFn)
  }

  /**
    * @param arr a byte array
    * @return a view of the byte array as an int array
    */
  private def toIntArray(arr: Array[Byte]): Array[Int] = {
    val intArray = new Array[Int](arr.length / 4)
    // TODO: can this copy be avoided?
    ByteBuffer.wrap(arr).asIntBuffer().get(intArray)
    intArray
  }

  /**
    * @param arr an int array
    * @return a view of the int array as a byte array
    */
  private def toByteArray(arr: Array[Int]): Array[Byte] = {
    val buf = ByteBuffer.allocate(arr.length * 4)
    buf.asIntBuffer().put(arr)
    buf.array()
  }
}
