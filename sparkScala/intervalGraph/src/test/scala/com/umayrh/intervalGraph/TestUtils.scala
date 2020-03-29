package com.umayrh.intervalGraph

import java.sql.Date

import com.google.common.base.Preconditions
import org.apache.spark.SparkContext
import org.apache.spark.sql.{DataFrame, SQLContext}
import org.roaringbitmap.RoaringBitmap
import org.scalatest.matchers.should._

import scala.util.Random

/**
  * Common test utilities
  */
object TestUtils extends Matchers {

  /**
    * @param maxLen maximum length across generated ranges. Must be positive.
    * @return a sequence of tuples with the randomly generated range start
    *         and range end pair. The range is guaranteed to be non-empty,
    *         and bounded, and should be treated as inclusive.
    */
  def getRandRanges(maxLen: Int = 1000): List[(Long, Long)] = {
    Preconditions.checkArgument(maxLen > 0)
    List
      .fill(maxLen)(10 * maxLen)
      .map(k => (Random.nextInt(k), Random.nextInt(maxLen) + 1))
      .map(k => (Int.int2long(k._1), Int.int2long(k._1 + k._2 - 1)))
  }

  /**
    * @param start start of range (must be >= 0)
    * @param end end of range (must be >= start, and < Long.MaxValue)
    * @return a [[RoaringBitmap]] with bits in the inclusive range (start, end) set to 1
    */
  def makeBitmap(start: Long, end: Long): RoaringBitmap = {
    Preconditions.checkArgument(start >= 0 && start <= end && end < Long.MaxValue)
    val bitmap = new RoaringBitmap()
    bitmap.add(start, end + 1)
    bitmap
  }

  /**
    * @param sqlContext [[SQLContext]], for importing implicits
    * @param bitmaps list of bitmaps to be dataframe-d
    * @param colName name of column containing bitmaps
    * @return a dataframe of serialized [[RoaringBitmap]]s out of the given list
    */
  def bitmapsToDf(sc: SparkContext, sqlContext: SQLContext)(bitmaps: List[RoaringBitmap],
                                                            colName: String): DataFrame = {
    val serializedBitmaps = bitmaps.map(RoaringBitmapSerde.serialize)
    // implicits, yuck...
    import sqlContext.implicits._
    sc.parallelize(serializedBitmaps).toDF(colName)
  }

  /**
    * Convert a list of date ranges to a dataframe
    * @param dates list of date ranges
    * @param startCol name of start date column (default: "s")
    * @param endCol name of end date column (default: "t")
    * @return a dataframe with two date columns
    */
  def datesToDf(sc: SparkContext, sqlContext: SQLContext)(dates: List[(Date, Date)],
                                                          startCol: String = "s",
                                                          endCol: String = "t"): DataFrame = {
    // implicits, yuck...
    import sqlContext.implicits._
    sc.parallelize(dates).toDF(startCol, endCol)
  }

  /**
    * Assumes that given dataframes have only one column containing [[RoaringBitmap]].
    * Asserts that the bitmaps in the given dataframes are equal.
    * @param expectedDf expected table
    * @param actualDf actual table
    */
  def assertDataFrameEquals(expectedDf: DataFrame, actualDf: DataFrame): Unit = {
    // Alas, DataFrameSuiteBaseLike's assertDataFrameEquals has issues
    actualDf.count() should be(expectedDf.count())
    val expected = expectedDf
      .collect()
      .map(r => RoaringBitmapSerde.deserialize(r.getAs[Array[Byte]](0)))
    val actual = actualDf
      .collect()
      .map(r => RoaringBitmapSerde.deserialize(r.getAs[Array[Byte]](0)))
    val result = Range(0, expected.length).map(idx => bitmapsEqual(expected(idx), actual(idx)))
    result.foreach(k => assert(k._1, k._2))
  }

  /**
    * @param map1 a [[RoaringBitmap]]
    * @param map2 another [[RoaringBitmap]]
    * @return (true, "") if the bitmaps are equals. Otherwise, the second element in the
    *         tuple is an error message describing bitmap ranges.
    */
  def bitmapsEqual(map1: RoaringBitmap, map2: RoaringBitmap): (Boolean, String) = {
    if (map1.equals(map2)) {
      (true, "")
    } else {
      (false, bitmapToString(map1) + " != " + bitmapToString(map2))
    }
  }

  def bitmapToString(map: RoaringBitmap): String = {
    val card = map.getCardinality
    if (card == 0) {
      "EMPTY"
    } else {
      (map.first(), map.last()) + ": " + card
    }
  }
}
