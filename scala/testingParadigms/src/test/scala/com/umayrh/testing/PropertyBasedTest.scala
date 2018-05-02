package com.umayrh.testing

import org.scalacheck.Gen._
import org.scalacheck._
import org.scalatest._
import org.scalatest.junit.AssertionsForJUnit
import org.scalatest.prop.GeneratorDrivenPropertyChecks

/**
  * Test class that combines behavior- and property-driven testing paradigms
  * See also ScalaCheck guide https://github.com/rickynils/scalacheck/blob/master/doc/UserGuide.md
  *
  * Annotate with @RunWith(classOf[JUnitRunner]) to run as JUnit test
  */
class PropertyBasedTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with GeneratorDrivenPropertyChecks
    with Matchers {

  feature(
    "A summing function for sequences of integers - tested using function properties") {
    scenario("the function is commutative") {
      Given("a sequence of integers of random size and with random elements")
      val inputSeqGen =
        Gen.listOf(choose(Int.MinValue, Int.MaxValue)).suchThat(_.size >= 0)

      When("reducer is invoked on the sequence and its shuffled version")
      Then(
        "result is the equal if there no overflow/underflow, ArithmeticException thrown otherwise")

      forAll(inputSeqGen) { inputSeq: List[Int] =>
        var result = 0
        var resultShuffled = 0
        var resultThrew = false
        var resultShuffledThrew = false

        try {
          result = ReducerRedux.reduceSeq(inputSeq, ReducerRedux.sumLongs)
        } catch {
          case e: ArithmeticException => resultThrew = true
        }

        try {
          resultShuffled =
            ReducerRedux.reduceSeq(scala.util.Random.shuffle(inputSeq),
                                   ReducerRedux.sumLongs)
        } catch {
          case e: ArithmeticException => resultShuffledThrew = true
        }

        resultThrew should be(resultShuffledThrew)

        if (!resultThrew) {
          result should be(resultShuffled)
        }
      }
    }

    scenario("the function is associatative") {
      Given("a sequence of integers of random size and with random elements")
      val inputSeqGen =
        Gen.listOf(choose(Int.MinValue, Int.MaxValue)).suchThat(_.size >= 0)
      val randomNumGen = scala.util.Random

      When("reducer is invoked on the sequence and its subsets")
      Then(
        "result is the equal if there no overflow/underflow, ArithmeticException thrown otherwise")
      forAll(inputSeqGen) { inputSeq: List[Int] =>
        var result = 0
        var resultSplit = 0
        var resultThrew = false
        var resultSplitThrew = false
        val inputSeqLen = inputSeq.length
        val splitIndex = if (inputSeqLen == 0) 0 else randomNumGen.nextInt()

        try {
          result = ReducerRedux.reduceSeq(inputSeq, ReducerRedux.sumLongs)
        } catch {
          case e: ArithmeticException => resultThrew = true
        }

        try {
          val inputSeqSplit =
            inputSeq.splitAt(splitIndex).productIterator.toList
          val inputSeqSplitResult = inputSeqSplit
            .map(_.asInstanceOf[List[Int]])
            .map(seq => ReducerRedux.reduceSeq(seq, ReducerRedux.sumLongs))
          resultSplit =
            ReducerRedux.reduceSeq(inputSeqSplitResult, ReducerRedux.sumLongs)
        } catch {
          case e: ArithmeticException => resultSplitThrew = true
        }
        resultThrew should be(resultSplitThrew)

        if (!resultThrew) {
          result should be(resultSplit)
        }
      }
    }
  }
}
