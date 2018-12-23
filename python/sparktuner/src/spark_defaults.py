"""This module describes all Spark parameters and their defaults"""

import csv
import os

# TODO: use immutables

# Required parameters for spark-submit when running Spark JARs
SPARK_REQUIRED_DIRECT_PARAM = ["name", "class", "master", "deploy-mode"]

SPARK_DIRECT_PARAM = {
    "name": "spark_program",
    "class": "main_class",
    "master": "local[*]",
    "deploy-mode": "client",
    "driver-memory": 10485760,
    "executor-memory": 10485760,
    "executor-cores": 2
}

SPARK_DIRECT_PARAM_ARGS = {
    "name": (str, "Program name"),
    "class": (str, "Fully qualified main class name"),
    "master": (str, "Spark master type: local/yarn/mesos"),
    "deploy-mode": (str, "Deployment mode: client/cluster"),
    "driver-memory": (int, "Amount of driver memory"),
    "executor-memory": (int, "Amount of executor memory"),
    "executor-cores": (int, "Number of executor cores")
}

# Conf whitelist

SPARK_ALLOWED_CONF_PARAM = {
    "max-executors": "spark.dynamicAllocation.maxExecutors",
    "spark-parallelism": "spark.default.parallelism",
    "spark-partitions": "spark.sql.shuffle.partitions"
}

SPARK_CONF_PARAM = {
    "spark.dynamicAllocation.enabled": True,
    "spark.dynamicAllocation.maxExecutors": 2,
    "spark.default.parallelism": 10,
    "spark.sql.shuffle.partitions": 10,
    "spark.eventLog.dir": "file:///tmp/spark-events",
    "spark.eventLog.enabled": True,
    "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version": 2,
    "spark.shuffle.service.enabled": True,
    "spark.sql.autoBroadcastJoinThreshold": 10485760,
    "spark.yarn.maxAppAttempts": 1
}

# Parse the CSV file containing Spark conf param names, defaults, and meaning.
# The result is placed into a dictionary that maps parameter name to a tuple
# containing the parameter's Spark default value, and the meaning.
SPARK_CONF_PARAM_DICT = {}
# This indirection helps run these scripts from any path
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
conf_file = os.path.join(dir_path, "spark_2_4_params.csv")
with open(conf_file, 'rb') as csv_file:
    param_reader = csv.reader(csv_file)
    next(param_reader)
    for row in param_reader:
        param_name = row[0].strip
        if param_name in SPARK_CONF_PARAM:
            SPARK_CONF_PARAM_DICT[param_name] = (row[1].strip, row[2].strip)
