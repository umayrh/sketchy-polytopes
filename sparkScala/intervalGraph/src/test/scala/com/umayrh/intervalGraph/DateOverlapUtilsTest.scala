package com.umayrh.intervalGraph

import java.sql.Date

import com.holdenkarau.spark.testing.{DataFrameSuiteBase, SharedSparkContext}
import org.apache.spark.sql.types.DataTypes
import org.roaringbitmap.RoaringBitmap
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
    import sqlContext.implicits._

    Scenario("mapIntRangeToBitSet() creates a column containing bitmap") {

      Given("A data frame with overlapping dates")
      val inputDf = sc
        .parallelize(List[(Long, Long)]((1, 3), (1, 4), (4, 5)))
        .toDF("start", "end")

      When("mapIntRangeToBitSet is invoked on given integer ranges")
      val outputDf =
        DateOverlapUtils.mapIntRangeToBitmap(inputDf, "start", "end", "bitmap")

      Then(
        "the table's schema contains a new column of serialized RoaringBitmap")
      outputDf.schema.fields.size equals 3
      outputDf.schema.fields.map(f => f.name) contains ("bitmap")
      outputDf.schema.fields
        .filter(f => f.name.equals("bitmap"))(0)
        .dataType equals (DataTypes.BinaryType)

      val bitmaps: Array[RoaringBitmap] = outputDf
        .select("bitmap")
        .collect()
        .map(row => {
          RoaringBitmapSerde.deserialize(row.get(0).asInstanceOf[Array[Byte]])
        })

      val result = new RoaringBitmap()
      bitmaps.foreach(b => result.or(b))
      And("the serialized RoaringBitmap can be correctly deserialized")
      result.getCardinality equals (5)
      RoaringBitmap.flip(result, 1L, 5L).getCardinality equals (0)

    }
  }

  private def date(input: String): Date = {
    Date.valueOf(input)
  }
}
