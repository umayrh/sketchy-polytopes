package com.umayrh.intervalGraph

import java.sql.Date

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import org.scalatest.junit.AssertionsForJUnit
import org.scalatest.{FeatureSpec, GivenWhenThen}

/**
  * Tests [[DateOverlapUtils]]
  */
class DateOverlapUtilsTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with SharedSparkContext
    with DataFrameSuiteBase {
  Feature("Functions for creating bitmaps from a table containing dates") {

    Scenario("mapDateToInt() maps a date range to an int range") {
      Given("A data frame with date columns")
      When("mapDateToInt() is invoked")
      Then("the table has two new columns representing the normalized epoch start and end")
      pending
    }

    Scenario("makeIndexDf() maps an aggregated bitmap to an array of monotonically increasing ids") {
      Given("A data frame with int range, it's aggregated bitmap, and an index column name")
      When("mapDateToInt() is invoked")
      Then(
        "the table has a column with expected name, the same number of rows as the aggregated bitmap, and correct indices")
      pending
    }

    Scenario(
      "intersectBitmaps() maps an dateframe with ranges to an integer such that overlapping ranges have the same value") {
      Given("A data frame with int range, it's aggregated bitmap, and an output column name")
      When("mapDateToInt() is invoked")
      Then(
        "the table has a column with expected name, the same number of rows as the input bitmap, and correct ids")
      pending
    }
  }

  private def date(input: String): Date = {
    Date.valueOf(input)
  }
}
