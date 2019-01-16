class SparkMetrics(object):
    """
    Utilities for collecting Spark job performance metrics.
    These follow Hadoop-YARN's ResourceManager API:
    https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/ResourceManagerRest.html
    YARN provides the following metrics:

    * memorySeconds
        * (long) The amount of memory the application has allocated
        (megabyte-seconds)
    * vcoreSeconds
        * (long) The amount of CPU resources the application has
        allocated (virtual core-seconds)
    * elapsedTime
        * (long) The elapsed time since the application started (in ms)

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
    """
    @staticmethod
    def get_metrics(spark_master, master_addr, app_id):
        """
        Returns a tupe containing metrics about RAM and vcores
        consumed (over time), and application runtime.
        :param spark_master: (str) either 'yarn' or 'localhost'
        :param master_addr: if master is 'yarn', then the
        yarn.resourcemanager.webapp.address including the port
        number. Otherwise, unused.
        :param app_id: if 'yarn', then the application id. If
        'localhost', then the process id.
        :return: a triple containing:
        - an int, representing MB-seconds
        - an int, representing vcore seconds,
        - an int, representing runtime in seconds
        """
        pass
