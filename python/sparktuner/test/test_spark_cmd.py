"""This module tests spark-submit command formation"""

import unittest
from chainmap import ChainMap
from args import ArgumentParser
from spark_cmd import SparkSubmitCmd
from spark_defaults import SPARK_REQUIRED_DIRECT_PARAM, \
    SPARK_ALLOWED_CONF_PARAM


class SparkSubmitCmdTest(unittest.TestCase):
    DEFAULT_PATH = "path/to"

    def setUp(self):
        self.parser = ArgumentParser()
        self.cmder = SparkSubmitCmd()

    @staticmethod
    def make_required_args_dict():
        args = {"path": SparkSubmitCmdTest.DEFAULT_PATH}
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            args[ArgumentParser.to_flag(param)] = "test_value"
        return args

    @staticmethod
    def parse_spark_cmd(spark_cmd):
        """
        Extracts the Spark direct and conf parameters from a spark-submit
        command.
        :param spark_cmd: spark-submit command
        :return: tuple of two dict: first containing direct, the second conf
        """
        cmd = spark_cmd.replace(SparkSubmitCmd.SPARK_SUBMIT_PATH, "")
        cmd = cmd[:cmd.find(SparkSubmitCmdTest.DEFAULT_PATH)].strip()
        direct_param = {}
        conf_param = {}
        for line in cmd.split("--"):
            if not line:
                continue
            line = line.strip()
            if line.startswith("conf"):
                res = line.replace("conf", "").strip().split("=")
                conf_param[res[0]] = res[1]
            else:
                res = line.split(" ")
                direct_param[res[0]] = res[1]
        return direct_param, conf_param

    def test_merge_param_with_required_flags_only(self):
        args = self.make_required_args_dict()
        (direct, conf) = self.cmder.merge_params(args, {})
        self.assertTrue(len(conf) == 0)
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            self.assertTrue(param in direct)
            self.assertEqual(direct[param], "test_value")
        # no conf param in direct
        result_dict = {k for k in direct if k in SPARK_ALLOWED_CONF_PARAM}
        self.assertTrue(len(result_dict) == 0)

    def test_merge_param_with_both_flags(self):
        args = self.make_required_args_dict()
        for param in SPARK_ALLOWED_CONF_PARAM:
            args[param] = (2, 2)
        (direct, conf) = self.cmder.merge_params(args, {})
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            self.assertTrue(param in direct)
            self.assertEqual(direct[param], "test_value")
        for param in SPARK_ALLOWED_CONF_PARAM:
            self.assertTrue(SPARK_ALLOWED_CONF_PARAM[param] in conf)
            self.assertEqual(conf[SPARK_ALLOWED_CONF_PARAM[param]], (2, 2))

    def test_merge_param_with_tuner_cfg(self):
        args = self.make_required_args_dict()
        tuner_cfg = {}
        for param in SPARK_ALLOWED_CONF_PARAM:
            args[param] = (2, 2)
            tuner_cfg[SPARK_ALLOWED_CONF_PARAM[param]] = (3, 3)
        (direct, conf) = self.cmder.merge_params(args, tuner_cfg)
        for param in SPARK_ALLOWED_CONF_PARAM:
            self.assertTrue(SPARK_ALLOWED_CONF_PARAM[param] in conf)
            self.assertEqual(conf[SPARK_ALLOWED_CONF_PARAM[param]], (3, 3))

    def test_merge_param_with_defaults(self):
        args = self.make_required_args_dict()
        tuner_cfg = {"spark.dynamicAllocation.maxExecutors": 23}
        direct_default = {"executor-cores": 111, "driver-memory": 12000}
        conf_default = {"spark.eventLog.dir": "file:///tmp/spark-events",
                        "spark.yarn.maxAppAttempts": 123}
        spark_cmd = SparkSubmitCmd(direct_default, conf_default)
        (direct, conf) = spark_cmd.merge_params(args, tuner_cfg)
        expected_conf_dict = dict(ChainMap(
            {"spark.dynamicAllocation.maxExecutors": 23},
            conf_default))
        self.assertEqual(conf, expected_conf_dict)
        self.assertTrue("executor-cores" in direct)
        self.assertEqual(direct["executor-cores"], 111)
        self.assertTrue("driver-memory" in direct)
        self.assertEqual(direct["driver-memory"], 12000)

    def test_make_cmd_no_prog_args(self):
        args = self.make_required_args_dict()
        tuner_cfg = {"spark.default.parallelism": 231}
        direct_default = {"executor-cores": 111, "driver-memory": 12000}
        conf_default = {"spark.dynamicAllocation.maxExecutors": 23}
        spark_cmd = SparkSubmitCmd(direct_default, conf_default)
        cmd = spark_cmd.make_cmd(args, tuner_cfg).strip()
        self.assertTrue(cmd.startswith(SparkSubmitCmd.SPARK_SUBMIT_PATH))
        self.assertTrue(cmd.endswith(SparkSubmitCmdTest.DEFAULT_PATH))
        (actual_direct, actual_conf) = self.parse_spark_cmd(cmd)
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            self.assertTrue(param in actual_direct)
        self.assertTrue("executor-cores" in actual_direct)
        self.assertEqual(actual_direct["executor-cores"], "111")
        self.assertTrue("driver-memory" in actual_direct)
        self.assertEqual(actual_direct["driver-memory"], "12000")
        expected_conf = {"spark.default.parallelism": "231",
                         "spark.dynamicAllocation.maxExecutors": "23"}
        self.assertEqual(actual_conf, expected_conf)

    def test_make_cmd_with_prog_args(self):
        pass
