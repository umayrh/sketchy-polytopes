package com.umayrh.intervalGraph

import org.apache.spark.sql.DataFrame
import org.roaringbitmap.RoaringBitmap
import org.scalatest.Matchers

/**
  * Common test utilities
  */
object TestUtils extends Matchers {

  /**
    * @return a sequence of tuples with the first element implying
    *         a randomly generated (0-Int.Max) range start index, and the second
    *         implying a sequence length capped maxLen (default: 1000)
    */
  def getRandRanges(maxLen: Long = 1000): List[(Long, Long)] = {
    List
      .fill(1000)(Int.MaxValue)
      .map(k => (scala.util.Random.nextInt(k), scala.util.Random.nextInt(1000)))
      .map(k => (Int.int2long(k._1), Int.int2long(k._2)))
  }

  /**
    * @return a [[RoaringBitmap]] with bits in the inclusive range (start, end) set to 1
    */
  def makeBitmap(start: Long, end: Long): RoaringBitmap = {
    val bitmap = new RoaringBitmap()
    bitmap.add(start, end)
    bitmap
  }

  /**
    * Assumes that given dataframes have only one column containing [[RoaringBitmap]].
    * Asserts that the bitmaps in the given dataframes are equal.
    * @param expectedDf expected table
    * @param actualDf actual table
    */
  def assertDataFrameEquals(expectedDf: DataFrame,
                            actualDf: DataFrame): Unit = {
    // Alas, DataFrameSuiteBaseLike's assertDataFrameEquals has issues
    actualDf.count() should be(expectedDf.count())
    val expected = expectedDf
      .collect()
      .map(r => RoaringBitmapSerde.deserialize(r.getAs[Array[Byte]](0)))
    val actual = actualDf
      .collect()
      .map(r => RoaringBitmapSerde.deserialize(r.getAs[Array[Byte]](0)))
    val result = Range(0, expected.length).map(idx =>
      bitmapsEqual(expected(idx), actual(idx)))
    result.foreach(k => assert(k._1, k._2))
  }

  /**
    * @param map1 a [[RoaringBitmap]]
    * @param map2 another [[RoaringBitmap]]
    * @return (true, "") if the bitmaps are equals. Otherwise, the second element in the
    *         tuple is an error message describing bitmap ranges.
    */
  def bitmapsEqual(map1: RoaringBitmap,
                   map2: RoaringBitmap): (Boolean, String) = {
    if (map1.equals(map2)) {
      (true, "")
    } else {
      (false, s"($map1.first(), $map1.last()) != ($map2.first(), $map2.last())")
    }
  }
}
