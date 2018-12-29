## Mac

Assuming `brew` is installed:

* Install XCode: `xcode-select --install`
* Install Java: `brew cask install java`
* Install Scala: `brew install scala`

To install Apache Spark:

* `brew install apache-spark`

Update system environment variables with:

```
export SPARK_HOME=`brew info apache-spark | grep /usr | tail -n 1 | cut -f 1 -d " "`/libexec
```
