package com.umayrh.testing

import org.scalatestplus.junit.AssertionsForJUnit

import org.scalatest._
import org.scalatest.prop.TableDrivenPropertyChecks

/**
  * Test class that combines behavior- and data-driven testing paradigms
  *
  * Annotate with @RunWith(classOf[JUnitRunner]) to run as JUnit test
  */
class ExampleBasedTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with TableDrivenPropertyChecks {

  feature("A summing function for sequences of integers - tested using example data") {
    scenario("the function is invoked on an empty sequence") {
      Given("an empty sequence")
      val emptySeq = Seq()

      When("reducer is invoked")
      val result = Reducer.reduceSeq(emptySeq, Reducer.sumInts)

      Then("result is 0")
      assert(result == 0)
    }

    scenario("the function is invoked on a sequence without causing overflow/underflow") {
      Given("a sequence of integers less than MAX_VAL and greater than MIN_VAL")
      When("reducer is invoked")
      val testData = Table(
        ("input", "output"),
        (Seq(1, 2, 3), 6),
        (Seq(-1, -2, 3), 0),
        (Seq(100, 2, 3), 105),
        (Seq(-1, 0, 1), 0),
        (Seq(-1, -2, -3), -6)
      )

      Then("result is an integer, which is the sum of input integers")
      forAll(testData) { (input: Seq[Int], output: Int) =>
        assert(Reducer.reduceSeq(input, Reducer.sumInts) == output)
      }
    }

    scenario("the function is invoked on a sequence causing underflow/overflow") {
      Given("a sequence containing MIN_VAL or MAX_VAL")
      val testData = Table(
        "input",
        Seq(Int.MaxValue, 1),
        Seq(Int.MinValue, -1)
      )

      When("reducer is invoked")
      Then("result is an ArithmeticException")
      forAll(testData) { input: Seq[Int] =>
        intercept[ArithmeticException] {
          Reducer.reduceSeq(input, Reducer.sumInts)
        }
      }
    }
  }
}
