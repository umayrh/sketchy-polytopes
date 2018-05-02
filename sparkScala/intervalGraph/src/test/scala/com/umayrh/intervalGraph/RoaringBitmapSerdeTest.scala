package com.umayrh.intervalGraph

import com.umayrh.intervalGraph.RoaringBitmapSerde._
import org.roaringbitmap.RoaringBitmap
import org.scalacheck.Gen
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.{FeatureSpec, GivenWhenThen}

/**
  * Tests [[RoaringBitmapSerde]]
  */
object RoaringBitmapSerdeTest
    extends FeatureSpec
    with GivenWhenThen
    with GeneratorDrivenPropertyChecks {
  Feature("Functions for serializing and deserializing RoaringBitmap objects") {
    Scenario(
      "RoaringBitmaps before serialization and after deserialization are equal") {
      Given("a sequence of integer pairs between 0 and Int.Max")
      val pairGen = for {
        n <- Gen.choose(0L, Int.MaxValue.longValue())
        m <- Gen.choose(n, Int.MaxValue.longValue())
      } yield (n, m)

      When("a given bitmap is serialized and then deserialized")
      Then("the cardinality of the bitmap does not change")

      // TODO: figure our why forAll cannot be resolved
      //     forAll(pairGen) { (start: Long, end: Long) =>
      //       val bitmap = new RoaringBitmap()
      //       bitmap.add(start, end)

      //       val serializedMap = serialize(bitmap, makeOutputStream)
      //       val deserializedMap = deserialize(serializedMap, makeInputStream)

      //       bitmap.getCardinality equals (deserializedMap.getCardinality)
      //     }
    }
  }
}
