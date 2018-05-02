package com.umayrh.intervalGraph

import com.google.common.base.Preconditions
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.roaringbitmap.RoaringBitmap

/**
  * Utilities for grouping observations that overlap in time
  */
object DateOverlap {
  implicit val ENCODER = org.apache.spark.sql.Encoders.kryo[RoaringBitmap]

  private val SECONDS_IN_A_DAY: Long = 86400

  /**
    *
    */
  def groupByOverlap(df: DataFrame, bitmapCol: String): DataFrame = {
    // aggregate all bitmaps

    df
  }

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
        (unix_timestamp(outDf(inputCols(idx))) / SECONDS_IN_A_DAY)
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
      RoaringBitmapSerde.serialize(map)
    }
    val serializeBitmapUdf = udf(serializeBitmap)
    df.withColumn(outputCol, serializeBitmapUdf(df(inputStart), df(inputEnd)))
  }
}
