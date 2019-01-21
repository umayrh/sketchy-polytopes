import os
import json
import os.path
import unittest
import contextlib
import requests_mock

from requests.compat import urljoin
from sparktuner.yarn_metrics import (YarnMetrics,
                                     YarnProperty,
                                     YarnResourceManager)


class YarnMetricsTestUtil(object):
    @staticmethod
    @contextlib.contextmanager
    def modified_environ(*remove, **update):
        """
        Temporarily updates the ``os.environ`` dictionary in-place.

        The ``os.environ`` dictionary is updated in-place so that
        the modification is sure to work in all situations.

        This function is cribbed from:
          https://github.com/laurent-laporte-pro/stackoverflow-q2059482

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


class YarnMetricsConfigTest(unittest.TestCase):
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
        self.assertEqual(
            "localhost",
            yarn_properties["yarn.resourcemanager.hostname"])
        # TODO: is this right, or should the value be substituted?
        self.assertEqual(
            "${yarn.resourcemanager.hostname}:8090",
            yarn_properties["yarn.resourcemanager.webapp.https.address.rm1"])


class YarnMetricsServiceTest(unittest.TestCase):
    def setUp(self):
        self.yarn_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resources")
        self.yarn_properties = YarnMetrics.get_yarn_property_map(
            os.path.join(self.yarn_dir, YarnMetrics.YARN_SITE))

    def test_get_webapp_protocol(self):
        proto = YarnMetrics.get_webapp_protocol(self.yarn_properties)
        self.assertEqual("http", proto)

        proto = YarnMetrics.get_webapp_protocol(
            {YarnProperty.HTTP_POLICY: "https_only"})
        self.assertEqual("https", proto)

    def test_get_webapp_port(self):
        port = YarnMetrics.get_webapp_port(self.yarn_properties)
        self.assertEqual("8088", port)

        port = YarnMetrics.get_webapp_port(
            {YarnProperty.HTTP_POLICY: "https_only"})
        self.assertEqual("8090", port)

    def test_get_rm_ha_webapp_addr(self):
        with self.assertRaises(NotImplementedError):
            YarnMetrics._get_rm_ha_webapp_addr("", "")

    def rm_webapp_addr_helper(self, mocker, yarn_properties, addr_property):
        proto = YarnMetrics.get_webapp_protocol(yarn_properties)
        port = YarnMetrics.get_webapp_port(yarn_properties)
        addr = yarn_properties[addr_property]
        headers = {"content-type": "application/json"}

        mocker.get(urljoin(proto + "://" + addr + ":" + port,
                           YarnResourceManager.ROUTE_INFO),
                   json="[]", headers=headers)
        self.assertEqual(
            addr,
            YarnMetrics._get_rm_webapp_addr(proto, port, yarn_properties)
        )

    @requests_mock.Mocker()
    def test_get_rm_webapp_addr(self, mocker):
        yarn_properties = {YarnProperty.RM_WEBAPP_ADDR: "spark.data"}
        self.rm_webapp_addr_helper(
            mocker, yarn_properties, YarnProperty.RM_WEBAPP_ADDR)

        yarn_properties = {YarnProperty.RM_ADDR: "10.1.5.2",
                           YarnProperty.HTTP_POLICY: "https_only"}
        self.rm_webapp_addr_helper(
            mocker, yarn_properties, YarnProperty.RM_ADDR)

    def yarn_api_helper(self, mocker, json_file, proto, addr, port, route):
        headers = {"content-type": "application/json"}
        info_resp_path = os.path.join(
            self.yarn_dir, json_file)
        with open(info_resp_path) as json_file:
            json_data = json.load(json_file)
            base_url = proto + "://" + addr + ":" + port
            req_url = urljoin(base_url, route)
            mocker.get(req_url, json=json_data, headers=headers)
        return json_data

    @requests_mock.Mocker()
    def test_get_yarn_info(self, mocker):
        proto, addr, port = ("http", "spark.data", "8088")
        expected_json_data = self.yarn_api_helper(
            mocker,
            "yarn-resp-cluster-info.json",
            proto, addr, port,
            YarnResourceManager.ROUTE_INFO)
        self.assertDictEqual(
            expected_json_data,
            YarnMetrics.get_yarn_info(proto, addr, port)
        )

    @requests_mock.Mocker()
    def test_get_yarn_app_info(self, mocker):
        proto, addr, port, app_id = ("http", "spark.data", "8088", "appid")
        expected_json_data = self.yarn_api_helper(
            mocker,
            "yarn-resp-app-info.json",
            proto, addr, port,
            urljoin(YarnResourceManager.ROUTE_APP_ID, app_id))
        self.assertDictEqual(
            expected_json_data["app"],
            YarnMetrics.get_yarn_app_info(proto, addr, port, app_id)
        )