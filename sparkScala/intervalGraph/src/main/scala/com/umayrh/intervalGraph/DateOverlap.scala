package com.umayrh.intervalGraph

import com.google.common.base.Preconditions
import com.umayrh.intervalGraph.DateOverlapUtils._
import org.apache.spark.sql.DataFrame

/**
  * Utilities for grouping observations that overlap in time
  *
  * See also:
  * - Bitmaps vs sorted lists
  * [[https://lemire.me/blog/2012/10/23/when-is-a-bitmap-faster-than-an-integer-list/]]
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
    Preconditions.checkArgument(df.columns.contains(inputCols._1))
    Preconditions.checkArgument(df.columns.contains(inputCols._2))

    val epochStartCol = "TMP_start"
    val epochEndCol = "TMP_end"
    val intDf = mapDateToInt(df, inputCols, (epochStartCol, epochEndCol))

    val aggCol = "TMP_agg_bitmap"
    val bitmapUdaf = new RoaringBitmapUDAF(epochStartCol, epochEndCol)
    val aggDf =
      intDf.agg(bitmapUdaf(intDf(epochStartCol), intDf(epochEndCol)).as(aggCol))

    val result =
      intersectBitmaps(intDf, epochStartCol, aggDf, aggCol, outputCol)

    result
      .drop(epochStartCol)
      .drop(epochEndCol)
      .drop(aggCol)
  }
}
