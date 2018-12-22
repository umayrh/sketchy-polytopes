"""This module handles argument parsing"""

import argparse
from humanfriendly import parse_size
from spark_defaults import SPARK_REQUIRED_DIRECT_PARAM,\
    SPARK_ALLOWED_CONF_PARAM, SPARK_CONF_PARAM_DICT, \
    SPARK_DIRECT_PARAM, SPARK_DIRECT_PARAM_ARGS


class ArgumentParserError(Exception):
    """Represents argument parsing errors"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    JAR_PATH_ARG_NAME = "path"
    PROGRAM_CONF_ARG_NAME = "program_conf"

    @staticmethod
    def cast(str_value):
        """
        Casts an input string, possibly a file size, into an integer.

        :param str_value: an input string, possibly a file size.
        :return: an integer value. If file size, the binary value of the
        human readable input.
        """
        return parse_size(str_value, binary=True)

    @staticmethod
    def type_int_range(arg_value):
        """
        Converts an input string, possibly with file sizes,
        into a range of values.
        # TODO handle cast and range exceptions

        :param arg_value: an input string of comma-separated values,
        possibly file sizes. The expected format for range is:
        start,end, with end (default: start) being optional.
        :return: a tuple containing two integers that represent an
        input range. The range is inclusive-exclusive.
        """
        cast = ArgumentParser.cast
        if len(arg_value) == 0:
            raise ArgumentParserError(IndexError, "empty range arg")
        range_array = str(arg_value).split(",")
        range_len = len(range_array)
        if range_len == 1:
            val = cast(range_array[0])
            return val, val
        elif range_len == 2:
            return cast(range_array[0]), cast(range_array[1])
        else:
            raise ArgumentParserError(IndexError, "invalid range arg")

    @staticmethod
    def make_flag(flag_param):
        """
        Converts a parameter into a flag by prefixing it with "--"
        :param flag_param: a parameter
        :return: parameter prefixed with "--"
        """
        return "--" + flag_param

    @staticmethod
    def from_flag(flag_param):
        """
        Replaces the underscores in argparse flags with hyphens
        :param flag_param: flag name
        :return: flag with underscores replaced with hyphens
        """
        return flag_param.replace('_', '-')

    @staticmethod
    def to_flag(arg_name):
        """
        Replaces the hyphens in command-line args with underscores
        :param arg_name: arg name
        :return: arg_name with hyphens replaced with underscores
        """
        return arg_name.replace('-', '_')

    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)

        # Program information
        self.add_argument(self.make_flag(self.JAR_PATH_ARG_NAME),
                          type=str, required=True,
                          help="Fully qualified JAR path")
        self.add_argument(self.make_flag(self.PROGRAM_CONF_ARG_NAME),
                          type=str, required=False,
                          help="Program-specific parameters")

        for param in SPARK_REQUIRED_DIRECT_PARAM:
            param_flag = self.make_flag(param)
            param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
            self.add_argument(param_flag, type=param_tuple[0], required=True,
                              help=param_tuple[1])

        # Configuration parameters
        _OPTIONAL_DIRECT_PARAM = \
            set(SPARK_DIRECT_PARAM) - set(SPARK_REQUIRED_DIRECT_PARAM)
        for param in _OPTIONAL_DIRECT_PARAM:
            param_flag = self.make_flag(param)
            param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
            self.add_argument(param_flag, type=self.type_int_range,
                              help=param_tuple[1])

        # TODO only handles integer conf for now - generalize
        for param in SPARK_ALLOWED_CONF_PARAM:
            param_flag = self.make_flag(param)
            conf_name = SPARK_ALLOWED_CONF_PARAM[param]
            param_meaning = \
                SPARK_CONF_PARAM_DICT.get(conf_name, ("", conf_name))[1]
            self.add_argument(param_flag, type=self.type_int_range,
                              help=param_meaning)

    def error(self, message):
        """Overwrites default error function"""
        raise ArgumentParserError("ArgumentParserError", message)
