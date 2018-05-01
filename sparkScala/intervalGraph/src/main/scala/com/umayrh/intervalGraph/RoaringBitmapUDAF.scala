package com.umayrh.intervalGraph

import org.apache.spark.sql.expressions.MutableAggregationBuffer
import org.apache.spark.sql.expressions.UserDefinedAggregateFunction
import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
import org.roaringbitmap.RoaringBitmap

/**
  * [[UserDefinedAggregateFunction]] for [[org.apache.spark.sql.Dataset]] columns
  * containing [[RoaringBitmap]] objects
  */
class RoaringBitmapUDAF(inputCol: String, outputCol: String)
    extends UserDefinedAggregateFunction {

  def inputSchema: StructType =
    new StructType().add(inputCol, DoubleType)

  def bufferSchema: StructType =
    new StructType().add(outputCol, DoubleType)

  def dataType: DataType = DoubleType

  def deterministic: Boolean = true

  def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, 0.0) // Initialize the result to 0.0
  }

  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    val sum = buffer.getDouble(0) // Intermediate result to be updated
    val price = input.getDouble(0) // First input parameter
    val qty = input.getLong(1) // Second input parameter
    buffer.update(0, sum + (price * qty)) // Update the intermediate result
  }
  // Merge intermediate result sums by adding them
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1.update(0, buffer1.getDouble(0) + buffer2.getDouble(0))
  }
  // THe final result will be contained in 'buffer'
  def evaluate(buffer: Row): Any = {
    buffer.getDouble(0)
  }
}
