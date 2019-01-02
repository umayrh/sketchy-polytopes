# Un Sinuoso Laberinto Creciente

> Para la otra vez ... le prometo ese laberinto, que consta de una sola línea recta y que es indivisible, incesante. (_La muerte y la brújula_)

### Projects

#### Documentation

* Aim: help connect documents across projects? At least, Markdown docs.
  * Connect Github with [Gitbook](https://umayrh.gitbook.io/docs/)
  * Markdown, and static site gen. [Jekyll](https://github.com/jekyll/jekyll)?
  * [bookdown](https://bookdown.org/yihui/bookdown/)?
 
#### Infrastructure

* Continuous integration: Travis 
  * Set up matrix builds with [multiple os](https://docs.travis-ci.com/user/multi-os/) 
    and [multiple languages](https://stackoverflow.com/questions/27644586/how-to-set-up-travis-ci-with-multiple-languages)
* Deployment: Docker, Terraform, Kubernetes
  * [No-VM Kubernetes](https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube)

#### Algorithms:

* Min-cost network flow
* Space-filling curves
* Series-parallel graph
* Infer graph [classes](http://www.graphclasses.org/index.html) and 
  [properties](https://gap-packages.github.io/Digraphs/doc/chap6.html#X7ADDEFD478D470D5),
  or [network motifs](https://en.wikipedia.org/wiki/Network_motif). 
* [Causal discovery](http://ftp.cs.ucla.edu/pub/stat_ser/R156.pdf), counterfactual
  evaluation, and intervention effects.

#### Programming:

* Haskell
* Scalaz

### Log

#### 2019-01-01
* Fixed some sparktuner bugs. Stated doc for [causality](./Causality.md). Would like
  to figure out a good way to explore causal effects of Spark configs. 

#### 2018-12-29

* Need to a publish packages to internal and external repos. Maybe use Github
  release - see e.g. [this](https://www.victorhurdugaci.com/github-releases-travis). 
* Need a deployment story. See [this](https://medium.com/build-acl/docker-deployments-using-terraform-d2bf36ec7bdf).
* Investigate [AWS](https://aws.amazon.com/free/) and 
  [GCP](https://cloud.google.com/free/docs/gcp-free-tier) free tiers.

#### 2018-12-15

* Figure out how to map all CF templates using [cloudformation-graph](https://github.com/umayrh/cloudformation-graph)
* Revisit the [Datalog](https://github.com/frankmcsherry/blog/blob/master/posts/2018-05-19.md) abstraction for data flows
* Move from Wordpress to Github [pages](https://yunmingzhang.wordpress.com/2018/06/15/how-to-use-github-pages/#more-2128)?
* [Opentuner](http://opentuner.org/tutorial/setup/) for Spark
* ConceptQL to Spark mapping. 
  * [Indexing](http://hpc.isti.cnr.it/hpcworkshop2014/PartitionedEliasFanoIndexes.pdf) might be useful
  * Map a clinical protocol to a Spark SQL DAG
* Structured Causal Model framework for policy evaluation

#### 2018-06-31

* Flesh out [README.md](python/evolvingdag/README.md).

#### 2018-06-30

* Integrate with PyGradle. Some heartache. 
* Skeleton for Python project, `evolvingdags`. The idea is to use [NetworkX](https://networkx.github.io)
  to create a time series of (randomly generated) directed acyclic graphs (DAG), and then to
  store the graph in Neo4j. The intended application is performance evaluation of data pipelines.
* `pandoc --from=markdown --to=rst --output=README.txt README.md`

#### 2017-10-20
* Create a Scala package `testingParadigms` that uses ScalaTest, ScalaCheck, Junit and Hamcrest 
    * Outline a possible Gradle template for Java/Scala projects 
    * Encode some testing paradigms 
