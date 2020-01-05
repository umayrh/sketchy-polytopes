package com.umayrh.sort

import com.holdenkarau.spark.testing.DataFrameSuiteBase
import java.io.{File, FilenameFilter}

import org.scalatest.{FeatureSpec, GivenWhenThen, Matchers}
import org.scalatest.junit.AssertionsForJUnit

import scala.io.Source
import scala.reflect.io.Directory

class MainTest
    extends FeatureSpec
    with AssertionsForJUnit
    with GivenWhenThen
    with Matchers
    with DataFrameSuiteBase {

  var outputFile: File = null

  override def beforeAll(): Unit = {
    super.beforeAll()
    outputFile = File.createTempFile("MainTest", "")
  }

  override def afterAll(): Unit = {
    super.afterAll()
    val directory = new Directory(outputFile)
    directory.deleteRecursively()
  }

  Feature("Class to generate, sort and write random numbers to a CSV file") {

    Scenario("A thousand random numbers are generated") {
      Given("Program inputs: a thousand, and output file location")
      val dataSize       = math.pow(10, 3).toInt
      val outputLocation = outputFile.getAbsolutePath
      outputFile.delete()

      When("Main.main is invoked")

      Main.main(Array(dataSize.toString, outputLocation))

      Then("the output file exists and contains a million numbers")

      val outputDir = new File(outputLocation)
      outputDir.exists() should be(true)

      val fileFilter = new FilenameFilter {
        override def accept(dir: File, name: String): Boolean =
          name.endsWith(".csv")
      }

      val outputCsvFile = outputDir.listFiles(fileFilter)(0)
      Source.fromFile(outputCsvFile).getLines.size should be(dataSize)
    }
  }
}
