package com.umayrh.testing

import java.lang.Math.addExact
import java.lang.ArithmeticException

/**
  * A class that offers a more considered implementation of a reducer
  */
object ReducerRedux {
    /**
      * Aggregates an input sequence of integers
      * 
      */
    def reduceSeq(input: Seq[Int], binaryReducer: (Long, Long) => Long): Int = {
        if (input.length == 0) {
            return 0
        }
        val result = input.map(a => a.toLong).reduce(binaryReducer)
        if (result > Int.MaxValue || result < Int.MinValue) {
            throw new ArithmeticException()
        }
        result.toInt
    }

    /**
      * Adds two integers but throws on integer overflow/underflow 
      */
    def sumLongs(a: Long, b: Long): Long = {
        addExact(a, b)
    }
}
