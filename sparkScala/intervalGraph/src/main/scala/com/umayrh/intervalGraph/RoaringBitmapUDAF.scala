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
  * OR operation across all objects in a given column. Each object is a row with
  * two columns representing the start and the end of the range of set bits in a
  * bitmap. This is a better performing but restricted version of [[RoaringBitmapOrUDAF]].
  *
  * To use in Spark SQL: sqlContext.udf.register("rb", new RoaringBitmapUDAF)
  */
class RoaringBitmapUDAF(startCol: String, endCol: String)
    extends UserDefinedAggregateFunction {
  def inputSchema: StructType =
    new StructType()
      .add(startCol, LongType)
      .add(endCol, LongType)

  def bufferSchema: StructType = new StructType().add("udaf_buffer", BinaryType)

  def dataType: DataType = BinaryType

  def deterministic: Boolean = true

  def initialize(buffer: MutableAggregationBuffer): Unit = {
    buffer.update(0, RoaringBitmapSerde.serialize(new RoaringBitmap()))
  }

  def update(buffer: MutableAggregationBuffer, input: Row): Unit = {
    buffer.update(0, set(buffer.get(0), input.getLong(0), input.getLong(1)))
  }

  def merge(buffer1: MutableAggregationBuffer, buffer2: Row): Unit = {
    buffer1.update(0, or(buffer1.get(0), buffer2.get(0)))
  }

  /*
   * Since inputBitmap only has a single subsequence of
   * set bits, then we can probably do a more efficient union.
   * Consider using a writer like OrderedWriter or a variant of
   * RoaringBitmap.bitmapOfUnordered
   * http://richardstartin.uk/roaringbitmaps-construction-performance/
   */
  private def set(buffer: Any, start: Long, end: Long): Array[Byte] = {
    val bufferBitmap =
      RoaringBitmapSerde.deserialize(buffer.asInstanceOf[Array[Byte]])
    bufferBitmap.add(start, end)
    RoaringBitmapSerde.serialize(bufferBitmap)
  }

  private def or(buffer1: Any, buffer2: Any): Array[Byte] = {
    val b1 = RoaringBitmapSerde.deserialize(buffer1.asInstanceOf[Array[Byte]])
    val b2 = RoaringBitmapSerde.deserialize(buffer2.asInstanceOf[Array[Byte]])
    RoaringBitmapSerde.serialize(RoaringBitmap.or(b1, b2))
  }

  def evaluate(buffer: Row): Any = {
    buffer.get(0)
  }
}
