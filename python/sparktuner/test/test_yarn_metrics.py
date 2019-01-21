import os
import os.path
import contextlib
import unittest

from sparktuner.yarn_metrics import YarnMetrics


class YarnMetricsTestUtil(object):
    @staticmethod
    @contextlib.contextmanager
    def modified_environ(*remove, **update):
        """
        Temporarily updates the ``os.environ`` dictionary in-place.

        The ``os.environ`` dictionary is updated in-place so that
        the modification is sure to work in all situations.
        From: https://github.com/laurent-laporte-pro/stackoverflow-q2059482

        :param remove: Environment variables to remove.
        :param update: Dictionary of environment variables and values
        to add/update.
        """
        env = os.environ
        update = update or {}
        remove = remove or []

        # List of environment variables being updated or removed.
        stomped = (set(update.keys()) | set(remove)) & set(env.keys())
        # Environment variables and values to restore on exit.
        update_after = {k: env[k] for k in stomped}
        # Environment variables and values to remove on exit.
        remove_after = frozenset(k for k in update if k not in env)

        try:
            env.update(update)
            [env.pop(k, None) for k in remove]
            yield
        finally:
            env.update(update_after)
            [env.pop(k) for k in remove_after]


class YarnMetricsTest(unittest.TestCase):
    def setUp(self):
        self.yarn_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resources")

    def test_get_yarn_site_path(self):
        with YarnMetricsTestUtil.modified_environ(
                'YARN_CONF_DIR', HADOOP_CONF_DIR=self.yarn_dir):
            yarn_site_path = YarnMetrics.get_yarn_site_path()
            self.assertIsNotNone(yarn_site_path)
            self.assertEqual(
                YarnMetrics.YARN_SITE, os.path.basename(yarn_site_path))
            self.assertEqual(
                self.yarn_dir, os.path.dirname(yarn_site_path))

        with YarnMetricsTestUtil.modified_environ(
                'HADOOP_CONF_DIR', YARN_CONF_DIR=self.yarn_dir):
            yarn_site_path = YarnMetrics.get_yarn_site_path()
            self.assertIsNotNone(yarn_site_path)
            self.assertEqual(
                YarnMetrics.YARN_SITE, os.path.basename(yarn_site_path))
            self.assertEqual(
                self.yarn_dir, os.path.dirname(yarn_site_path))

        with YarnMetricsTestUtil.modified_environ(
                'YARN_CONF_DIR', 'HADOOP_CONF_DIR'):
            self.assertIsNone(YarnMetrics.get_yarn_site_path())

    def test_get_yarn_property_map(self):
        yarn_site_path = os.path.join(
            self.yarn_dir, YarnMetrics.YARN_SITE)
        yarn_properties = YarnMetrics.get_yarn_property_map(yarn_site_path)

        self.assertIsNotNone(yarn_properties)
        self.assertEqual("localhost",
                         yarn_properties["yarn.resourcemanager.hostname"])

        # TODO: is this right, or should the value be substituted?
        self.assertEqual(
            "${yarn.resourcemanager.hostname}:8090",
            yarn_properties["yarn.resourcemanager.webapp.https.address.rm1"])

    @unittest.skip
    def test_get_webapp_protocol(self):
        pass

    @unittest.skip
    def test_get_yarn_app_info(self):
        pass

    @unittest.skip
    def test_get_rm_webapp_addr(self):
        pass
