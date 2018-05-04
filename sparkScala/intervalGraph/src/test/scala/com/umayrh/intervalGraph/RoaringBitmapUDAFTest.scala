package com.umayrh.intervalGraph

import java.io.{DataInputStream, DataOutputStream}
import java.nio.ByteBuffer

import com.umayrh.intervalGraph.RoaringBitmapUDAF._
import org.roaringbitmap.RoaringBitmap
import org.scalatest.{FeatureSpec, GivenWhenThen, Matchers}
import org.scalatest.prop.GeneratorDrivenPropertyChecks

/**
  * Tests [[RoaringBitmapUDAF]]
  */
class RoaringBitmapUDAFTest
    extends FeatureSpec
    with GivenWhenThen
    with GeneratorDrivenPropertyChecks
    with Matchers {
  Feature(
    "Spark User-defined Aggregation Function for performing an OR op on a RoaringBitmap column") {
    Scenario("The UDAF is commutative ") {
      Given("")

      When("")
      Then("")

    }
  }
}
