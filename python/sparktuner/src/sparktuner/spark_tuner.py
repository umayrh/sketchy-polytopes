"""
Main module that is used for running a Spark application with different
configurable parameters, possibly a given range instead of a point value.
"""
import os
import logging
from args import ArgumentParser
from opentuner import (MeasurementInterface, Result, argparsers)
from opentuner.search.manipulator import (ConfigurationManipulator,
                                          IntegerParameter,
                                          BooleanParameter)
from spark_param import SparkParamType, \
    SparkIntType, SparkMemoryType, SparkBooleanType
from spark_cmd import SparkSubmitCmd
from tuner_cfg import MinimizeTimeAndResource

log = logging.getLogger(__name__)


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
        # Extract ranged SparkParamType objects from arguments
        param_dict = SparkParamType.get_param_map(
            vars(self.args), lambda p: p.is_range_val)
        log.info(str(param_dict))

        for flag, param in param_dict.items():
            log.info("Adding flag: " + str(flag) + ", " + str(type(param)))
            if isinstance(param, SparkIntType):
                tuner_param = IntegerParameter(
                    flag,
                    param.get_range_start(),
                    param.get_range_end())
            elif isinstance(param, SparkMemoryType):
                tuner_param = IntegerParameter(
                    flag,
                    param.get_range_start(),
                    param.get_range_end())
            elif isinstance(param, SparkBooleanType):
                tuner_param = BooleanParameter(flag)
            else:
                raise SparkTunerConfigError(
                    ValueError, "Invalid type for ConfigurationManipulator")
            log.info("Added config: " + str(type(tuner_param)) +
                     ": legal range " + str(tuner_param.legal_range(None)) +
                     ", search space size " +
                     str(tuner_param.search_space_size()))
            manipulator.add_parameter(tuner_param)
        return manipulator

    def run(self, desired_result, input, limit):
        """
        Runs a program for given configuration and returns the result
        """
        arg_dict = vars(self.args)
        jar_path = arg_dict.get(ArgumentParser.JAR_PATH_ARG_NAME)
        program_conf = arg_dict.get(ArgumentParser.PROGRAM_CONF_ARG_NAME, "")
        fixed_args = arg_dict.get(ArgumentParser.FIXED_SPARK_PARAM, "")
        # This config dict is keyed by the program flag. See
        # manipulator().
        cfg_data = desired_result.configuration.data
        log.info("Config dict: " + str(cfg_data))
        # Extract all SparkParamType objects from map
        param_dict = SparkParamType.get_param_map(arg_dict)
        # Seems strange making a SparkParamType out of a value but it helps
        # maintain a consistent interface to SparkSubmitCmd
        tuner_cfg = {flag: param_dict[flag].make_param(
            cfg_data[flag]) for flag in cfg_data}

        # TODO figure out appropriate defaults
        spark_submit = SparkSubmitCmd({}, {}, fixed_args)
        # make_cmd() expects only dicts of flags to SparkParamType as input
        run_cmd = spark_submit.make_cmd(
            jar_path, program_conf, param_dict, tuner_cfg)
        log.info(run_cmd)

        run_result = self.call_program(run_cmd)
        # TODO differentiate between config errors and errors due to
        # insufficient resources
        assert run_result['returncode'] == 0, run_result['stderr']

        return Result(time=run_result['time'], size=0)

    def save_final_config(self, configuration):
        """Saves optimal configuration, after tuning, to a file"""
        if self.args.out_config is not None:
            file_name = os.path.join(
                self.args.output_config,
                self.args.name + "_final_config.json")
            log.info("Writing final config", file_name, configuration.data)
            self.manipulator().save_to_file(configuration.data, file_name)

    def objective(self):
        # TODO: add a flag to allow using a different objective function
        return MinimizeTimeAndResource()

    @staticmethod
    def make_parser():
        """Creates and returns the default parser"""
        return ArgumentParser(parents=argparsers(), add_help=True)


def main():
    SparkConfigTuner.main(SparkConfigTuner.make_parser().parse_args())


if __name__ == '__main__':
    main()
