"""This module handles argument parsing"""
import argparse
import opentuner
from humanfriendly import parse_size
from spark_defaults import SPARK_REQUIRED_PARAM, SPARK_ALLOWED_CONF_PARAM, \
    SPARK_DIRECT_PARAM, SPARK_DIRECT_PARAM_ARGS, \
    SPARK_CONF_PARAM_DICT

parser = argparse.ArgumentParser(parents=opentuner.argparsers())


def cast(str_value):
    """
    Cast an input string, possibly a file size, into an integer.

    :param str_value: an input string, possibly a file size.
    :return: an integer value. If file size, the binary value of the
    human readable input.
    """
    return parse_size(str_value, binary=True)


def type_int_range(arg_value):
    """
    Convert an input string, possibly with file sizes, into a range of values.

    :param arg_value: an input string of comma-separated values, possibly file
    sizes. The expected format for range is: start,end,step_size, with end
    (default: start + 1) and step_size (default: 1) are optional.
    :return: a range object representing input range. The range is
    inclusive-exclusive, with a default step size of 1.
    """
    range_array = str(arg_value).split(",")
    print("arg_value " + arg_value + ", " +
          range_array + ", " + len(range_array))
    # TODO handle cast and range exceptions
    length_switcher = {
        1: range(cast(range_array[0]), cast(range_array[0]) + 1),
        2: range(cast(range_array[0]), cast(range_array[1])),
        3: range(cast(range_array[0]), cast(range_array[1]),
                 cast(range_array[2])),
    }
    return length_switcher.get(len(range_array),
                               lambda: "Invalid range argument")


def make_flag(flag_param):
    """
    Convert a parameter into a flag by prefixing it with "--"
    :param flag_param: a parameter
    :return: parameter prefixed with "--"
    """
    return "--" + flag_param


# Program information

for param in SPARK_REQUIRED_PARAM:
    param_flag = make_flag(param)
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    print("adding " + param_flag)
    parser.add_argument(param_flag, type=param_tuple[0], required=True,
                        help=param_tuple[1])

# Configuration parameters

_OPTIONAL_DIRECT_PARAM = set(SPARK_DIRECT_PARAM) - set(SPARK_REQUIRED_PARAM)
for param in _OPTIONAL_DIRECT_PARAM:
    param_flag = make_flag(param)
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    print("adding " + param_flag)
    parser.add_argument(param_flag, type=type_int_range, help=param_tuple[1])

# TODO only handles integer conf for now - generalize
for param in SPARK_ALLOWED_CONF_PARAM:
    param_flag = make_flag(param)
    conf_name = SPARK_ALLOWED_CONF_PARAM[param]
    param_meaning = SPARK_CONF_PARAM_DICT.get(conf_name, ("", conf_name))[1]
    print("adding " + param_flag)
    parser.add_argument(param_flag, type=type_int_range, help=param_meaning)
