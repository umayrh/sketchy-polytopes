package com.umayrh.intervalGraph

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions.rand
import org.roaringbitmap.RoaringBitmap
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.{FeatureSpec, GivenWhenThen, Matchers}

import scala.util.Random

/**
  * Tests [[RoaringBitmapUDAF]]
  */
object RoaringBitmapUDAFTest {
  val MAX_ITER = 50
  val INPUT_COL = "bitmap"
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
    "Spark User-defined Aggregation Function for performing an OR op on a RoaringBitmap column") {
    val orFn = new RoaringBitmapUDAF(INPUT_COL)

    Scenario("The UDAF is commutative ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val df = toDf(inputData())
      val expectedDf = df.agg(orFn(df(INPUT_COL)))

      When("bitmaps rows in a dataframe are shuffled")
      val shuffledDf = df.orderBy(rand())
      val actualDf = shuffledDf.agg(orFn(shuffledDf(INPUT_COL)))

      Then("the result of UDAF doesn't change")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }

    Scenario("The UDAF is associative ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val data = inputData()
      val df = toDf(data)
      val expectedDf = df.agg(orFn(df(INPUT_COL)).as(OUTPUT_COL))

      When(
        "UDAF is invoked on the results of randomly ordered UDAF invocations")
      val splitSize = Random.nextInt(data.size)
      val splitData = data.grouped(splitSize)
      val splitDf = splitData.map(toDf)
      val bitmapsDf =
        splitDf.map(df => df.agg(orFn(df(INPUT_COL)).as(OUTPUT_COL)))
      val unionedDf = Random.shuffle(bitmapsDf).reduce(_.union(_))
      val actualDf = unionedDf.agg(orFn(unionedDf(OUTPUT_COL)))

      Then("the result of UDAF doesn't change")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }

    Scenario("The UDAF is idempotent") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val df = toDf(inputData())
      val expectedDf = df.agg(orFn(df(INPUT_COL)).as(OUTPUT_COL))

      When("invoking the UDAF N times (N >= 1) on the same bitmap")
      var actualDf = df.withColumnRenamed(INPUT_COL, OUTPUT_COL)
      val numIter = Random.nextInt(MAX_ITER) + 1
      Range(0, numIter).foreach(k =>
        actualDf = actualDf.agg(orFn(actualDf(OUTPUT_COL)).as(OUTPUT_COL)))

      Then("doesn't change the bitmap")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }

    Scenario("The UDAF obeys De Morgan's law: A OR B = ~A AND ~B ") {
      Given("bitmaps containing possibly overlapping ranges of bits set")
      val data = inputData()
      val flipped = data.map(b => RoaringBitmap.andNot(b, b))
      val conjugated = flipped.reduce(RoaringBitmap.and)
      val expectedDf = toDf(List(conjugated))

      When("UDAF is invoked on a set of bitmaps")
      val df = toDf(data)
      val actualDf = df.agg(orFn(df(INPUT_COL)).as(INPUT_COL))

      Then(
        "the result is the same as that of bitmaps conjugated after being flipped")
      TestUtils.assertDataFrameEquals(expectedDf, actualDf)
    }
  }

  /**
    * @return list of [[RoaringBitmap]]s with a randomly generated range of bits set
    */
  private def inputData(): List[RoaringBitmap] = {
    TestUtils
      .getRandRanges()
      .map(range => TestUtils.makeBitmap(range._1, range._2))
  }

  /**
    * @param bitmaps list of [[RoaringBitmap]]s
    * @return a dataframe out of the given list
    */
  private def toDf(bitmaps: List[RoaringBitmap]): DataFrame = {
    val serializedBitmaps = bitmaps.map(RoaringBitmapSerde.serialize)
    // implicits, yuck...
    import sqlContext.implicits._
    sc.parallelize(serializedBitmaps).toDF(INPUT_COL)
  }
}
