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
  * TODO: Reduce memory copies.
  * TODO: Maybe use Kryo directly (KryoOutput/KryoOutputDataOutputBridge, KryoInput/KryoOutputDataInputBridge).
  * TODO: Figure out if/when to deallocate.
  * TODO: The unsafe serde functions need more thought - we'd want Spark to effectively
  *       manipulate ByteBuffers directly.
  * TODO: Better to use pairs of stream to clarify which input and output streams
  *       work together.
  */
object RoaringBitmapSerde {

  /**
    * Serializes a given [[RoaringBitmap]] to a byte array
    * @return serialized byte array
    */
  def serialize(bitmap: RoaringBitmap): Array[Byte] = {
    serialize(bitmap, false, makeOutputStream)
  }

  /**
    * Serializes a given [[RoaringBitmap]] to a byte array using
    * the given [[DataOutputStream]] generator
    * @return serialized byte array
    */
  def serialize(bitmap: RoaringBitmap,
                useDirectBuffer: Boolean,
                outputGen: (ByteBuffer) => DataOutputStream): Array[Byte] = {
    val outputBuffer =
      getBuffer(useDirectBuffer, bitmap.serializedSizeInBytes())
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
      buffer
        .flip() // reset position to allow reading the buffer just written to
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
    deserialize(buffer, false, makeInputStream)
  }

  /**
    * Deserializes a given byte array to a [[RoaringBitmap]] using
    * the given [[DataInputStream]] generator
    * @return byte array deserialized to a [[RoaringBitmap]]
    */
  def deserialize(buffer: Array[Byte],
                  useDirectBuffer: Boolean,
                  inputGen: (ByteBuffer) => DataInputStream): RoaringBitmap = {
    val bitmap = new RoaringBitmap()
    val outputBuffer = getBuffer(useDirectBuffer, buffer.length)
    outputBuffer.put(buffer)
    outputBuffer.flip() // reset position to read the buffer just written to
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

  /**
    * Returns either a direct or an array-backed [[ByteBuffer]] of given capacity
    */
  private def getBuffer(isDirectBuffer: Boolean, capacity: Int): ByteBuffer = {
    if (isDirectBuffer) ByteBuffer.allocateDirect(capacity)
    else ByteBuffer.allocate(capacity)
  }
}
