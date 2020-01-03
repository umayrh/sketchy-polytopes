# Un Sinuoso Laberinto Creciente

> Para la otra vez ... le prometo ese laberinto, que consta de una sola línea recta y que es indivisible, incesante. (_La muerte y la brújula_)

### Projects

#### Documentation

* Aim: help connect documents across projects? At least, Markdown docs.
  * Connect Github with [Gitbook](https://umayrh.gitbook.io/docs/)
  * Markdown, and static site gen. [Jekyll](https://github.com/jekyll/jekyll)?
  * [bookdown](https://bookdown.org/yihui/bookdown/)?
 
#### Infrastructure

* Move to Py3.7
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
#### 2020-01-03
* Updated Scala build since https://github.com/alenkacz/gradle-scalafmt/issues/32 was resolved

#### 2020-01-02
* Created https://github.com/alenkacz/gradle-scalafmt/issues/32

#### 2020-01-01
* Premature celebration of the fix. The build works locally because of caching. Can reproduce when 
`gradle --refresh-dependencies -p scala clean build` ([thanks](http://blog.defun.work/post-75169d14-c64b-4ff4-be46-47747911d348.html)).
* It's cz.alenkacz:gradle-scalafmt 1.6.0->1.10.0 that's causing issues..

#### 2019-21-31
* Finally fixed the Travis build. The build.gradle was definitely buggy but maybe just leaving mavenCentral()
  also helped (?). Here's the Gradle red herring error:
  ```
  Caused by: java.lang.NullPointerException: Username must not be null!
  	at com.google.common.base.Preconditions.checkNotNull(Preconditions.java:910)
  	at org.gradle.internal.resource.transport.http.ntlm.NTLMCredentials.<init>(NTLMCredentials.java:36)
  	at org.gradle.internal.resource.transport.http.HttpClientConfigurer.useCredentials(HttpClientConfigurer.java:197)
  	at org.gradle.internal.resource.transport.http.HttpClientConfigurer.configureCredentials(HttpClientConfigurer.java:139)
  	at org.gradle.internal.resource.transport.http.HttpClientConfigurer.configure(HttpClientConfigurer.java:109)
  	at org.gradle.internal.resource.transport.http.HttpClientHelper.getClient(HttpClientHelper.java:195)
  ``` 
* Also updated the Scala tests to be compatible with new versions. Unfortunately, ScalaTest seems to have removed
support for JUnit testing without warning or documentation. So, can't run scala tests from IntelliJ for now.
#### 2019-21-30
* Can now publish on [Sonatype](https://issues.sonatype.org/browse/OSSRH-54178). See also 
[this](https://medium.com/@nmauti/sign-and-publish-on-maven-central-a-project-with-the-new-maven-publish-gradle-plugin-22a72a4bfd4b).

#### 2019-12-24 - 27
* Add repo for Github pages. `https://umayrh.github.io` 
* Set up Ruby dev, Jekyll and all.
  * `brew install ruby`
  * `brew install rbenv`
  * `rbenv install 2.6.5`
  * `rbenv global 2.6.5`
  * `gem install --user-install bundler jekyll`
  * `bundle update`
  * `bundle exec jekyll build`
  * `bundle exec jekyll serve`
  * Links: [Jekyll](https://jekyllrb.com/docs/), 
    [Github](https://help.github.com/en/github/working-with-github-pages/setting-up-a-github-pages-site-with-jekyll)
* Prep site
  * Update _contacts.yml
  * Export data form Wordpress
  * `brew install npm` + lonekorean/wordpress-export-to-markdown.git 
  * `node index.js --input ~/Downloads/umayrh.wordpress.com-2019-12-25-00_54_53/sketchespolytopes.wordpress.2019-12-25.001.xml --prefixdate`
  * ... lots of painful wrangling with getting Github and Jekyll custom plugins to work together, but ...
  * Build on Netlify, and redirect umayrh.github.io to Netlify. Since barber-jekyll's custom plugins cause build failure on Github. 
  * Clean up all posts - fix LaTeX and layout.

#### 2019-12-21 - 23
* Install PostGres and ELasticStalk
  * Add `/Library/PostgreSQL/12/bin/` to PATH. Can’t run psql otherwise
* Rebuild repo
  * Done: installed Xcode, jdk13, jdk8, neo4j, apache-spark
  * `gradle wrapper --gradle-version 6.0.1`
  * Install and set up neo4j. Fix pivy-importer and submit a PR (https://github.com/linkedin/pygradle/pull/335)
  * Renamed `python/_template/build.gradle` to `_build.gradle` cuz it won’t build otherwise
  * Rcpp 0.12.x wouldn’t built. Upgraded to 1.0.3. Remove all installed packrat lib+src, and manually updated packrat.lock. 
    Fixed packrat.opts - added `symlink.system.packages = TRUE` and set external packages
  * `brew install rustup` + `rustup-init` `https://sourabhbajaj.com/mac-setup/Rust/`
  * Scala package updated. Still Error: Could not find or load main class org.scalatest.tools.Runner. Needed to make scalacheck a testImplementation dependency and Scala-lib api
  * Same for sparkScala but also testImplementation for scalacheck 
  * Installed Lemon: `wget http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz` and `brew install cmake glpk doxygen graphviz ghostscript ` for Lemon build.
  * Also, SOPLEX https://soplex.zib.de/index.php#download though Lemon doesn’t compile with it
  * Travis errors:
    * Spark mirror had moved. Updated.
    * R woes:
    * Updating rUtils documentation
    ```
    8180 Writing NAMESPACE
    8181 Loading rUtils
    8182 Error: Dependency package(s) 'pryr' not available.
    8183 <error/rlang_error>
    8184 Dependency package(s) 'pryr' not available.
    8185 Backtrace:
    8186    █
    8187  1. └─devtools::document()
    8188  2.   ├─withr::with_envvar(...)
    8189  3.   │ └─base::force(code)
    8190  4.   └─roxygen2::roxygenise(pkg$path, roclets, load_code = load_code)
    8191  5.     └─roxygen2:::load_code(base_path)
    8192  6.       └─pkgload::load_all(path, helpers = FALSE, attach_testthat = FALSE)
    8193  7.         └─pkgload:::load_imports(path)
    8194  8.           └─pkgload:::abort_for_missing_packages(res, imports$package)
    8195 In addition: Warning message:
    8196 In (function (dep_name, dep_ver = "*")  :
    8197   Dependency package 'pryr' not available.
    8198
    ```
  * `brew cask install basictex` + put `/usr/local/texlive/2019basic/bin/x86_64-darwin/` in PATH + 
    * `sudo tlmgr install inconsolata`
    * `sudo tlmgr update --self`
    * `sudo tlmgr update --all`
    * `sudo tlmgr install helvetic`
    * `sudo tlmgr install letltxmacro`
  * Finally, `R CMD Rd2pdf man` works successfully
  * `R CMD build . && R CMD check rUtils_0.1.0.tar.gz` 
  * `cat(packrat:::appDependencies(), sep = " ")`, and reinstalled all dependencies. 
  * Already updated travis-setup.sh to installed R 3.6.2, updated packrat.opts
    to remove local.repos, and DESCRIPTION to remove data.table from REQUIRES.

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
