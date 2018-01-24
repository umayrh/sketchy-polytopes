package com.umayrh.intervalGraph

import java.sql.Date

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner
import org.scalatest.junit.AssertionsForJUnit

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks

import com.holdenkarau.spark.testing._

/**
  * Test class for DateOverlap
  */
class DateOverlapTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with SharedSparkContext
    with DataFrameSuiteBase {
  Feature(
    "A function for grouping overlapping dates - tested using example data") {
    Scenario("the function is invoked on an empty sequence") {
      import sqlContext.implicits._

      Given("A data frame with overlapping dates")
      val inputDf = sc
        .parallelize(
          List[(Date, Date)]((date("1990-01-01"), date("1990-01-11")),
                             (date("1990-01-01"), date("1990-02-01")),
                             (date("1990-01-10"), date("1990-03-01"))))
        .toDF("start", "end")

      When("reducer is invoked")

      Then("result is 0")
    }
  }

  private def date(input: String): Date = {
    Date.valueOf(input)
  }
}
