package com.umayrh.intervalGraph

import java.sql.Date

import com.holdenkarau.spark.testing._
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.DataFrame
import org.scalatest._
import org.scalatest.matchers.should._
import org.scalatest.featurespec._

/**
  * Tests [[DateOverlap]]
  */
class DateOverlapIntegrationTest
    extends AnyFeatureSpec
    with GivenWhenThen
    with Matchers
    with SharedSparkContext
    with DataFrameSuiteBase {
  Feature("A function for grouping overlapping dates") {
    Scenario("An dataset without given input columns results in an exception") {
      Given("A dataset without specified input columns")
      val dataset = spark.emptyDataFrame
      When("groupByOverlap is invoked")
      intercept[IllegalArgumentException] {
        DateOverlap.groupByOverlap(dataset, ("s", "t"), "id")
      }
      Then("the result is an exception")
    }

    Scenario("An emtpy dataset results in an empty dataset with given output column") {
      Given("An empty dataset")
      val dataset      = makeDataset(List(("2018-01-01", "2018-01-02")))
      val emptyDataset = dataset.filter(col("s") > Date.valueOf("2019-01-02"))
      When("groupByOverlap is invoked")
      val result = DateOverlap.groupByOverlap(emptyDataset, ("s", "t"), "id")
      Then("the result is an empty dataset with the given output column")
      result.count() should be(0)
      result.columns.contains("id") should be(true)
    }

    Scenario(
      "A dataset of non-overlapping date ranges returns an id column with the same cardinality") {
      Given("A dataset with non-overlapping dates")
      val dataset = makeDataset(
        List(("2018-01-01", "2018-01-02"),
             ("2018-02-01", "2018-02-02"),
             ("2018-03-01", "2018-03-02"),
             ("2018-04-01", "2018-04-02"),
             ("2018-05-01", "2018-05-02")))
      When("groupByOverlap is invoked on")
      val result = DateOverlap.groupByOverlap(dataset, ("s", "t"), "id")
      Then("result is the original dataset with an id column of the same cardinality")
      result.select("id").distinct().count() should be(result.count())
    }

    Scenario("A dataset of overlapping date ranges returns an id column with cardinality 1") {
      Given("A dataset with overlapping dates")
      val dataset = makeDataset(
        List(("2018-01-01", "2018-02-02"),
             ("2018-02-02", "2018-02-02"),
             ("2018-02-02", "2018-03-02"),
             ("2018-03-02", "2018-04-02"),
             ("2018-04-02", "2018-05-02")))
      When("groupByOverlap is invoked on")
      val result = DateOverlap.groupByOverlap(dataset, ("s", "t"), "id")
      Then("result is the original dataset with an id column of the same cardinality")
      result.select("id").distinct().count() should be(1)
    }
  }

  def makeDataset(strRanges: List[(String, String)]): DataFrame = {
    val ranges = strRanges.map(k => (Date.valueOf(k._1), Date.valueOf(k._2)))
    TestUtils.datesToDf(sc, sqlContext)(ranges, "s", "t")
  }
}
