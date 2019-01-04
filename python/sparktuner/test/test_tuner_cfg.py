import unittest
import random
from sparktuner.tuner_cfg import ScaledIntegerParameter


class ScaledIntegerParameterTest(unittest.TestCase):
    def test_bad_scaling_values(self):
        with self.assertRaises(AssertionError):
            ScaledIntegerParameter("a", 1, 2, 0)
        with self.assertRaises(AssertionError):
            ScaledIntegerParameter("a", 3, 1000, 20)
        with self.assertRaises(AssertionError):
            ScaledIntegerParameter("a", 30, 100, 1000)

    def _test_scaling_unscaling(self):
        """
        Test if scaling and unscaling, in any order,
        cause a parameter values to go out of bounds
        TODO
        """
        test_size = 100
        min_values = random.sample(range(1, 1000), test_size)
        max_values = random.sample(range(1000, 10000), test_size)

        for idx in range(0, test_size):
            min_val = min_values[idx]
            max_val = max_values[idx]
            scale = random.randint(1, min_val + 1)

            param = ScaledIntegerParameter("a", min_val, max_val, scale)
            val = random.randint(min_val, max_val)

            result = param._scale(param._unscale(val))
            print ("a. val scale unscale: " +
                   " ".join([str(val), str(scale), str(param._unscale(val))]))

            self.assertGreaterEqual(result, min_val)
            self.assertLessEqual(result, max_val)

            result = param._unscale(param._scale(val))
            print ("b. val scale unscale: " +
                   " ".join([str(val), str(scale), str(param._scale(val))]))
            self.assertGreaterEqual(result, min_val)
            self.assertLessEqual(result, max_val)


class MinimizeTimeAndResourceTest(unittest.TestCase):
    def test_blah(self):
        pass
