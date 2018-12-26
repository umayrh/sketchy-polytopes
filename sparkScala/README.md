# Spark-Scala projects

## New project

Gradle expects the following directory structure by default:
* `src/main/java` Production Java source.
* `src/main/resources` Production resources, such as XML and properties files.
* `src/main/scala` Production Scala source. May also contain Java source files for joint compilation.
* `src/test/java` Test Java source.
* `src/test/resources` Test resources.
* `src/test/scala` Test Scala source. May also contain Java source files for joint compilation.

To quote Gradle: "All the Scala source directories can contain Scala and Java code. 
The Java source directories may only contain Java source code. None of these 
directories need to exist or have anything in them; the Scala plugin will simply 
compile whatever it finds."

## References

* [Gradle Scala plugin](https://docs.gradle.org/current/userguide/scala_plugin.html)
