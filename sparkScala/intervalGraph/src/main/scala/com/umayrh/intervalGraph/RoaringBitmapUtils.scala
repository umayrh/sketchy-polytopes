package com.umayrh.intervalGraph

import java.io.{DataInputStream, DataOutputStream, InputStream, OutputStream}
import java.nio.ByteBuffer

import org.roaringbitmap.RoaringBitmap

/**
  * Utilities for manipulating [[org.roaringbitmap.RoaringBitmap]]
  *
  * @see [[https://github.com/RoaringBitmap/RoaringBitmap/blob/master/examples/SerializeToByteArrayExample.java]]
  */
object RoaringBitmapUtils {

  /**
    * Serializes a given [[RoaringBitmap]] to a byte array
    * @return serialized byte array
    */
  def serialize(bitmap: RoaringBitmap): Array[Byte] = {
    val outputBuffer = ByteBuffer.allocate(bitmap.serializedSizeInBytes())
    bitmap.serialize(makeOutputStream(outputBuffer))
    outputBuffer.array()
  }

  /**
    *
    * Deserializes a given byte array to a [[RoaringBitmap]]
    * @return deserialized [[RoaringBitmap]]
    */
  def deserialize(buffer: Array[Byte]): RoaringBitmap = {
    val bitmap = new RoaringBitmap()
    bitmap.deserialize(makeInputStream(ByteBuffer.wrap(buffer)))
    bitmap
  }

  /**
    * @return a [[DataOutputStream]] initialized with the given byte buffer
    */
  def makeOutputStream(outputBuffer: ByteBuffer): DataOutputStream = {
    new DataOutputStream(new OutputStream {

      override def close() {}

      override def flush() {}

      override def write(b: Int) {
        outputBuffer.put(b.byteValue())
      }

      override def write(b: Array[Byte]) {
        outputBuffer.put(b)
      }

      override def write(b: Array[Byte], off: Int, len: Int) {
        outputBuffer.put(b, off, len)
      }
    })
  }

  /**
    * @return a [[java.io.DataInputStream]] initialized with the given byte buffer
    */
  def makeInputStream(outputBuffer: ByteBuffer): DataInputStream = {
    new DataInputStream(new InputStream {
      var idx: Int = 0

      override def read: Int = {
        val res = outputBuffer.get(idx) & 0xff
        idx += 1
        res
      }

      override def read(b: Array[Byte]): Int = read(b, 0, b.length)

      override def read(b: Array[Byte], off: Int, len: Int): Int = {
        System.arraycopy(outputBuffer.array(), idx, b, off, len)
        idx += len
        len
      }
    })
  }
}
