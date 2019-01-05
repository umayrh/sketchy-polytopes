"""Contains extension to Opentuner manipualtor objects"""

import logging
from opentuner.resultsdb.models import Result
from opentuner.search.manipulator import (NumericParameter,
                                          IntegerParameter,
                                          ScaledNumericParameter)
from opentuner.search.objective import SearchObjective
# YUCK!
try:
    from math import isclose
except ImportError:
    # Python 3 backport
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

log = logging.getLogger(__name__)


class ScaledIntegerParameter(ScaledNumericParameter, IntegerParameter):
    """
    An integer parameter that is searched on a
    linear scale after normalization, but stored without scaling
    """
    def __init__(self, name, min_value, max_value, scaling, **kwargs):
        assert 0 < abs(scaling) <= abs(min_value), "Invalid scaling"
        kwargs['value_type'] = int
        super(ScaledNumericParameter, self).__init__(
            name, min_value, max_value, **kwargs)
        self.scaling = scaling

    def _scale(self, v):
        return (v + 1.0 - self.min_value) / float(self.scaling)

    def _unscale(self, v):
        v = v * self.scaling - 1.0 + self.min_value
        v = int(round(v))
        return v

    def legal_range(self, config):
        low, high = NumericParameter.legal_range(self, config)
        # increase the bounds account for rounding
        return self._scale(low - 0.4999), self._scale(high + 0.4999)

    def search_space_size(self):
        return self._scale(
            super(ScaledIntegerParameter, self).search_space_size())


class MinimizeTimeAndResource(SearchObjective):
    """
    Minimize Result().time (with epsilon-comparison), and
    break ties with Result().size, which is being overloaded to
    represent a single Spark resource amount (memory, partitions,
    CPU etc).
    Note: given how Result model is structured around a fixed set of
    objective function values, it seems that there's no clean way
    to support minimizing multiple kinds of resource usage.
    """
    def __init__(self, rel_tol=1e-09, abs_tol=0.0):
        """
        :param rel_tol: relative tolerance for math.isclose()
        :param abs_tol: absolute tolerance for math.isclose()
        """
        super(SearchObjective, self).__init__()
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol

    def result_order_by_terms(self):
        """Return database columns required to order by the objective"""
        return [Result.time, Result.size]

    def result_compare(self, result1, result2):
        """cmp() compatible comparison of resultsdb.models.Result"""
        if isclose(result1.time, result2.time, self.rel_tol, self.abs_tol):
            return cmp(result1.size, result2.size)
        return cmp(result1.time, result2.time)

    def display(self, result):
        """
        Produce a string version of a resultsdb.models.Result()
        """
        return "time=%.2f, size=%.1f" % (result.time, result.size)

    @staticmethod
    def _ratio(a, b):
        if b == 0:
            return float('inf') * a
        return a / b

    def result_relative(self, result1, result2):
        """return None, or a relative goodness of resultsdb.models.Result"""
        if isclose(result1.time, result2.time, self.rel_tol, self.abs_tol):
            return MinimizeTimeAndResource._ratio(result1.time, result2.time)
        return MinimizeTimeAndResource._ratio(result1.size, result2.size)
