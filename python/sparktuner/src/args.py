import argparse
import opentuner
from humanfriendly import parse_size
from spark_defaults import SPARK_REQUIRED_PARAM, SPARK_ALLOWED_CONF_PARAM, \
    SPARK_DIRECT_PARAM, SPARK_CONF_PARAM, SPARK_DIRECT_PARAM_ARGS

parser = argparse.ArgumentParser(parents=opentuner.argparsers())


def cast(str_value):
    """
    Casts an input string, possibly a file size, into an integer.

    :param str_value: an input string, possibly a file size.
    :return: an integer value. If file size, the binary value of the
    human readable input.
    """
    return parse_size(str_value, binary=True)


def type_int_range(value):
    """
    Convert an input string, possibly with file sizes, into a range of values.

    :param value: an input string of comma-separated values, possibly file
    sizes. The expected format for range is: start,end,step_size, with end
    (default: start + 1) and step_size (default: 1) are optional.
    :return: a range object representing input range. The range is
    inclusive-exclusive, with a default step size of 1.
    """
    range_array = value.split(",")
    # TODO handle cast and range exceptions
    length_switcher = {
        1: range(cast(range_array[0]), cast(range_array[0]) + 1),
        2: range(cast(range_array[0]), cast(range_array[1])),
        3: range(cast(range_array[0]), cast(range_array[1]),
                 cast(range_array[2])),
    }
    return length_switcher.get(len(range_array),
                               lambda: "Invalid range argument")


# Program information

for param in SPARK_REQUIRED_PARAM:
    param_flag = "--" + param
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    parser.add_argument(param_flag, type=param_tuple[0], required=True,
                        help=param_tuple[1])

# Configuration parameters

for param in set(SPARK_DIRECT_PARAM) - set(SPARK_REQUIRED_PARAM):
    param_flag = "--" + param
    param_tuple = SPARK_DIRECT_PARAM_ARGS[param]
    default_value = str(SPARK_DIRECT_PARAM[param])
    parser.add_argument(param_flag, type=type_int_range, default=default_value,
                        help=param_tuple[1])

for param in SPARK_ALLOWED_CONF_PARAM:
    param_flag = "--" + param
    conf_name = SPARK_ALLOWED_CONF_PARAM[param]
    default_value = str(SPARK_CONF_PARAM[param])
    # TODO add better help
    parser.add_argument(param_flag, type=type_int_range, default=default_value,
                        help=conf_name)
