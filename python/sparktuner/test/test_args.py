"""This module tests argument parsing"""

import unittest
from args import ArgumentParserError, ArgumentParser
from spark_defaults import SPARK_REQUIRED_DIRECT_PARAM, \
    SPARK_ALLOWED_CONF_PARAM


class ArgumentParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = ArgumentParser()

    @staticmethod
    def make_required_flags():
        args = ["--path", "path/to"]
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            args.append(ArgumentParser.make_flag(param))
            args.append("test_name")
        return args

    def test_bad_flags(self):
        with self.assertRaises(ArgumentParserError):
            self.parser.parse_args(['--blah', "blah"])
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            with self.assertRaises(ArgumentParserError):
                self.parser.parse_args(['--' + param, param + "_name"])

    def test_required_flags(self):
        args = self.make_required_flags()
        res = self.parser.parse_args(args)
        self.assertIsNotNone(res)
        res_dict = vars(res)
        for param in SPARK_REQUIRED_DIRECT_PARAM:
            param_flag = ArgumentParser.to_flag(param)
            self.assertEqual(res_dict[param_flag], "test_name")

    def test_type_int_range(self):
        range_flag = ArgumentParser.type_int_range("2")
        self.assertEqual(range_flag, (2, 2))
        range_flag = ArgumentParser.type_int_range("2k")
        self.assertEqual(range_flag, (2048, 2048))
        range_flag = ArgumentParser.type_int_range("2,3")
        self.assertEqual(range_flag, (2, 3))
        range_flag = ArgumentParser.type_int_range("2g,4g")
        self.assertEqual(range_flag, (2*1024**3, 4*1024**3))

        with self.assertRaises(ArgumentParserError):
            ArgumentParser.type_int_range("2,4,1")
        with self.assertRaises(ArgumentParserError):
            ArgumentParser.type_int_range("")

    def test_optional_flags(self):
        args = self.make_required_flags()
        for param in SPARK_ALLOWED_CONF_PARAM:
            args.append(ArgumentParser.make_flag(param))
            args.append("2")

        res = self.parser.parse_args(args)
        self.assertIsNotNone(res)
        res_dict = vars(res)
        for param in SPARK_ALLOWED_CONF_PARAM:
            param_flag = ArgumentParser.to_flag(param)
            self.assertEqual(res_dict[param_flag], (2, 2))
