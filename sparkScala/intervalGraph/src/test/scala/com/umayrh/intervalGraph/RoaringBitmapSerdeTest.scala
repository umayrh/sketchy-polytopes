package com.umayrh.intervalGraph

import java.io.{DataInputStream, DataOutputStream}
import java.nio.ByteBuffer

import com.umayrh.intervalGraph.RoaringBitmapSerde._
import org.roaringbitmap.RoaringBitmap
import org.scalatest.prop.GeneratorDrivenPropertyChecks
import org.scalatest.{FeatureSpec, GivenWhenThen, Matchers}

/**
  * Tests [[RoaringBitmapSerde]]
  */
class RoaringBitmapSerdeTest
    extends FeatureSpec
    with GivenWhenThen
    with GeneratorDrivenPropertyChecks
    with Matchers {
  Feature("Functions for serializing and deserializing RoaringBitmap objects") {
    Scenario(
      "RoaringBitmaps before serialization and after deserialization are equal") {
      Given("a sequence of integer pairs between 0 and Int.Max")
      val pairGen = List
        .fill(1000)(Int.MaxValue)
        .map(k =>
          (scala.util.Random.nextInt(k), scala.util.Random.nextInt(1000)))
        .map(k => (Int.int2long(k._1), Int.int2long(k._2)))

      When("a given bitmap is serialized and then deserialized")
      Then(
        "the cardinality of the bitmap is 0 after flipping bits in the given range")

      pairGen.map({
        case (start: Long, len: Long) =>
          val end = start + len - 1
          val bitmap = makeBitmap(start, end)

          val streams: Seq[(Boolean,
                            (ByteBuffer) => DataOutputStream,
                            (ByteBuffer) => DataInputStream)] =
            Seq((false, makeOutputStream, makeInputStream),
                (true, makeUnsafeOutputStream, makeUnsafeInputStream))

          for ((useDirectBuffer, outputStream, inputStream) <- streams) {
            val serializedMap = serialize(bitmap, useDirectBuffer, outputStream)
            val deserializedMap =
              deserialize(serializedMap, useDirectBuffer, inputStream)

            RoaringBitmap
              .flip(deserializedMap, start, end)
              .getCardinality should be(0)
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
