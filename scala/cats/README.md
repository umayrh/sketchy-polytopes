# Testing Paradigms

A three-tiered [pyramid](https://guides.gradle.org/testing-gradle-plugins/) models unit, integration, and functional testing as relying each other.
A complimentary way would be to model tests in [contractual terms](https://en.wikipedia.org/wiki/Behavior-driven_development) of interaction/behavior. 
The focus is on understanding the user and context for code. 

[Spock](http://spockframework.org), a testing framework for Groovy and Java, elegantly supports [interaction-based 
testing](http://spockframework.org/spock/docs/1.1/interaction_based_testing.html). For Scala, [ScalaTest](http://www.scalatest.org) has similar
features. This document outlines some of ScalaTest's features. As of 10-2017, ScalaTest docs are available only for v3.0.1.

## Gradle and ScalaTest

While ScalaTest has a [plugin](http://www.scalatest.org/user_guide/using_the_scalatest_maven_plugin) for Maven, there's none for Gradle that would
support running tests Junit and/or ScalaTest. As a workaround, we can add a ScalaTest-specific task to build.gradle for a Scala project:

```

task scalaTest(dependsOn: ['testClasses'], type: JavaExec) {
  main = 'org.scalatest.tools.Runner'
  args = ['-R', 'build/classes/scala/test', '-o']
  classpath = sourceSets.test.runtimeClasspath
}

test.dependsOn scalaTest
```

Otherwise, we'll need to tag classes with `@RunWith(classOf[JUnitRunner])` for `gradle test` to run tests at all. By default, Gradle's Scala 
[plugin](https://docs.gradle.org/current/userguide/scala_plugin.html) only compiles test classes.

## Behavior-driven testing

### Features and scenarios

Iteractions can be specified using a [Hoare triple](https://en.wikipedia.org/wiki/Hoare_logic#Hoare_triple) such as Given-When-Then and then 
aggregated into "scenarios" and "features." In ScalaTest, this require implementing the [GivenWhenThen](http://doc.scalatest.org/3.0.1/#org.scalatest.GivenWhenThen) 
trait. E.g.

```
feature("A summing function for sequences of integers") {
    scenario("the function is invoked on an empty sequence") {
        Given("an empty sequence")
        val emptySeq = Seq()

        When("reducer is invoked")
        val result = Main.reduceSeq(emptySeq, Main.sumInts)

        Then("result is 0")
        assert(result == 0)
    }
}
```

Given-When-Then statements provide for structured documentation. These user stories can be printed out:

```
$ gradle test

> Task :scalaTest
Discovery starting.
Discovery completed in 139 milliseconds.
Run starting. Expected test count is: 3
MainTest:
Feature: A summing function for sequences of integers
  Scenario: the function is invoked on an empty sequence
    Given an empty sequence 
    When reducer is invoked 
    Then result is 0 
  Scenario: the function is invoked on a sequence without causing overflow/underflow
    Given a sequence of integers less than MAX_VAL and greater than MIN_VAL 
    When reducer is invoked 
    Then result is an integer, which is the sum of input integers 
  Scenario: the function is invoked on a sequence causing underflow/overflow
    Given an empty sequence 
    When reducer is invoked 
    Then result is an ArithmeticException 
Run completed in 305 milliseconds.
Total number of tests run: 3
Suites: completed 2, aborted 0
Tests: succeeded 3, failed 0, canceled 0, ignored 0, pending 0
All tests passed.
```

See [FeatureSpec](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.FeatureSpec) for more properties.

### Data-driven testing

It seems like this is a rubric for specifying data tables and/or data pipes for testing. [Spock](http://spockframework.org/spock/docs/1.0/data_driven_testing.html)
goes a long way here. [ScalaTest](http://www.scalatest.org/user_guide/table_driven_property_checks) allows encoding test data in a 
[Table](http://doc.scalatest.org/3.0.0/index.html#org.scalatest.prop.Tables). E.g.

```
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
    forAll (testData) { (input: Seq[Int], output: Int) =>
        assert(Main.reduceSeq(input, Main.sumInts) == output)
    }
}
```

A `Table` needs a header as its first row, and may accept up to 22 columns. Each row forms a tuple, and `forAll` is used to iterate over and map each tuple.

### Property-based testing

[Property-based](https://ucaat.etsi.org/2016/documents/S07_SPECSOLUTIONS_Nagy.pdf) testing seems to have two goals:
* Specify not specific examples but "generators" that produce a class of examples
* Test not specific results but "properties" of a function

This allows random test data generation and, possibly, more rigorous testing (what properties would be sufficient or necessary?). The toy exmaple is
that of testing a function that adds two integers. Instead of specifying test data, we would generate random integers and test for properties of
addition: identity, commutativity, associativity, and distributivity.

[ScalaCheck](http://www.scalacheck.org) is a Scala library for property-based testing, which is also supported by 
[ScalaTest](http://www.scalatest.org/user_guide/generator_driven_property_checks). Generally, these tests would:

* extend the `GeneratorDrivenPropertyChecks` trait,
* create randomly generated test cases using `org.scalacheck.Arbitrary` or `org.scalacheck.Gen` generators,
* use the `forAll` method for iterating for randomly generated test cases (this method comes from the `GeneratorDrivenPropertyChecks` trait),
* use [matchers](http://www.scalatest.org/user_guide/using_matchers) for specifying assertions, and
* use `whenever` method to selectively test for conditions (beware that test-case may fail if `whenever` ends up being too exclusive)

See also:
* [ScalaCheck Github](https://github.com/rickynils/scalacheck)
* [ScalaCheck User Guide](https://github.com/rickynils/scalacheck/blob/master/doc/UserGuide.md)
* [ScalaCheck: The Definitive Guide - Coding Examples](https://booksites.artima.com/scalacheck/examples/index.html)
