# Spark

## Quick notes

* Large number of partitions for Spark jobs writing to S3 may lead to S3 rate being limited
* YARN core nodes may be terminated and new ones created silently if e.g. HDFS storage exceeds capacity. This will cause job to die eventually but slowly.
