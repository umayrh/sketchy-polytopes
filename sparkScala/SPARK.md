# Spark

## Resources

* [Apache Spark - Best Practices and Tuning](https://umbertogriffo.gitbooks.io/apache-spark-best-practices-and-tuning/content/)
* [Spark 2.x Troubleshooting Guide](https://www.slideshare.net/jcmia1/a-beginners-guide-on-troubleshooting-spark-applications)
* [Lessons from Using Spark...](https://www.indix.com/blog/engineering/lessons-from-using-spark-to-process-large-amounts-of-data-part-i/)
* [What I learned from...](https://dlab.epfl.ch/2017-09-30-what-i-learned-from-processing-big-data-with-spark/)

## Common errors

##### `java.lang.OutOfMemoryError: Java heap space java.lang.OutOfMemoryError: GC overhead limit exceeded`
May be caused by:
* Insufficient driver memory.
* Inefficient code e.g. using Scala `Seq` to store a large number of objects instead
of using RDD or Dataframe directly.

May also respond to:
* Using a different garbage collection algorithm

## Quick notes

### Projects

* Given a large, complex data pipeline that consists of distinct Spark jobs such that each job
  * has its own resource requirements, and
  * reads input from and writes output to some distributed file system (HDFS, S3...).

  Set the scheduler so that it improves data locality.

### S3

* Large number of partitions for Spark jobs requesting S3 objects may lead to S3 rate being limited.

### YARN

* The default scheduler ([CapacityScheduler](https://hadoop.apache.org/docs/r2.7.4/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)) might schedule containers on lost nodes. This 
would cause Spark jobs to never make progress but not fail either.
[YARN-1198](https://issues.apache.org/jira/browse/YARN-1680) describes the issue while [YARN-3446](https://issues.apache.org/jira/browse/YARN-3446) fixes it for 
[FairScheduler](https://hadoop.apache.org/docs/r2.7.4/hadoop-yarn/hadoop-yarn-site/FairScheduler.html).
  * In EMR, it's possible to change the scheduling algorithm of a live cluster by
    * logging into EMR master,
    * updating `/etc/hadoop/conf/yarn-site.xml`:
        ```
        <property>
          <name>yarn.resourcemanager.scheduler.class</name>
          <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value>
        </property>
        ```
    * and, finally, restarting YARN:
        ```
        sudo /sbin/stop hadoop-yarn-resourcemanager
        sudo /sbin/start hadoop-yarn-resourcemanager
        ```
* In an AWS cluster, YARN core nodes may be terminated and new ones created silently if e.g. HDFS storage exceeds capacity. This will cause Spark job to die eventually but slowly.
