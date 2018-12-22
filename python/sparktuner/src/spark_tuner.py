"""
Main module that is used for running a Spark application with different
configurable parameters, possibly a given range instead of a point value.
"""
# import adddeps  # fix sys.path

import logging
from opentuner import (MeasurementInterface, Result, argparsers)
from opentuner.search.manipulator import (ConfigurationManipulator,
                                          IntegerParameter)
from args import ArgumentParser

log = logging.getLogger(__name__)


class SparkConfigTuner(MeasurementInterface):
    """
    OpenTuner implementation for Spark configuration.
    Extends MeasurementInterface.
    """
    SPARK_SUBMIT_PATH = "/usr/local/bin/spark-submit"

    def manipulator(self):
        """
        Defines the search space across configuration parameters
        """
        manipulator = ConfigurationManipulator()
        manipulator.add_parameter(
            IntegerParameter('blockSize', 1, 10))
        return manipulator

    def run(self, desired_result, input, limit):
        """
        Runs a program for given configuration and returns the result
        """
        # cfg = desired_result.configuration.data

        # build command
        run_cmd = SparkConfigTuner.SPARK_SUBMIT_PATH

        run_result = self.call_program(run_cmd)
        assert run_result['returncode'] == 0

        return Result(time=run_result['time'])

    def save_final_config(self, configuration):
        """Saves optimal configuration, after tuning, to a file"""
        print "??? written to ???_final_config.json:",\
            configuration.data
        self.manipulator().save_to_file(configuration.data,
                                        '???_final_config.json')

    @staticmethod
    def get_spark_default_configs():
        """Returns a space-delimited string of default
        Spark config parameters"""
        configs = " "
        configs += "--conf spark.dynamicAllocation.enabled=true "
        configs += "--conf spark.dynamicAllocation.maxExecutors=15 "
        configs += "--conf spark.eventLog.dir=hdfs:///var/log/spark/apps "
        configs += "--conf spark.eventLog.enabled=True "
        configs += "--conf spark.hadoop.mapreduce." \
                   "fileoutputcommitter.algorithm.version=2 "
        configs += "--conf spark.shuffle.service.enabled=true "
        configs += "--conf spark.sql.autoBroadcastJoinThreshold=-1 "
        configs += "--conf spark.yarn.maxAppAttempts=1 "
        return configs

    @staticmethod
    def make_parser():
        """Creates and returns the default parser"""
        return ArgumentParser(parents=argparsers())


if __name__ == '__main__':
    SparkConfigTuner.main(SparkConfigTuner.make_parser().parse_args())
