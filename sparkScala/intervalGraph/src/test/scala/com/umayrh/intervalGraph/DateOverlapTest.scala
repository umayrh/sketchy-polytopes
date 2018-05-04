package com.umayrh.intervalGraph

import com.holdenkarau.spark.testing._
import org.scalatest._
import org.scalatest.junit.AssertionsForJUnit

/**
  * Tests [[DateOverlap]]
  */
class DateOverlapTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with SharedSparkContext
    with DataFrameSuiteBase {
  Feature("A function for grouping overlapping dates") {
    Scenario("An empty dataset of date ranges returns without a new column") {

      // TODO
      Given("A data frame with overlapping dates")
      When("groupByOverlap is invoked on an empty sequence")
      Then("result is the original dataframe")
    }
  }
}
