# Un Sinuoso Laberinto Creciente

> Para la otra vez ... le prometo ese laberinto, que consta de una sola línea recta y que es indivisible, incesante. (_La muerte y la brújula_)

## TODO
* CI: Travis 
    * Set up matrix builds with [multiple os](https://docs.travis-ci.com/user/multi-os/) and [multiple 
languages](https://stackoverflow.com/questions/27644586/how-to-set-up-travis-ci-with-multiple-languages)
* Deployment: Docker, Terraform, Kubernetes
    * [No-VM Kubernetes](https://blog.travis-ci.com/2017-10-26-running-kubernetes-on-travis-ci-with-minikube)
* Documentation:
    * Can [bookdown](https://bookdown.org/yihui/bookdown/) help connect documents across projects? At least,
    Markdown docs.
* Algorithms:
    * Min-cost network flow implemented with data structures using space-filling curve
    * Series-parallel graph converter
* Programming:
    * Haskell
    * Scalaz

### 2018-06-30

* Integrate with PyGradle. Some heartache. 
* Skeleton for Python project, `evolvingdags`. The idea is to use [Networkx](https://networkx.github.io) to 
create a time series of (randomly generated) directed acyclic graphs (DAG), and then to
store the graph in Neo4j. The intended application is performance evaluation of data pipelines.

### 2017-10-20
* Create a Scala package `testingParadigms` that uses ScalaTest, ScalaCheck, Junit and Hamcrest 
    * Outline a possible Gradle template for Java/Scala projects 
    * Encode some testing paradigms 
