import psutil


class SparkMetrics(object):
    """
    Utilities for collecting Spark job performance metrics.
    Following Hadoop-YARN's ResourceManager API
    (https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html),
    we focus on the following metrics:

    * memorySeconds
        * (long) The amount of memory the application has allocated
        (megabyte-seconds)
    * vcoreSeconds
        * (long) The amount of CPU resources the application has
        allocated (virtual core-seconds)
    * elapsedTime
        * (long) The elapsed time since the application started (in ms)

    TODO: use abc's to allow user-specific implementations
    """
    @staticmethod
    def get_yarn_metrics(master_addr, app_id):
        """
        Returns a tuple containing metrics about RAM and vcores
        consumed (over time), and application runtime.

        Here's a sample request and response:
        $ GET https://rm_address:8090/ws/v1/cluster/apps/app_id

        <app>
            <id>app_id</id>
            <user>user_name</user>
            <name>spark_job_name</name>
            <queue>queue_name</queue>
            <state>FINISHED</state>
            <finalStatus>SUCCEEDED</finalStatus>
            <progress>100.0</progress>
            <trackingUI>History</trackingUI>
            <trackingUrl>
                http://spark_master_dns_name:20888/proxy/app_id/
            </trackingUrl>
            <diagnostics/>
            <clusterId>1546536712852</clusterId>
            <applicationType>SPARK</applicationType>
            <applicationTags/>
            <priority>0</priority>
            <startedTime>1547501766223</startedTime>
            <finishedTime>1547503062445</finishedTime>
            <elapsedTime>1296222</elapsedTime>
            <amContainerLogs>
                http://spark_master_dns_name:8042/node/containerlogs/app_id/user_name
            </amContainerLogs>
            <amHostHttpAddress>am_host:8042</amHostHttpAddress>
            <amRPCAddress>am_ip_address:0</amRPCAddress>
            <allocatedMB>-1</allocatedMB>
            <allocatedVCores>-1</allocatedVCores>
            <runningContainers>-1</runningContainers>
            <memorySeconds>443600497</memorySeconds>
            <vcoreSeconds>64720</vcoreSeconds>
            <queueUsagePercentage>0.0</queueUsagePercentage>
            <clusterUsagePercentage>0.0</clusterUsagePercentage>
            <preemptedResourceMB>0</preemptedResourceMB>
            <preemptedResourceVCores>0</preemptedResourceVCores>
            <numNonAMContainerPreempted>0</numNonAMContainerPreempted>
            <numAMContainerPreempted>0</numAMContainerPreempted>
            <preemptedMemorySeconds>0</preemptedMemorySeconds>
            <preemptedVcoreSeconds>0</preemptedVcoreSeconds>
            <logAggregationStatus>SUCCEEDED</logAggregationStatus>
            <unmanagedApplication>false</unmanagedApplication>
            <amNodeLabelExpression/>
        </app>

        :param master_addr: the yarn.resourcemanager.webapp.address
        including the port number.
        :param app_id: the application id.
        :return: a triple containing:
        - an int, representing MB-seconds
        - an int, representing vcore seconds,
        - an int, representing runtime in seconds
        """
        pass

    @staticmethod
    def get_process_metrics(pr, cpu_interval=1):
        """
        Gets process metrics in psutil.Process.oneshot() using
        psutil.memory_info() and psutil.cpu_percent().
        Note that cpu_percent(interval=...) is a blocking call,
        so this function will effectively sleep for cpu_interval
        seconds.
        TODO: Unique set size (USS) rather than resident set size
        (RSS) is probably a better metric but:
        1. USS may not be available on all platforms, and
        2. accessing USS may require higher privileges.
        Can these issues be resolved?

        :param pr: a psutil.Process object
        :param cpu_interval: interval (in secs) for
        psutil.cpu_percent(). May be None.
        :return: a tuple of RSS (in bytes) and CPU percent over
        cpu_interval
        """
        with pr.oneshot():
            try:
                mem = pr.memory_info().rss
                cpu = pr.cpu_percent(interval=cpu_interval)
                return mem, cpu
            except psutil.Error:
                # horrid it may seem but the process may be dead
                pass
        return 0, 0
