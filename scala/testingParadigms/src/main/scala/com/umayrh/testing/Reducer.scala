package com.umayrh.testing

import java.lang.Math.addExact

/**
  * A class that offers a simple implementation of a reducer
  */
object Reducer {

  /**
    * Aggregates an input sequence of integers
    *
    */
  def reduceSeq(input: Seq[Int], binaryReducer: (Int, Int) => Int): Int = {
    if (input.length == 0) {
      return 0
    }
    input.reduce(binaryReducer)
  }

  /**
    * Adds two integers but throws on integer overflow/underflow
    */
  def sumInts(a: Int, b: Int): Int = {
    addExact(a, b)
  }
}
