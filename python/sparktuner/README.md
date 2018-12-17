# Spark Tuner

## Setup and build

[Spark]

`gradle build` should install all dependencies (including projects-specific ones in requirements.txt), and run tests.

## Spark parameters

Some commonly used Spark (2.0.2+) parameters:

|Parameter Name|Direct?|Sample Value|
|--------------|-------|------------|
|master|Yes|yarn|
|deploy-mode|Yes|cluster|
|driver-memory|Yes|10G|
|executor-memory|Yes|20G|
|executor-cores|Yes|4|
|spark.default.parallelism|No|100|
|spark.dynamicAllocation.enabled|No|true|
|spark.dynamicAllocation.maxExecutors|No|10|
|spark.eventLog.enabled|No|true|
|spark.eventLog.dir|No|hdfs:///var/log/spark/apps|
|spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version|No|2|
|spark.shuffle.service.enabled|No|true|
|spark.sql.autoBroadcastJoinThreshold|No|-1|
|spark.sql.shuffle.partitions|No|100|
|spark.yarn.maxAppAttempts|No|1|
|spark.memory.fraction|No|0.6|
|spark.memory.storageFraction|No|0.5|

For all available configurations, see [this](https://spark.apache.org/docs/2.4.0/configuration.html).

## Creating an OpenTuner configuration

Implement [MeasurementInterface](https://github.com/jansel/opentuner/blob/c9db469889b9b504d1f7affe2374b2750adafe88/opentuner/measurement/interface.py),
three methods in particular:
* `manipulator`: defines the search space across configuration parameters
* `run`: runs a program for given configuration and returns the result
* `save_final_config`: saves optimal configuration, after tuning, to a file

A fourth, `objective`, should be implemented if an objective function other than the default
[MinimizeTime](https://github.com/jansel/opentuner/blob/c9db469889b9b504d1f7affe2374b2750adafe88/opentuner/search/objective.py)
is desired.

## References

### Auto-tuning

* [OpenTuner](http://opentuner.org)

### Spark tuning guides

* [Tuning Spark](https://spark.apache.org/docs/latest/tuning.html)
* [Spark Performance Tuning: A Checklist](https://zerogravitylabs.ca/spark-performance-tuning-checklist/)

### Spark tuning research

* Using Spark to Tune Spark [link](https://www.slideshare.net/databricks/using-apache-spark-to-tune-spark-with-shivnath-babu-and-adrian-popescu)
* A Novel Method for Tuning Configuration Parameters of Spark Based on Machine Learning [link](https://www.computer.org/csdl/proceedings/hpcc/2016/4297/00/07828429.pdf)
* A Methodology for Spark Parameter Tuning [link](delab.csd.auth.gr/papers/BDR2017gt.pdf)

## TODO

* Ideally, all tuning run details are published to a central location as a time-series.
This would help pool run data, and track of significant outcome changes (e.g. as a result
of a code change).  
* The default parameters should be read from a file instead of being hard-coded. All
parameters should be merged into a final map.