package com.umayrh.intervalGraph

import java.io.{DataInputStream, DataOutputStream, InputStream, OutputStream}
import java.nio.ByteBuffer

import com.esotericsoftware.kryo.io.{UnsafeMemoryInput, UnsafeMemoryOutput}
import com.google.common.base.Preconditions
import org.roaringbitmap.RoaringBitmap
import sun.nio.ch.DirectBuffer

/**
  * Serialization/deserialization utilities for [[org.roaringbitmap.RoaringBitmap]]
  *
  * @see [[https://github.com/RoaringBitmap/RoaringBitmap/blob/master/examples/SerializeToByteArrayExample.java]]
  *
  * TODO: reduce memory copies, and maybe use Kryo directly
  * TODO: figure out if/when to deallocate
  * TODO: the unsafe serde needs more thought - we'd want Spark to effectively
  * manipulate ByteBuffers directly
  */
object RoaringBitmapSerde {

  /**
    * Serializes a given [[RoaringBitmap]] to a byte array
    * @return serialized byte array
    */
  def serialize(bitmap: RoaringBitmap): Array[Byte] = {
    serialize(bitmap, makeUnsafeOutputStream)
  }

  /**
    * Serializes a given [[RoaringBitmap]] to a byte array using
    * the given [[DataOutputStream]] generator
    * @return serialized byte array
    */
  def serialize(bitmap: RoaringBitmap,
                outputGen: (ByteBuffer) => DataOutputStream): Array[Byte] = {
    val outputBuffer = ByteBuffer.allocateDirect(bitmap.serializedSizeInBytes())
    bitmap.serialize(outputGen.apply(outputBuffer))
    byteBufferToArray(outputBuffer)
  }

  /**
    * @return [[Array[Byte]] version of [[ByteBuffer]], handling the
    *        case where the buffer may not be array-backed
    */
  private def byteBufferToArray(buffer: ByteBuffer): Array[Byte] = {
    if (buffer.hasArray) {
      buffer.array()
    } else {
      val output = new Array[Byte](buffer.capacity())
      // reset position to allow reading the buffer just written to
      buffer.rewind()
      // performance gain down the drain
      buffer.get(output, 0, output.length)
      output
    }
  }

  /**
    * Deserializes a given byte array to a [[RoaringBitmap]]
    * @return deserialized [[RoaringBitmap]]
    */
  def deserialize(buffer: Array[Byte]): RoaringBitmap = {
    deserialize(buffer, makeUnsafeInputStream)
  }

  /**
    * Deserializes a given byte array to a [[RoaringBitmap]] using
    * the given [[DataInputStream]] generator
    * @return byte array deserialized to a [[RoaringBitmap]]
    */
  def deserialize(buffer: Array[Byte],
                  inputGen: (ByteBuffer) => DataInputStream): RoaringBitmap = {
    val bitmap = new RoaringBitmap()
    var outputBuffer = ByteBuffer.allocateDirect(buffer.length)
    outputBuffer = outputBuffer.put(buffer)
    // reset position to allow reading the buffer just written to
    outputBuffer.rewind()
    bitmap.deserialize(inputGen.apply(outputBuffer))
    bitmap
  }

  /**
    * @return an [[UnsafeMemoryOutput]]-based stream set to output to given buffer
    */
  def makeUnsafeOutputStream(outputBuffer: ByteBuffer): DataOutputStream = {
    // otherwise UnsafeMemoryOutput will throw. Use ByteBuffer.allocateDirect
    Preconditions.checkArgument(outputBuffer.isInstanceOf[DirectBuffer])
    val out = new UnsafeMemoryOutput(outputBuffer.capacity())
    out.setBuffer(outputBuffer)
    new DataOutputStream(out)
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
    * return an [[UnsafeMemoryInput]]-based stream set to read from given buffer
    */
  def makeUnsafeInputStream(inputBuffer: ByteBuffer): DataInputStream = {
    new DataInputStream(new UnsafeMemoryInput(inputBuffer))
  }

  /**
    * @return a [[java.io.DataInputStream]] set to read from the given byte buffer
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
