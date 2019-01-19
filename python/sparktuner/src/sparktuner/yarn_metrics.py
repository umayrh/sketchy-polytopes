import os
import logging

from util import XmlParser, WebRequest, WebRequestError

log = logging.getLogger(__name__)


class YarnProperty(object):
    RM_ADDR = "yarn.resourcemanager.address"
    RM_WEBAPP_ADDR = "yarn.resourcemanager.webapp.address"
    RM_HAS_HA = "yarn.resourcemanager.ha.enabled"
    RM_PREFIX_WEBAPP_HTTPS = "yarn.resourcemanager.webapp.https.address."
    RM_PREFIX_WEBAPP_ADDR = "yarn.resourcemanager.webapp.address."
    RM_PREFIX_ADMIN_ADDR = "yarn.resourcemanager.admin.address."
    HTTP_POLICY = "yarn.http.policy"


class YarnResourceManager(object):
    ROUTE_INFO = "/ws/v1/cluster/info"
    ROUTE_APP_ID = "/ws/v1/cluster/apps/app_id"


class YarnMetricsError(Exception):
    pass


class YarnMetrics(object):
    """
    Utilities for accessing YARN configuration parameters,
    and for querying YARN Resource Manager.

    This implementation follows Sparlyr:
    https://github.com/rstudio/sparklyr/blob/master/R/yarn_cluster.R

    See also YARN's ResourceManager API:
    https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html
    """
    YARN_CONF_DIR = "YARN_CONF_DIR"
    HADOOP_CONF_DIR = "HADOOP_CONF_DIR"
    YARN_SITE = "yarn-site.xml"
    YARN_API_REQUEST_HEADER = {}

    @staticmethod
    def get_yarn_site_path():
        """
        Locates yarns-site.xml by using either the YARN_CONF_DIR
        or HADOOP_CONF_DIR environment variables.
        :return: the path, as a str, if the file exist. None otherwise
        """
        conf_dir = os.getenv(YarnMetrics.YARN_CONF_DIR,
                             os.getenv(YarnMetrics.HADOOP_CONF_DIR))
        if not conf_dir:
            return None

        yarn_site = os.path.join(conf_dir, YarnMetrics.YARN_SITE)
        if os.path.exists(yarn_site):
            return yarn_site
        return None

    @staticmethod
    def get_yarn_property_map(yarn_site_path):
        """
        :param yarn_site_path: absolute path to yarn-site.xml
        :return: a dictionary of parameter names and values in the
        yarn-site.xml file, or an empty dict if path is an empty str.
        :raises XmlParserError if file not found or if XML cannot be parsed.
        """
        if not yarn_site_path:
            return {}
        xml_parsed = XmlParser.parse_file(yarn_site_path)
        # there must be a one-pass way to do this
        property_names = XmlParser.map_element_data(xml_parsed, 'name')
        property_values = XmlParser.map_element_data(xml_parsed, 'value')
        return dict(zip(property_names, property_values))

    @staticmethod
    def get_webapp_protocol(yarn_property_map):
        """
        :param yarn_property_map: dict of YARN properties
        :return: str ("http" or "https") representing
        YARN HTTP policy
        """
        proto = yarn_property_map.get(YarnProperty.HTTP_POLICY, "http")
        if proto.lower() == "https_only":
            return "https"
        return "http"

    @staticmethod
    def _get_rm_ha_webapp_addr(yarn_webapp_proto, yarn_property_map):
        """
        TODO(unimplemented)
        :param yarn_webapp_proto: YARN HTTP policy
        :param yarn_property_map: dict of YARN properties
        :return: the web address of a live HA Resource Manager
        if server address can be found in yarn-site.xml and if
        the server is currently online.
        """
        raise NotImplementedError

    @staticmethod
    def _get_rm_webapp_addr(yarn_webapp_proto, yarn_property_map):
        rm_addr = yarn_property_map.get(
            YarnProperty.RM_WEBAPP_ADDR,
            yarn_property_map.get(
                YarnProperty.RM_ADDR,
                None))
        if not rm_addr:
            raise YarnMetricsError("No RM address in yarn-site.xml")
        # return rm_addr if server is online
        try:
            # Check to see if the server is available
            resp = WebRequest.request_get(
                webapp=rm_addr,
                route=YarnResourceManager.ROUTE_INFO,
                data_dict=None,
                scheme=yarn_webapp_proto)
            log.debug("YARN RM info: " + str(resp))
            return rm_addr
        except WebRequestError:
            raise YarnMetricsError("Cannot reach RM server")

    @staticmethod
    def get_rm_webapp_addr(yarn_webapp_proto, yarn_property_map):
        """
        :param yarn_webapp_proto: YARN HTTP policy
        :param yarn_property_map: dict of YARN properties
        :return: the web address of a live Resource Manager
        if server address can be found in yarn-site.xml and
        if the server is currently online.
        TODO: may we should append scheme and port too
        """
        has_ha = yarn_property_map.get(YarnProperty.RM_HAS_HA, "false")
        if has_ha.lower() == "true":
            return YarnMetrics._get_rm_ha_webapp_addr(
                yarn_webapp_proto, yarn_property_map)
        return YarnMetrics._get_rm_webapp_addr(
            yarn_webapp_proto, yarn_property_map)

    @staticmethod
    def call_yarn_api(yarn_webapp_proto,
                      yarn_rm_addr,
                      yarn_rm_route,
                      request_data_dict=None):
        try:
            # Check to see if the server is available
            resp = WebRequest.request_get(
                webapp=yarn_rm_addr,
                route=yarn_rm_route,
                data_dict=None,
                scheme=yarn_webapp_proto)
            log.debug("YARN RM info: " + str(resp))
            return yarn_rm_addr
        except WebRequestError:
            raise YarnMetricsError("Cannot reach RM server")

    @staticmethod
    def get_yarn_app_info(rm_addr, app_id, items=None):
        """
        This function get info form YARN Resource Manager's
        Cluster Application API. "An application resource contains
        information about a particular application that was
        submitted to a cluster."
        :param rm_addr: YARN Resource Manager Webapp address
        :param app_id: YARN application id
        :param items: resource names to collect data for. If
        None, all information is collected.
        :return: a dict of resource name to resource values.
        """
        raise NotImplementedError

    def __init__(self):
        # Some of these may raise, which shouldn't happen in ctor
        yarn_site_path = YarnMetrics.get_yarn_site_path()
        yarn_property_map = YarnMetrics.get_yarn_property_map(yarn_site_path)
        yarn_webapp_proto = YarnMetrics.get_webapp_protocol(
            yarn_property_map)
        self.yarn_rm_webapp_addr = YarnMetrics.get_rm_webapp_addr(
            yarn_webapp_proto, yarn_property_map)

    def get_app_info(self, app_id, items=None):
        return YarnMetrics.get_yarn_app_info(
            self.yarn_rm_webapp_addr, app_id, items)
