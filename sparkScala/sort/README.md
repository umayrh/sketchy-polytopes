# Sort

## Intro

A simple utility for generating, sorting and writing a given
number of uniformly random doubles. The utility uses Spark Mllib's 
RandomRDD API. The simple alternative is:

```
  val randNums = spark.sparkContext
    .parallelize(
      Seq.fill(args(0).toInt)(Random.nextInt),
      partitions
  )
  .toDF(COL_NAME)
```

Nonetheless, it will cause:

```
  Exception in thread "main" java.lang.OutOfMemoryError: GC overhead limit exceeded
      at scala.collection.mutable.ListBuffer.$plus$eq(ListBuffer.scala:174)
```

Sample usage:

```
spark-submit \
    --name "sorter" \ 
    --class com.umayrh.sort.Main \ 
    --master "local[*]" \
    --deploy-mode client \
    --executor-memory 1g \
    build/libs/sort-0.1.jar \
    100000000 /tmp/maintestout
```

The output CSV file should be inside the `/tmp/maintestout` directory.

## References

* [Random data generation](https://spark.apache.org/docs/2.3.0/mllib-statistics.html#random-data-generation)
