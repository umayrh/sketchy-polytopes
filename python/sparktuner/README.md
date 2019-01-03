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

For commonly used configurations, see 
[this](https://spark.apache.org/docs/2.4.0/configuration.html).

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

### Spark 

* See [here](../../sparkScala/SPARK.md).

## TODO

* Urgent
  * Fix sparktuner --help
  * Experiment with `sort` using different config
    * `build/deployable/bin/sparktuner --no-dups --name sartre_spark_sortre --path ../../sparkScala/sort/build/libs/sort-0.1-all.jar --deploy_mode client --master "local[*]" --class com.umayrh.sort.Main --spark_parallelism "1,10" --program_conf "10000 /tmp/sparktuner_sort"`
    * `build/deployable/bin/sparktuner --no-dups --name sartre_spark_sortre --path ../../sparkScala/sort/build/libs/sort-0.1-all.jar --deploy_mode client --master "local[*]" --class com.umayrh.sort.Main --executor_memory "50mb,1gb" --program_conf "10000 /tmp/sparktuner_sort"`
    * `build/deployable/bin/sparktuner --no-dups --name sartre_spark_sortre --path ../../sparkScala/sort/build/libs/sort-0.1-all.jar --deploy_mode client --master "local[*]" --class com.umayrh.sort.Main --driver_memory "1GB,6GB" --program_conf "1000000 /tmp/sparktuner_sort"`
      * There's an issue somewhere here: somehow invalid values (< specified min value) 
      are generated. Maybe because the search space is small.
      ```
        [     1s]    INFO sparktuner.spark_tuner: Setting value: 3, unscaled: 3221225472
        [     1s]    INFO sparktuner.spark_tuner: get_value: 3221225472
        [     1s]    INFO sparktuner.spark_tuner: get_value: 3221225472
        [     1s]    INFO sparktuner.spark_tuner: Config dict: {'driver_memory': 104857600}
        [     1s]    INFO sparktuner.spark_tuner: /usr/local/Cellar/apache-spark/2.4.0/libexec/bin/spark-submit --deploy-mode client --driver-memory 104857600 --master local[*] --name sartre_spark_sortre --class com.umayrh.sort.Main  ../../sparkScala/sort/build/libs/sort-0.1-all.jar 1000000 /tmp/sparktuner_sort
        ...
      Caused by: java.lang.IllegalArgumentException: System memory 93323264 must be at least 471859200. Please increase heap size using the --driver-memory option or spark.driver.memory in Spark configuration.
        at org.apache.spark.memory.UnifiedMemoryManager$.getMaxMemory(UnifiedMemoryManager.scala:217)
      ```
  * Finish test_spark_tuner
  * Add tests for: ScaledIntegerParameter
  * Replace `type` with `isinstance`

* Next steps
  * Allow JAR parameters to also be configurable.  
  * Implement a new objective function that, over _similar_ values of run-time, minimizes
    resource usage. E.g. if `spark.default.parallelism` ranging from 1 to 10 yields the 
    same runtime in all cases, the optimal configuration value should be 1.
  * `SparkParamType.get_param_map` is called twice, so is `manipulator()`. Redundant.
  * Figure out some DoWhy basics. 
    * In particular, figure out a sensible causal graph for Spark parameters.

* Nice to have
  * Tuner as a service. Opentuner issue [25](https://github.com/jansel/opentuner/issues/25).
  * New objective that optimizes the construction of a causal graph.
  * Ideally, all tuning run details are published to a central location as a time-series.
    This would help pool run data, and track of significant outcome changes (e.g. as a result
    of a code change). Even better if they can be easily visualized (see e.g. 
    [opentuner-visualizer](https://github.com/danula/opentuner-visualizer)).
  * The default parameters should be read from a file instead of being hard-coded. All
    parameters should be merged into a final map.
  * Since Spark parameters are many and jobs can take a while to run, warm starting
    autotuning might be useful.
  * Need to validate all Spark parameters.