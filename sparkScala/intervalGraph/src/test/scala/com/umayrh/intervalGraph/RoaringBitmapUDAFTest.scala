package com.umayrh.intervalGraph

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.rand
import org.roaringbitmap.RoaringBitmap
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.{FeatureSpec, GivenWhenThen, Matchers}

import scala.util.Random

/**
  * Tests [[RoaringBitmapOrUDAF]]
  */
object RoaringBitmapUDAFTest {
  val MAX_ITER = 50
  val BITMAP_COL = "bitmaps"
  val START_COL = "range_start"
  val END_COL = "range_end"
  val OUTPUT_COL = "agg_bitmap"
}

class RoaringBitmapUDAFTest
    extends FeatureSpec
    with GivenWhenThen
    with GeneratorDrivenPropertyChecks
    with Matchers
    with SharedSparkContext
    with DataFrameSuiteBase {
  import RoaringBitmapUDAFTest._

  Feature(
    "Spark User-defined Aggregation Function for performing an OR op on columns describing a range") {
    val orFn = new RoaringBitmapUDAF(START_COL, END_COL)

    Scenario("The UDAF is commutative ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val df = toDf(inputData())
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
      val data = inputData()
      val df = toDf(data)
      val expectedDf = df.agg(orFn(df(START_COL), df(END_COL)).as(OUTPUT_COL))

      When(
        "The results of randomly ordered UDAF invocations are aggregated using OR")
      val splitSize = Random.nextInt(data.size)
      val splitData = data.grouped(splitSize)
      val splitDf = splitData.map(toDf)
      val bitmapsDf =
        splitDf.map(df =>
          df.agg(orFn(df(START_COL), df(END_COL)).as(OUTPUT_COL)))
      val unionedDf = Random.shuffle(bitmapsDf).reduce(_.union(_))
      val actual = unionedDf
        .collect()
        .map(r => RoaringBitmapSerde.deserialize(r.getAs(0)))
        .reduce(RoaringBitmap.or)

      Then("the result of UDAF doesn't change")
      TestUtils.assertDataFrameEquals(expectedDf, toBitmapDf(List(actual)))
    }

    Scenario("TODO: The UDAF is idempotent") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      When("invoking the UDAF N times (N >= 1) on the same bitmap")
      Then("doesn't change the bitmap")
    }

    Scenario("The UDAF obeys De Morgan's law: A OR B = ~A AND ~B ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val data = inputData()
      val bitmaps = data.map(range => TestUtils.makeBitmap(range._1, range._2))
      val flipped = bitmaps.map(b => RoaringBitmap.andNot(b, b))
      val conjugated = flipped.reduce(RoaringBitmap.and)
      val expectedDf = toBitmapDf(List(conjugated))

      When("UDAF is invoked on a set of bitmaps")
      val df = toDf(data)
      val actualDf = df.agg(orFn(df(START_COL), df(END_COL)).as(BITMAP_COL))

      Then(
        "the result is the same as that of bitmaps conjugated after being flipped")
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
    TestUtils.toDf(sc, sqlContext)(bitmaps, BITMAP_COL)
  }
}
