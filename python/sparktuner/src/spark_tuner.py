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

    def manipulator(self):
        """
        Defines the search space across configuration parameters
        """
        manipulator = ConfigurationManipulator()
        param_dict = ArgumentParser.get_conf_parameters(self.args)
        for param, desc in param_dict.items():
            # TODO
            manipulator.add_parameter(
                IntegerParameter(param, 1, 10))
        return manipulator

    def run(self, desired_result, input, limit):
        """
        Runs a program for given configuration and returns the result
        """
        # cfg = desired_result.configuration.data

        # build command
        run_cmd = ""

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
    def make_parser():
        """Creates and returns the default parser"""
        return ArgumentParser(parents=argparsers())


if __name__ == '__main__':
    SparkConfigTuner.main(SparkConfigTuner.make_parser().parse_args())
