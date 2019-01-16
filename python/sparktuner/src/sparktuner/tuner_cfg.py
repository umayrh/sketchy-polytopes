"""Contains extensions to some Opentuner classes"""

import time
import psutil
import logging
import subprocess

from util import Util
from multiprocessing.pool import ThreadPool
from opentuner import MeasurementInterface
from opentuner.resultsdb.models import Result
from opentuner.search.manipulator import (NumericParameter,
                                          IntegerParameter,
                                          ScaledNumericParameter)
from opentuner.search.objective import SearchObjective
from opentuner.measurement.interface import (preexec_setpgid_setrlimit,
                                             goodwait,
                                             goodkillpg)

log = logging.getLogger(__name__)


class MeasurementInterfaceExt(MeasurementInterface):
    """
    Extends Opentuner's `MeasurementInterface` to override and add some
    new functionality.
    """
    def __init__(self, *pargs, **kwargs):
        super(MeasurementInterfaceExt, self).__init__(*pargs, **kwargs)
        self.the_io_thread_pool = None

    @staticmethod
    def get_psutil_info(pr):
        """
        :param pr: a psutil Process object
        :return: a tuple of RSS and CPU percent
        """
        with pr.oneshot():
            try:
                mem = pr.memory_info().rss
                cpu = pr.cpu_percent(interval=1)
                return mem, cpu
            except psutil.Error:
                # horrid it may seem but the process may be dead
                pass
        return 0, 0

    def the_io_thread_pool_init(self, parallelism=1):
        if self.the_io_thread_pool is None:
            self.the_io_thread_pool = ThreadPool(2 * parallelism)
            # make sure the threads are started up
            self.the_io_thread_pool.map(int, range(2 * parallelism))

    def call_program(self, cmd, limit=None, memory_limit=None, **kwargs):
        """
        The function is meant to "call cmd and kill it if it
        runs for longer than limit." While the process is running, we
        collect CPU and memory usage data at a 1sec interval.

        This unfortunately is mostly copy-pasta from Opentuner's own
        MeasurementInterface.call_program. The copy-pasta is necessary
        since the original code isn't modular enough and we may want to
        collect process resource usage information during its lifespan.

        :param cmd: (str) command to run
        :param limit: (float) process runtime limit (in seconds)
        :param memory_limit: The maximum area of address space
        which may be taken by the process (in bytes)
        :param kwargs: keyworded args passed to the pipe opened
        for the given command.
        :return: a dictionary like
          {'returncode': 0,
           'stdout': '', 'stderr': '',
           'timeout': False, 'time': 1.89}
        """
        self.the_io_thread_pool_init(self.args.parallelism)

        # performance counters
        cpu_num = psutil.cpu_count(logical=True)
        vcore_secs = 0.0
        mbyte_secs = 0.0

        if limit is float('inf'):
            limit = None
        if type(cmd) in (str, unicode):
            kwargs['shell'] = True
        killed = False
        t0 = time.time()
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=preexec_setpgid_setrlimit(memory_limit),
            **kwargs)
        pup = psutil.Process(p.pid)
        # Add p.pid to list of processes to kill
        # in case of keyboard interrupt
        self.pid_lock.acquire()
        self.pids.append(p.pid)
        self.pid_lock.release()

        try:
            stdout_result = self.the_io_thread_pool.apply_async(p.stdout.read)
            stderr_result = self.the_io_thread_pool.apply_async(p.stderr.read)
            while p.returncode is None:
                if limit is None:
                    # no need to sleep since cpu_percent(interval=1)
                    # is a blocking call
                    perf_res = self.get_psutil_info(pup)
                    mbyte_secs += perf_res[0]
                    vcore_secs += max(perf_res[1], 100) / 100.0 * cpu_num
                elif limit and time.time() > t0 + limit:
                    killed = True
                    goodkillpg(p.pid)
                    goodwait(p)
                else:
                    # TODO: fix repetitive
                    perf_res = self.get_psutil_info(pup)
                    mbyte_secs += perf_res[0]
                    vcore_secs += max(perf_res[1], 100) / 100.0 * cpu_num
                    # still waiting...
                    sleep_for = limit - (time.time() - t0)
                    if not stdout_result.ready():
                        stdout_result.wait(sleep_for)
                    elif not stderr_result.ready():
                        stderr_result.wait(sleep_for)
                    else:
                        # TODO(jansel): replace this with a portable waitpid
                        # (UH) maybe use os.waitpid
                        time.sleep(0.001)
                p.poll()
        except Exception:
            if p.returncode is None:
                goodkillpg(p.pid)
            raise
        finally:
            # No longer need to kill p
            self.pid_lock.acquire()
            if p.pid in self.pids:
                self.pids.remove(p.pid)
            self.pid_lock.release()

        t1 = time.time()
        return {'time': float('inf') if killed else (t1 - t0),
                'timeout': killed,
                'returncode': p.returncode,
                'stdout': stdout_result.get(),
                'stderr': stderr_result.get(),
                'mbyte_secs': mbyte_secs / (1024 ** 2),
                'vcore_secs': vcore_secs}


class ScaledIntegerParameter(ScaledNumericParameter, IntegerParameter):
    SCALING = 1000
    """
    An integer parameter that is searched on a
    linear scale after normalization, but stored without scaling.

    TODO: revisit this implementation, and this class' utility.
    It seems hard to achieve all of the following goals simultaneously:
    - Keep this parameter type an integer,
    - Allow scaling the parameter range by another integer, with
    possibly irrational result,
    - Enforce that rounding, or some other way to convert a real
    value to an integer, doesn't cause a bounded value to go
    out of bounds after either scaling-unscaling or unscaling-scaling.
    A partial solution might be to ensure that scaling factor is
    _effectively_ a real between 0 and 1. We achieve this by rescaling
    values by 1000000.
    The current implementation may fail the following test because
    of rounding errors:
        result = param._scale(param._unscale(val))
        self.assertGreaterEqual(result, min_val)
        self.assertLessEqual(result, max_val)
    """
    def __init__(self, name, min_value, max_value, scaling, **kwargs):
        assert 0 < abs(scaling) <= abs(min_value), "Invalid scaling"
        kwargs['value_type'] = int
        super(ScaledNumericParameter, self).__init__(
            name, min_value, max_value, **kwargs)
        self.scaling = scaling

    def _scale(self, v):
        return (v - self.min_value) * ScaledIntegerParameter.SCALING \
               / float(self.scaling)

    def _unscale(self, v):
        v = (v * self.scaling) / ScaledIntegerParameter.SCALING + \
            self.min_value
        return int(round(v))

    def legal_range(self, config):
        low, high = NumericParameter.legal_range(self, config)
        # We avoid increasing the bounds (to account for rounding)
        # by rescaling using ScaledIntegerParameter.SCALING
        return int(self._scale(low)), int(self._scale(high))


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
    def __init__(self, rel_tol=1e-09, abs_tol=0.0, ranged_param_dict={}):
        """
        :param rel_tol: relative tolerance for math.isclose()
        :param abs_tol: absolute tolerance for math.isclose()
        :param ranged_param_dict: dict of ranged SparkParamType
        """
        super(SearchObjective, self).__init__()
        self.rel_tol = rel_tol
        self.abs_tol = abs_tol
        self.ranged_param_dict = ranged_param_dict

    def result_order_by_terms(self):
        """Return database columns required to order by the objective"""
        return [Result.time, Result.size]

    def result_compare(self, result1, result2):
        """cmp() compatible comparison of resultsdb.models.Result"""
        if Util.isclose(result1.time, result2.time,
                        self.rel_tol, self.abs_tol):
            return cmp(result1.size, result2.size)
        return cmp(result1.time, result2.time)

    def display(self, result):
        """
        Produce a string version of a resultsdb.models.Result()
        """
        return "time=%.2f, size=%.2f, config=%s" % \
               (result.time, result.size, str(result.configuration.data))

    @staticmethod
    def _ratio(a, b):
        if b == 0:
            return float('inf') * a
        return a / b

    def result_relative(self, result1, result2):
        """return None, or a relative goodness of resultsdb.models.Result"""
        if Util.isclose(result1.time, result2.time,
                        self.rel_tol, self.abs_tol):
            return MinimizeTimeAndResource._ratio(result1.size, result2.size)
        return MinimizeTimeAndResource._ratio(result1.time, result2.time)
