package com.umayrh.testing

import java.lang.Math.addExact

/**
  * A class encapsulating
  */
object Main {
    /**
      * Aggregates an input sequence of integers
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
