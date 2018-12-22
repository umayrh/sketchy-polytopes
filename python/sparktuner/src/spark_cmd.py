from collections import ChoiceMap
from args import ArgumentParser
from spark_defaults import SPARK_DIRECT_PARAM, SPARK_ALLOWED_CONF_PARAM


class SparkSubmitCmd:
    """
    Constructs spark-submit command
    """
    CMD_SEPARATOR = " "
    SPARK_SUBMIT_PATH = "/usr/local/bin/spark-submit"

    @staticmethod
    def make_spark_direct_flag(flag_param):
        """
        Converts a direct parameter into a flag by prefixing it with "--"
        :param flag_param: a parameter
        :return: parameter prefixed with "--"
        """
        return "--" + flag_param

    @staticmethod
    def make_spark_conf_flag(flag_param):
        """
        Converts a parameter into a flag by prefixing it with "--conf "
        :param flag_param: a parameter
        :return: parameter prefixed with "--conf "
        """
        return "--conf " + flag_param

    @staticmethod
    def make_subcmd(param_dict, is_direct=False):
        """
        Creates the sub-command for Spark direct param

        :param param_dict: dictionary mapping a Spark
        parameter to its value
        :param is_direct whether the dictionary parameters are
        direct or conf (default: False i.e. conf params)
        :return: a string representing the sub-command without leading
        or trailing whitespaces
        """
        dirc_flag = SparkSubmitCmd.make_spark_direct_flag
        conf_flag = SparkSubmitCmd.make_spark_conf_flag
        subcmd_list = []
        for param, value in param_dict:
            param_flag = dirc_flag(param) if is_direct else conf_flag(param)
            subcmd_list.append(param_flag)
            subcmd_list.append(value)
        return SparkSubmitCmd.CMD_SEPARATOR.join(subcmd_list)

    def merge_params(self, arg_dict, tuner_cfg_dict):
        """
        XXX
        :param arg_dict:
        :param tuner_cfg_dict:
        :return:
        """
        input_direct_params = dict()
        input_conf_params = dict()

        # extract direct and conf param from input dicts
        for param, value in arg_dict:
            from_flag = ArgumentParser.from_flag(param)
            if from_flag in SPARK_DIRECT_PARAM:
                input_direct_params[param] = value
            elif from_flag in SPARK_ALLOWED_CONF_PARAM:
                input_conf_params[SPARK_ALLOWED_CONF_PARAM[param]] = value
        for param, value in tuner_cfg_dict:
            from_flag = ArgumentParser.from_flag(param)
            if from_flag in SPARK_DIRECT_PARAM:
                input_direct_params[param] = value
            elif from_flag in SPARK_ALLOWED_CONF_PARAM:
                input_conf_params[SPARK_ALLOWED_CONF_PARAM[param]] = value

        # merge input dicts with defaults
        direct_params = ChoiceMap(
            input_direct_params, self.direct_param_default)
        conf_params = ChoiceMap(input_conf_params, self.conf_defaults)

        return dict(direct_params), dict(conf_params)

    def make_cmd(self, arg_dict, tuner_cfg_dict):
        """
        Constructs spark-submit command

        :param arg_dict: string dictionary of program arguments to their
        values. This include Spark and non-Spark params. This dict is
        required to contained the key ArgumentParser.JAR_PATH_ARG_NAME.
        :param tuner_cfg_dict:
        :return: a string representing an executable spark-submit
        command
        """
        # extract path and program_conf args
        assert ArgumentParser.JAR_PATH_ARG_NAME in arg_dict
        jar_path = arg_dict.get(ArgumentParser.JAR_PATH_ARG_NAME)
        program_conf = \
            arg_dict.get(ArgumentParser.PROGRAM_CONF_ARG_NAME, "")

        # merge input parameter
        (direct_params, conf_params) = \
            self.merge_params(arg_dict, tuner_cfg_dict)
        # construct command from parameters
        return SparkSubmitCmd.CMD_SEPARATOR.join([
            SparkSubmitCmd.SPARK_SUBMIT_PATH,
            SparkSubmitCmd.make_subcmd(direct_params, True),
            SparkSubmitCmd.make_subcmd(conf_params, False),
            jar_path,
            program_conf
        ])

    def __init__(self, direct_param_default=dict(), conf_defaults=dict()):
        self.direct_param_default = direct_param_default
        self.conf_defaults = conf_defaults
        return
