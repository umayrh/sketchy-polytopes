"""This module tests argument parsing"""
import unittest
from args import ArgumentParserError, make_flag, to_flag, type_int_range
from spark_tuner import get_parser
from spark_defaults import SPARK_REQUIRED_PARAM, SPARK_ALLOWED_CONF_PARAM


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()

    def test_bad_flags(self):
        with self.assertRaises(ArgumentParserError):
            self.parser.parse_args(['--blah', "blah"])
        for param in SPARK_REQUIRED_PARAM:
            with self.assertRaises(ArgumentParserError):
                self.parser.parse_args(['--' + param, param + "_name"])

    def test_required_flags(self):
        args = []
        for param in SPARK_REQUIRED_PARAM:
            args.append(make_flag(param))
            args.append("test_name")
        res = self.parser.parse_args(args)
        self.assertIsNotNone(res)
        res_dict = vars(res)
        for param in SPARK_REQUIRED_PARAM:
            self.assertEqual(res_dict[to_flag(param)], "test_name")

    def test_type_int_range(self):
        self.assertEqual(type_int_range("2"), range(2, 3))
        self.assertEqual(type_int_range("2,3"), range(2, 3))
        self.assertEqual(type_int_range("2,4,1"), range(2, 4, 1))
        with self.assertRaises(IndexError):
            type_int_range("2,4,1,0")
        with self.assertRaises(IndexError):
            type_int_range("")

    def optional_flags(self):
        args = []
        for param in SPARK_REQUIRED_PARAM:
            args.append(make_flag(param))
            args.append("test_name")
        for param in SPARK_ALLOWED_CONF_PARAM:
            args.append(make_flag(param))
            args.append("2")

        print("args " + " ".join(args))
        res = self.parser.parse_args(args)
        self.assertIsNotNone(res)
        res_dict = vars(res)
        for param in SPARK_ALLOWED_CONF_PARAM:
            self.assertEqual(res_dict[to_flag(param)], "2")
