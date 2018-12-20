##
# This module describes all Spark parameters and their defaults
##

# Required parameters for spark-submit when running Spark JARs
SPARK_REQUIRED_PARAM = ["name", "main-class", "jar-path",
                        "master", "deploy-mode"]

SPARK_DIRECT_PARAM = {
    "name": "spark_program",
    "main-class": "main_class",
    "jar-path": "jar_path",
    "master": "local[*]",
    "deploy-mode": "client",
    "driver-memory": 10485760,
    "executor-memory": 10485760,
    "executor-cores": 2
}

SPARK_DIRECT_PARAM_ARGS = {
    "name": (str, "Program name"),
    "main-class": (str, "Fully qualified main class name"),
    "jar-path": (str, "Full qualified JAR pathname"),
    "master": (str, "Spark master type: local/yarn/mesos"),
    "deploy-mode": (str, "Deplyment mode: client/cluster"),
    "driver-memory": (int, "Amount of driver memory"),
    "executor-memory": (int, "Amount of executor memory"),
    "executor-cores": (int, "Number of executor cores")
}

# Conf whitelist

SPARK_ALLOWED_CONF_PARAM = {
    "max-executors": "spark.dynamicAllocation.maxExecutors",
    "parallelism": "spark.default.parallelism",
    "partitions": "spark.sql.shuffle.partitions"
}

SPARK_CONF_PARAM = {
    "spark.dynamicAllocation.enabled": True,
    "spark.dynamicAllocation.maxExecutors": 2,
    "spark.default.parallelism": 10,
    "spark.sql.shuffle.partitions": 10,
    "spark.eventLog.dir": "/tmp/log/spark/apps",
    "spark.eventLog.enabled": True,
    "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version": 2,
    "spark.shuffle.service.enabled": True,
    "spark.sql.autoBroadcastJoinThreshold": 10485760,
    "spark.yarn.maxAppAttempts": 1
}
