"""This module handles argument parsing"""
import logging
import argparse
import opentuner
from humanfriendly import parse_size
from spark_defaults import SPARK_REQUIRED_PARAM, SPARK_ALLOWED_CONF_PARAM, \
    SPARK_DIRECT_PARAM, SPARK_DIRECT_PARAM_ARGS, \
    SPARK_CONF_PARAM_DICT


class ArgumentParserError(Exception):
    """Represents argument parsing errors"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    """Overwrites default argparse error function"""
    def error(self, message):
        raise ArgumentParserError("ArgumentParserError", message)


parser = ArgumentParser(parents=opentuner.argparsers())
log = logging.getLogger(__name__)


def cast(str_value):
    """
    Casts an input string, possibly a file size, into an integer.

    :param str_value: an input string, possibly a file size.
    :return: an integer value. If file size, the binary value of the
    human readable input.
    """
    return parse_size(str_value, binary=True)


def type_int_range(arg_value):
    """
    Converts an input string, possibly with file sizes, into a range of values.
    # TODO handle cast and range exceptions

    :param arg_value: an input string of comma-separated values, possibly file
    sizes. The expected format for range is: start,end,step_size, with end
    (default: start + 1) and step_size (default: 1) are optional.
    :return: a range object representing input range. The range is
    inclusive-exclusive, with a default step size of 1.
    """
    if len(arg_value) == 0:
        raise IndexError
    range_array = str(arg_value).split(",")
    range_len = len(range_array)
    if range_len == 1:
        val = cast(range_array[0])
        return range(val, val + 1)
    elif range_len == 2:
        return range(cast(range_array[0]), cast(range_array[1]))
    elif range_len == 3:
        return range(cast(range_array[0]), cast(range_array[1]),
                     cast(range_array[2]))
    else:
        raise IndexError


def make_flag(flag_param):
    """
    Converts a parameter into a flag by prefixing it with "--"
    :param flag_param: a parameter
    :return: parameter prefixed with "--"
    """
    return "--" + flag_param


def from_flag(flag_param):
    """
    Replaces the underscores in argparse flags with hyphens
    :param flag_param: flag name
    :return: flag with underscores replaced with hyphens
    """
    return flag_param.replace('_', '-')


def to_flag(arg_name):
    """
    Replaces the hyphens in command-line args with underscores
    :param arg_name: arg name
    :return: arg_name with hyphens replaced with underscores
    """
    return arg_name.replace('-', '_')


# Program information

for param in SPARK_REQUIRED_PARAM:
    param_flag = make_flag(param)
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    parser.add_argument(param_flag, type=param_tuple[0], required=True,
                        help=param_tuple[1])

# Configuration parameters

_OPTIONAL_DIRECT_PARAM = set(SPARK_DIRECT_PARAM) - set(SPARK_REQUIRED_PARAM)
for param in _OPTIONAL_DIRECT_PARAM:
    param_flag = make_flag(param)
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    parser.add_argument(param_flag, type=type_int_range, help=param_tuple[1])

# TODO only handles integer conf for now - generalize
for param in SPARK_ALLOWED_CONF_PARAM:
    param_flag = make_flag(param)
    conf_name = SPARK_ALLOWED_CONF_PARAM[param]
    param_meaning = SPARK_CONF_PARAM_DICT.get(conf_name, ("", conf_name))[1]
    parser.add_argument(param_flag, type=type_int_range, help=param_meaning)
