package com.umayrh.intervalGraph

import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import org.roaringbitmap.RoaringBitmap

/**
  * Utilities for grouping observations that overlap in time
  */
object DateOverlap {
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
    * @param inputCol - name of date column
    * @param outputCol - name of column appended to the data frame
    * @return the input data frame with a new column containing unix timestamp (in days)
    */
  private def mapDateToInt(df: DataFrame,
                           inputCol: String,
                           outputCol: String): DataFrame = {
    df.withColumn(
      outputCol,
      (unix_timestamp(df(inputCol)) / SECONDS_IN_A_DAY).cast(LongType))
    // TODO: normalize the input's range e.g. subtract the min value from all
    // this requires an aggregation and a broadcast-join
  }

  /**
    *
    */
  private def mapIntRangeToBitSet(df: DataFrame,
                                  inputStart: String,
                                  inputEnd: String,
                                  outputCol: String): DataFrame = {
    val bitmap = (start: Long, end: Long) => {
      val map = new RoaringBitmap()
      map.add(start, end)
      map
    }
    val bitmapUdf = udf(bitmap)
    df.withColumn(outputCol, bitmapUdf(df(inputStart), df(inputEnd)))
  }
}
