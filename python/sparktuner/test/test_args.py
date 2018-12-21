"""This module tests argument parsing"""
import unittest
from args import make_flag
from spark_tuner import get_parser
from spark_defaults import SPARK_REQUIRED_PARAM


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser()

    def test_bad_flags(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['--blah', "blah"])
        for param in SPARK_REQUIRED_PARAM:
            with self.assertRaises(SystemExit):
                self.parser.parse_args(['--' + param, param + "_name"])

    def test_required_flags(self):
        args = []
        for param in SPARK_REQUIRED_PARAM:
            args.append(make_flag(param))
            args.append("test_name")
        print(" ".join(args))
        res = self.parser.parse_args(args)
        self.assertIsNotNone(res)
