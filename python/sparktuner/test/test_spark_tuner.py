"""Tests spark-tuner module"""

import unittest
import os
import shutil
import tempfile
from sparktuner.spark_tuner import SparkConfigTuner


class SparkTunerTest(unittest.TestCase):
    """
    Note: the JAR used here is a slim, unshaded file, and
    so should not be used for full functionality.
    """
    JAR_NAME = "sort-0.1.jar"

    @staticmethod
    def get_tempfile_name():
        return os.path.join(tempfile.gettempdir(),
                            next(tempfile._get_candidate_names()))

    @staticmethod
    def make_args(temp_file):
        program_conf = "10 " + temp_file
        dir_path = os.path.dirname(os.path.abspath(__file__))
        jar_path = os.path.join(dir_path, SparkTunerTest.JAR_NAME)
        return ["--no-dups",
                "--test-limit", "1",
                "--name", "sorter",
                "--class", "com.umayrh.sort.Main",
                "--master", "\"local[*]\"",
                "--deploy_mode", "client",
                "--path", jar_path,
                "--program_conf", program_conf]

    def setUp(self):
        self.temp_file = SparkTunerTest.get_tempfile_name()

    def tearDown(self):
        if os.path.exists(self.temp_file):
            shutil.rmtree(self.temp_file)

    def test_help(self):
        try:
            SparkConfigTuner.make_parser().print_help()
        except Exception:
            self.fail()

    @unittest.skipIf("SPARK_HOME" not in os.environ,
                     "SPARK_HOME environment variable not set.")
    def test_spark_tuner_main(self):
        arg_list = SparkTunerTest.make_args(self.temp_file)
        args = SparkConfigTuner.make_parser().parse_args(arg_list)
        SparkConfigTuner.main(args)

        if not os.path.exists(self.temp_file):
            self.fail("Expected output file")

    def test_no_config_args(self):
        """
        build/deployable/bin/sparktuner --name blah --path test/sort-0.1.jar
        --deploy_mode client --master "local[*]" --class Main
        """
        pass

    def test_no_bad_class_name(self):
        """
        build/deployable/bin/sparktuner --name blah --path test/sort-0.1.jar
        --deploy_mode client --master "local[*]" --class Main
        """
        pass
