package com.umayrh.sort

import org.apache.spark.sql.SparkSession

import org.apache.spark.mllib.random.RandomRDDs._

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

/**
  * A simple utility for generating, sorting and writing a given
  * number of uniformly random doubles.
  *
  * The utility uses Spark Mllib's RandomRDD API. The simple
  * alternative is:
  *
  *   val randNums = spark.sparkContext
  *     .parallelize(
  *       Seq.fill(args(0).toInt)(Random.nextInt),
  *       partitions
  *   )
  *   .toDF(COL_NAME)
  *
  * Nonetheless, it will cause:
  *   Exception in thread "main" java.lang.OutOfMemoryError: GC overhead limit exceeded
  *       at scala.collection.mutable.ListBuffer.$plus$eq(ListBuffer.scala:174)
  */
object Main extends SparkBase {
  val COL_NAME = "col"

  def main(args: Array[String]) {
    if (args.length < 2) {
      System.err.println(
        "Expect two positional arguments: data size, and output file path")
      System.exit(1)
    }

    val dataSize = args(0).toLong
    val outputDirPath = args(1)
    val partitions =
      spark.sparkContext.getConf.get("spark.default.parallelism", "1").toInt
    val outputPartitions = 1

    import spark.implicits._

    val randNums =
      uniformRDD(spark.sparkContext, dataSize, partitions).toDF(COL_NAME)

    val sortedRands = randNums.sort(COL_NAME)
    sortedRands
      .coalesce(outputPartitions)
      .write
      .format("com.databricks.spark.csv")
      .option("header", "false")
      .save(outputDirPath)
    spark.stop()
  }
}
