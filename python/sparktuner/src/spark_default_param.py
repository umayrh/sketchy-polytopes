"""This module describes all Spark parameters and their defaults"""

import csv
import os
from spark_param import SparkStringType, \
    SparkBooleanType, SparkIntType, SparkMemoryType


class SparkParam(object):
    """
    Holds all Spark parameter objects
    """
    # Parse the CSV file containing Spark conf param names, defaults,
    # and meaning. The result is placed into a dictionary that maps
    # parameter name to a tuple containing the parameter's Spark
    # default value, and the meaning.
    SPARK_CONF_DICT = {}
    # This indirection helps run these scripts from any path
    __path = os.path.abspath(__file__)
    __dir_path = os.path.dirname(__path)
    __conf_file = os.path.join(__dir_path, "spark_2_4_params.csv")
    with open(__conf_file, 'rb') as csv_file:
        param_reader = csv.reader(csv_file)
        next(param_reader)
        for row in param_reader:
            param_name = row[0].strip()
            SPARK_CONF_DICT[param_name] = (row[1].strip(), row[2].strip())
    # shorter alias
    __DICT = SPARK_CONF_DICT

    # All Spark parameters
    NAME = SparkStringType("name", "spark_program", "Program name")
    CLASS = SparkStringType(
        "class", "MainClass", "Fully qualified main class name")
    MASTER = SparkStringType(
        "master", "local[*]", "Spark master type: local/yarn/mesos")
    DEPLOY_MODE = SparkStringType(
        "deploy-mode", "client", "Deployment mode: client/cluster")
    DRIVER_MEM = SparkMemoryType(
        "driver-memory", 10485760, "Amount of driver memory")
    EXECUTOR_MEM = SparkMemoryType(
        "executor-memory", 10485760, "Amount of executor memory")
    EXECUTOR_CORES = SparkIntType(
        "executor-cores", 2, "Number of executor cores")
    MAX_EXECUTORS = SparkIntType(
        "spark.dynamicAllocation.maxExecutors", 2, "")
    PARALLELISM = SparkIntType(
        "spark.default.parallelism", 10,
        __DICT["spark.default.parallelism"])
    PARTITIONS = SparkIntType(
        "spark.sql.shuffle.partitions", 10,
        __DICT["spark.sql.shuffle.partitions"])
    DA_ENABLED = SparkBooleanType(
        "spark.dynamicAllocation.enabled", True,
        __DICT["spark.dynamicAllocation.enabled"])
    EVENTLOG_DIR = SparkStringType(
        "spark.eventLog.dir", "file:///tmp/spark-events",
        __DICT["spark.eventLog.dir"])
    EVENTLOG_ENABLED = SparkBooleanType(
        "spark.eventLog.enabled", True, __DICT["spark.eventLog.enabled"])
    MR_OUTCOM_ALGO = SparkStringType(
        "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2",
        __DICT["spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version"]
    )
    SHUFFLE_ENABLED = SparkBooleanType(
        "spark.shuffle.service.enabled", True,
        __DICT["spark.shuffle.service.enabled"])
    JOIN_THRESH = SparkMemoryType(
        "spark.sql.autoBroadcastJoinThreshold", 10485760,
        __DICT["spark.sql.autoBroadcastJoinThreshold"])
    YARN_MAX_ATTEMPTS = SparkIntType(
        "spark.yarn.maxAppAttempts", 1,
        __DICT["spark.yarn.maxAppAttempts"])


# Required parameters for spark-submit when running Spark JARs

SPARK_REQUIRED_DIRECT_PARAM = ["name", "class", "master", "deploy_mode"]

FLAG_TO_DIRECT_PARAM = {
    "name": SparkParam.NAME,
    "class": SparkParam.CLASS,
    "master": SparkParam.MASTER,
    "deploy_mode": SparkParam.DEPLOY_MODE,
    "driver_memory": SparkParam.DRIVER_MEM,
    "executor_memory": SparkParam.EXECUTOR_MEM,
    "executor_cores": SparkParam.EXECUTOR_CORES
}

# Conf whitelist

# These are allowed in the sense that they may be
# manipulated by OpenTuner for tuning
FLAG_TO_CONF_PARAM = {
    "max_executors": SparkParam.MAX_EXECUTORS,
    "spark_parallelism": SparkParam.PARALLELISM,
    "spark_partitions": SparkParam.PARTITIONS
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
