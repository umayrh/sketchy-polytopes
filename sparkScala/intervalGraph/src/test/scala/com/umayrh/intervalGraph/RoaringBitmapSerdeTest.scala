package com.umayrh.intervalGraph

import java.io.{DataInputStream, DataOutputStream}
import java.nio.ByteBuffer

import com.umayrh.intervalGraph.RoaringBitmapSerde._
import org.roaringbitmap.RoaringBitmap
import org.scalacheck.Gen
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.{FeatureSpec, GivenWhenThen}

/**
  * Tests [[RoaringBitmapSerde]]
  */
class RoaringBitmapSerdeTest
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

      // TODO: figure our why compiler cannot resolve forAll
      pairGen.map({
        case (start: Long, end: Long) =>
          val bitmap = makeBitmap(start, end)

          val streams: Seq[((ByteBuffer) => DataOutputStream,
                            (ByteBuffer) => DataInputStream)] =
            Seq((makeOutputStream, makeInputStream),
                (makeUnsafeOutputStream, makeUnsafeInputStream))

          for ((outputStream, inputStream) <- streams) {
            val serializedMap = serialize(bitmap, outputStream)
            val deserializedMap = deserialize(serializedMap, inputStream)

            RoaringBitmap
              .flip(deserializedMap, start, end)
              .getCardinality equals (bitmap.getCardinality)
          }
      })
    }
  }

  /*
   * @return a [[RoaringBitmap]] with bits in the inclusive range (start, end) set to 1
   */
  private def makeBitmap(start: Long, end: Long): RoaringBitmap = {
    val bitmap = new RoaringBitmap()
    bitmap.add(start, end)
    bitmap
  }
}
