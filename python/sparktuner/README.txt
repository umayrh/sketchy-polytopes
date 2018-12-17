Spark Tuner
===========

Setup and build
---------------

[Spark]

``gradle build`` should install all dependencies (including
projects-specific ones in requirements.txt), and run tests.

Spark parameters
----------------

Some commonly used Spark (2.0.2+) parameters:

+-----------------------+-----------------------+-----------------------+
| Parameter Name        | Direct?               | Sample Value          |
+=======================+=======================+=======================+
| master                | Yes                   | yarn                  |
+-----------------------+-----------------------+-----------------------+
| deploy-mode           | Yes                   | cluster               |
+-----------------------+-----------------------+-----------------------+
| driver-memory         | Yes                   | 10G                   |
+-----------------------+-----------------------+-----------------------+
| executor-memory       | Yes                   | 20G                   |
+-----------------------+-----------------------+-----------------------+
| executor-cores        | Yes                   | 4                     |
+-----------------------+-----------------------+-----------------------+
| spark.default.paralle | No                    | 100                   |
| lism                  |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.dynamicAllocati | No                    | true                  |
| on.enabled            |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.dynamicAllocati | No                    | 10                    |
| on.maxExecutors       |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.eventLog.enable | No                    | true                  |
| d                     |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.eventLog.dir    | No                    | hdfs:///var/log/spark |
|                       |                       | /apps                 |
+-----------------------+-----------------------+-----------------------+
| spark.hadoop.mapreduc | No                    | 2                     |
| e.fileoutputcommitter |                       |                       |
| .algorithm.version    |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.shuffle.service | No                    | true                  |
| .enabled              |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.sql.autoBroadca | No                    | -1                    |
| stJoinThreshold       |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.sql.shuffle.par | No                    | 100                   |
| titions               |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.yarn.maxAppAtte | No                    | 1                     |
| mpts                  |                       |                       |
+-----------------------+-----------------------+-----------------------+
| spark.memory.fraction | No                    | 0.6                   |
+-----------------------+-----------------------+-----------------------+
| spark.memory.storageF | No                    | 0.5                   |
| raction               |                       |                       |
+-----------------------+-----------------------+-----------------------+

For all available configurations, see
`this <https://spark.apache.org/docs/2.4.0/configuration.html>`__.

Creating an OpenTuner configuration
-----------------------------------

Implement
`MeasurementInterface <https://github.com/jansel/opentuner/blob/c9db469889b9b504d1f7affe2374b2750adafe88/opentuner/measurement/interface.py>`__,
three methods in particular: \* ``manipulator``: defines the search
space across configuration parameters \* ``run``: runs a program for
given configuration and returns the result \* ``save_final_config``:
saves optimal configuration, after tuning, to a file

A fourth, ``objective``, should be implemented if an objective function
other than the default
`MinimizeTime <https://github.com/jansel/opentuner/blob/c9db469889b9b504d1f7affe2374b2750adafe88/opentuner/search/objective.py>`__
is desired.

References
----------

Auto-tuning
~~~~~~~~~~~

-  `OpenTuner <http://opentuner.org>`__

Spark tuning guides
~~~~~~~~~~~~~~~~~~~

-  `Tuning Spark <https://spark.apache.org/docs/latest/tuning.html>`__
-  `Spark Performance Tuning: A
   Checklist <https://zerogravitylabs.ca/spark-performance-tuning-checklist/>`__

Spark tuning research
~~~~~~~~~~~~~~~~~~~~~

-  Using Spark to Tune Spark
   `link <https://www.slideshare.net/databricks/using-apache-spark-to-tune-spark-with-shivnath-babu-and-adrian-popescu>`__
-  A Novel Method for Tuning Configuration Parameters of Spark Based on
   Machine Learning
   `link <https://www.computer.org/csdl/proceedings/hpcc/2016/4297/00/07828429.pdf>`__
-  A Methodology for Spark Parameter Tuning
   `link <delab.csd.auth.gr/papers/BDR2017gt.pdf>`__

TODO
----

-  Ideally, all tuning run details are published to a central location
   as a time-series. This would help pool run data, and track of
   significant outcome changes (e.g. as a result of a code change).
-  The default parameters should be read from a file instead of being
   hard-coded. All parameters should be merged into a final map.
