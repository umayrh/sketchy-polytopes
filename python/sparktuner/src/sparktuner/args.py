"""This module handles argument parsing"""

import argparse
from chainmap import ChainMap
from spark_default_param import REQUIRED_FLAGS, \
    FLAG_TO_CONF_PARAM, FLAG_TO_DIRECT_PARAM


class ArgumentParserError(Exception):
    """Represents argument parsing errors"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    """
    Sets up arguments and overrides default ArgumentParser error
    """
    JAR_PATH_ARG_NAME = "path"
    PROGRAM_CONF_ARG_NAME = "program_conf"
    CONFIG_OUTPUT_PATH = "out_config"
    PROGRAM_FLAGS = ChainMap(FLAG_TO_DIRECT_PARAM, FLAG_TO_CONF_PARAM)

    @staticmethod
    def make_flag(param):
        return "--" + param

    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)

        # Program information
        self.add_argument(ArgumentParser.make_flag(self.JAR_PATH_ARG_NAME),
                          type=str, required=True,
                          help="Fully qualified JAR path")
        self.add_argument(ArgumentParser.make_flag(self.PROGRAM_CONF_ARG_NAME),
                          type=str, required=False,
                          help="Program-specific parameters")
        self.add_argument(ArgumentParser.make_flag(self.CONFIG_OUTPUT_PATH),
                          type=str, required=False,
                          help="Output config storage location")

        for param in ArgumentParser.PROGRAM_FLAGS:
            required = True if param in REQUIRED_FLAGS else False
            param_obj = ArgumentParser.PROGRAM_FLAGS[param]
            param_flag = ArgumentParser.make_flag(param)
            self.add_argument(param_flag, type=param_obj.make_param_from_str,
                              required=required, help=param_obj.desc)

    def error(self, message):
        """Overwrites default error function"""
        raise ArgumentParserError("ArgumentParserError", message)