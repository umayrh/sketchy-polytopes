"""
Main module that is used for running a Spark application with different
configurable parameters, possibly a given range instead of a point value.
"""
# import adddeps  # fix sys.path

import logging
from opentuner import (MeasurementInterface, Result, argparsers)
from opentuner.search.manipulator import (ConfigurationManipulator,
                                          IntegerParameter,
                                          ScaledNumericParameter,
                                          BooleanParameter)
from args import ArgumentParser
from spark_param import SparkParamType, \
    SparkIntType, SparkMemoryType, SparkBooleanType
from spark_cmd import SparkSubmitCmd

log = logging.getLogger(__name__)


class ScaledIntegerParameter(ScaledNumericParameter, IntegerParameter):
    """
    An integer parameter that is searched on a
    linear scale after normalization, but stored without scaling
    """
    def __init__(self, name, min_value, max_value, scale, **kwargs):
        kwargs['value_type'] = int
        super(ScaledNumericParameter, self).__init__(
            name, min_value, max_value, **kwargs)
        assert scale > 0
        self.scale = float(scale)

    def _scale(self, v):
        return round(v / self.scale)

    def _unscale(self, v):
        return round(v * self.scale)

    def legal_range(self, config):
        return self._scale(self.min_value), self._scale(self.max_value)

    def search_space_size(self):
        return self._scale(
            super(ScaledIntegerParameter, self).search_space_size())


class SparkTunerConfigError(Exception):
    """Represents errors in OpenTuner configuration setup"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


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
        param_dict = SparkParamType.get_range_param_map(vars(self.args))
        for param in param_dict.values():
            spark_name = param.spark_name
            param_type = type(param)
            tuner_param = None
            if param_type is SparkIntType:
                tuner_param = IntegerParameter(
                    spark_name,
                    param.get_range_start(),
                    param.get_range_end)
            elif param_type is SparkMemoryType:
                tuner_param = ScaledIntegerParameter(
                    spark_name,
                    param.get_range_start(),
                    param.get_range_end,
                    param.get_scale)
            elif param_type is SparkBooleanType:
                tuner_param = BooleanParameter(spark_name)
            else:
                raise SparkTunerConfigError(
                    ValueError, "Invalid type for ConfigurationManipulator")
            manipulator.add_parameter(tuner_param)
        return manipulator

    def run(self, desired_result, input, limit):
        """
        Runs a program for given configuration and returns the result
        """
        arg_dict = vars(self.args)
        cfg_data = desired_result.configuration.data
        param_dict = SparkParamType.get_range_param_map(arg_dict)
        # Seems strange making a SparkParamType out of a value but it helps
        # maintain a consistent interface to SparkSubmitCmd
        tuner_cfg = {k: param_dict[k].make_param(
            cfg_data[param_dict[k].spark_name]) for k in param_dict}

        run_cmd = SparkSubmitCmd.make_cmd(arg_dict, tuner_cfg)

        run_result = self.call_program(run_cmd)
        assert run_result['returncode'] == 0

        return Result(time=run_result['time'])

    def save_final_config(self, configuration):
        """Saves optimal configuration, after tuning, to a file"""
        program_name = self.args.get("name", "spark_program")
        file_name = program_name + "_final_config.json"
        log.info("Writing final config", file_name, configuration.data)
        self.manipulator().save_to_file(configuration.data, file_name)

    @staticmethod
    def make_parser():
        """Creates and returns the default parser"""
        return ArgumentParser(parents=argparsers())


if __name__ == '__main__':
    SparkConfigTuner.main(SparkConfigTuner.make_parser().parse_args())
