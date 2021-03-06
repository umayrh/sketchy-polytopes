package com.umayrh.intervalGraph

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import com.umayrh.intervalGraph.RoaringBitmapUDAF.{toEndIndex, toStartIndex}
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.rand
import org.roaringbitmap.RoaringBitmap
import org.scalatest.featurespec.AnyFeatureSpec
import org.scalatest.matchers.should._
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.GivenWhenThen

import scala.util.Random

/**
  * Tests [[RoaringBitmapUDAF]]
  */
object RoaringBitmapUDAFTest {
  val MAX_ITER   = 50
  val BITMAP_COL = "bitmaps"
  val START_COL  = "range_start"
  val END_COL    = "range_end"
  val OUTPUT_COL = "agg_bitmap"
}

class RoaringBitmapUDAFTest
    extends AnyFeatureSpec
    with GivenWhenThen
    with Matchers
    with GeneratorDrivenPropertyChecks
    with SharedSparkContext
    with DataFrameSuiteBase {
  import RoaringBitmapUDAFTest._

  Feature(
    "Spark User-defined Aggregation Function for performing an OR op on columns describing a range") {
    val orFn = new RoaringBitmapUDAF(START_COL, END_COL)

    Scenario("The UDAF is commutative ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val df         = toDf(inputData())
      val expectedDf = df.agg(orFn(df(START_COL), df(END_COL)))

      When("bitmaps rows in a dataframe are shuffled")
      val shuffledDf = df.orderBy(rand())
      val actualDf =
        shuffledDf.agg(orFn(shuffledDf(START_COL), shuffledDf(END_COL)))

      Then("the result of UDAF doesn't change")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }

    Scenario("The UDAF is partially associative") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val data       = inputData()
      val df         = toDf(data)
      val expectedDf = df.agg(orFn(df(START_COL), df(END_COL)).as(OUTPUT_COL))

      When("The results of randomly ordered UDAF invocations are aggregated using OR")
      val splitSize = Random.nextInt(data.size)
      val splitData = data.grouped(splitSize)
      val splitDf   = splitData.map(toDf)
      val bitmapsDf =
        splitDf.map(df => df.agg(orFn(df(START_COL), df(END_COL)).as(OUTPUT_COL)))
      val unionedDf = Random.shuffle(bitmapsDf).reduce(_ union _)
      val actual = unionedDf
        .collect()
        .map(r => RoaringBitmapSerde.deserialize(r.getAs(0)))
        .reduce(RoaringBitmap.or)

      Then("the result of UDAF doesn't change")
      TestUtils.assertDataFrameEquals(expectedDf, toBitmapDf(List(actual)))
    }

    Scenario("The UDAF obeys De Morgan's law: A OR B = ~(~A AND ~B) ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val data = inputData()

      // since the UDAF does this scaling implicitly, test data needs explicit scaling
      val scaled = data.map(k => (toStartIndex(k._1), toEndIndex(k._1, k._2)))
      val bitmaps =
        scaled.map(range => TestUtils.makeBitmap(range._1, range._2))
      val maxCardinality = bitmaps.map(b => b.last()).reduce(Math.max)
      val flipped =
        bitmaps.map(b => RoaringBitmap.flip(b, 0L, maxCardinality + 1))
      val conjugated = flipped.reduce(RoaringBitmap.and)
      val negated    = RoaringBitmap.flip(conjugated, 0L, maxCardinality + 1)
      val expectedDf = toBitmapDf(List(negated))

      When("UDAF is invoked on a set of bitmaps")
      val df       = toDf(data)
      val actualDf = df.agg(orFn(df(START_COL), df(END_COL)).as(BITMAP_COL))

      Then("the result is the same as that of bitmaps flipped, conjugated, and flipped again")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }
  }

  /**
    * @return list of with a randomly generated ranges
    */
  private def inputData(): List[(Long, Long)] = {
    TestUtils.getRandRanges()
  }

  /**
    * @param ranges list of ranges
    * @return a dataframe out of the given list
    */
  private def toDf(ranges: List[(Long, Long)]): DataFrame = {
    import sqlContext.implicits._
    sc.parallelize(ranges).toDF(START_COL, END_COL)
  }

  /**
    * @param bitmaps list of [[RoaringBitmap]]s
    * @return a dataframe out of the given list
    */
  private def toBitmapDf(bitmaps: List[RoaringBitmap]): DataFrame = {
    TestUtils.bitmapsToDf(sc, sqlContext)(bitmaps, BITMAP_COL)
  }
}
