"""Tests util module"""

import unittest
from sparktuner.util import Util, InvalidSize


class UtilsTest(unittest.TestCase):
    def test_format_size(self):
        self.assertEqual("0b", Util.format_size(0))
        self.assertEqual("5b", Util.format_size(5))
        self.assertEqual("1kb", Util.format_size(1024))
        self.assertEqual("10kb", Util.format_size(10240))
        self.assertEqual("1mb", Util.format_size(1024 ** 2))
        self.assertEqual("22mb", Util.format_size(1024 ** 2 * 22))
        self.assertEqual("4gb", Util.format_size(1024 ** 3 * 4))
        self.assertEqual("4218mb", Util.format_size(int(1024 ** 3 * 4.12)))
        self.assertEqual("4tb", Util.format_size(1024 ** 4 * 4))
        self.assertEqual("4218gb", Util.format_size(int(1024 ** 4 * 4.12)))
        self.assertEqual("4pb", Util.format_size(1024 ** 5 * 4))
        self.assertEqual("4218tb", Util.format_size(int(1024 ** 5 * 4.12)))

        with self.assertRaises(InvalidSize):
            Util.format_size(1024 ** 3 * 4.12)
