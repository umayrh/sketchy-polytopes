package com.umayrh.intervalGraph

import java.sql.Date
import java.util

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner
import org.scalatest.junit.AssertionsForJUnit
import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks
import com.holdenkarau.spark.testing._
import org.apache.spark.sql.types.DataTypes
import org.roaringbitmap.RoaringBitmap

/**
  * Tests [[DateOverlap]]
  */
class DateOverlapTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with SharedSparkContext
    with DataFrameSuiteBase {
  Feature(
    "A function for grouping overlapping dates - tested using example data") {
    import sqlContext.implicits._
    Scenario("groupByOverlap is invoked on an empty sequence") {

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

    Scenario("mapIntRangeToBitSet creates a column containing bitmap") {

      Given("A data frame with overlapping dates")
      val inputDf = sc
        .parallelize(List[(Long, Long)]((1, 3), (1, 4), (4, 5)))
        .toDF("start", "end")

      When("mapIntRangeToBitSet is invoked on given integer ranges")
      val outputDf =
        DateOverlap.mapIntRangeToBitSet(inputDf, "start", "end", "bitmap")

      Then("the table's schema contains a new column of type BinaryType")
      outputDf.schema.fields.size equals 3
      outputDf.schema.fields.map(f => f.name) contains ("bitmap")
      outputDf.schema.fields
        .filter(f => f.name.equals("bitmap"))(0)
        .dataType equals (DataTypes.BinaryType)

      val bitmaps: Array[RoaringBitmap] = outputDf
        .select("bitmap")
        .collect()
        .map(row => {
          RoaringBitmapUtils.deserialize(row.get(0).asInstanceOf[Array[Byte]])
        })

      val result = new RoaringBitmap()
      bitmaps.foreach(b => result.or(b))
      result.getCardinality equals (5)
      RoaringBitmap.flip(result, 1L, 5L).getCardinality equals (0)

    }
  }

  private def date(input: String): Date = {
    Date.valueOf(input)
  }
}
