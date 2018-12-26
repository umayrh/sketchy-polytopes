package com.umayrh.sort

import org.apache.spark.sql.SparkSession

import scala.util.Random

/**
  * Trait for Spark applications
  */
trait SparkBase {
  val spark: SparkSession = SparkSession
    .builder()
    .getOrCreate()
  spark.sparkContext.setLogLevel("ERROR")

  /**
    * Closes a Spark session object
    */
  def close = {
    spark.close()
  }
}

object Main extends SparkBase {
  val COL_NAME = "col"

  def main(args: Array[String]) {
    if (args.length < 2) {
      System.err.println(
        "Expect two positional arguments: data size, and output file path")
      System.exit(1)
    }

    import spark.implicits._
    val randNums = spark.sparkContext
      .parallelize(
        Seq.fill(args(0).toInt)(Random.nextInt),
        spark.sparkContext.getConf.get("spark.default.parallelism", "1").toInt
      )
      .toDF(COL_NAME)

    val sortedRands = randNums.sort(COL_NAME)
    sortedRands
      .coalesce(1)
      .write
      .format("com.databricks.spark.csv")
      .option("header", "false")
      .save(args(1))
    spark.stop()
  }
}
