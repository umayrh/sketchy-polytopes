package com.umayrh.intervalGraph

import org.apache.spark.sql.DataFrame

/**
  * Utilities for grouping observations that overlap in time
  */
object DateOverlap {

  /**
    *
    */
  def groupByOverlap(df: DataFrame, bitmapCol: String): DataFrame = {
    // aggregate all bitmaps

    df
  }
}
