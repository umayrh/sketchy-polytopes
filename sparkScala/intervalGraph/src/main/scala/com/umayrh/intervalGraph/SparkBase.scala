package com.umayrh.intervalGraph

import org.apache.spark.sql.SparkSession

/**
  * Trait for initializing Spark session
  */
trait SparkBase {
  // TODO allow passing arguments via flags
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
