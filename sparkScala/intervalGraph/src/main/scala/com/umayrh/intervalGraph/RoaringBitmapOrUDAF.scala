package com.umayrh.intervalGraph

import org.apache.spark.sql.Row
import org.apache.spark.sql.expressions.{
  MutableAggregationBuffer,
  UserDefinedAggregateFunction
}
import org.apache.spark.sql.types._
import org.roaringbitmap.RoaringBitmap

/**
  * [[UserDefinedAggregateFunction]] for [[org.apache.spark.sql.Dataset]] doing an
  * OR operation across all [[RoaringBitmap]] objects in a given column.
  *
  * To use in Spark SQL: sqlContext.udf.register("rb", new RoaringBitmapOrUDAF)
  * TODO: figure out how to avoid incessant serde
  */
object RoaringBitmapOrUDAF {
  // use to create a new
  private val BASE_MAP = RoaringBitmapSerde.serialize(new RoaringBitmap())
}

class RoaringBitmapOrUDAF(inputCol: String)
    extends UserDefinedAggregateFunction {
  import RoaringBitmapOrUDAF.BASE_MAP

  def inputSchema: StructType = new StructType().add(inputCol, BinaryType)

  def bufferSchema: StructType = new StructType().add("udaf_buffer", BinaryType)

  def dataType: DataType = BinaryType

  def deterministic: Boolean = true

  def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, BASE_MAP.clone())
  }

  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    buffer.update(0, or(buffer.get(0), input.get(0)))
  }

  // Merge intermediate result sums by adding them
  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1.update(0, or(buffer1.get(0), buffer2.get(0)))
  }

  private def or(buffer: Any, input: Any): Array[Byte] = {
    val inputBitmap =
      RoaringBitmapSerde.deserialize(input.asInstanceOf[Array[Byte]])
    val bufferBitmap =
      RoaringBitmapSerde.deserialize(buffer.asInstanceOf[Array[Byte]])
    bufferBitmap.or(inputBitmap)
    RoaringBitmapSerde.serialize(bufferBitmap);
  }

  def evaluate(buffer: Row): Any = {
    buffer.get(0)
  }
}
