package com.umayrh.intervalGraph

import org.apache.spark.sql.DataFrame
import DateOverlapUtils._

/**
  * Utilities for grouping observations that overlap in time
  */
object DateOverlap {

  /**
    * Assigns an id to each row in the given dataframe such that iff
    * the date ranges in any two rows overlap, then they have the same id.
    * This function assumes but doesn't enforce valid inputs.
    *
    * @param df a dataframe
    * @param inputCols a pair of date columns, representing the start
    *                  and end dates (inclusive) of a range. A range is
    *                  considered valid if it is bounded but non-empty i.e.
    *                  start date < end date.
    * @param outputCol name of the id column
    * @return 'df' with a new column that represents the group id of bitmaps.
    *         Bitmaps have the same group id iff they overlap
    */
  def groupByOverlap(df: DataFrame,
                     inputCols: (String, String),
                     outputCol: String): DataFrame = {
    val epochStartCol = "TMP_start"
    val epochEndCol = "TMP_end"
    val intDf = mapDateToInt(df, inputCols, (epochStartCol, epochEndCol))

    val bitmapCol = "TMP_bitmap"
    val bitmapDf =
      mapIntRangeToBitmap(intDf, epochEndCol, epochEndCol, bitmapCol)

    val aggCol = "TMP_agg_bitmap"
    val bitmapUdaf = new RoaringBitmapUDAF(aggCol)
    val aggDf = bitmapDf.agg(bitmapUdaf(bitmapDf(bitmapCol)))

    val result = intersectBitmaps(df, bitmapCol, aggDf, aggCol, outputCol)

    result
      .drop(epochStartCol)
      .drop(epochEndCol)
      .drop(bitmapCol)
  }
}
