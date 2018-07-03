# Evolving DAG

## Setup

This project requires a [Neo4j](https://neo4j.com) server installed and running.

### Neo4j

* Download a Neo4j [release](https://neo4j.com/download/other-releases/#releases)
* `tar -xf neo4j-community-VERSION-unix.tar`
* `export NEO4J_HOME=/path/to/neo4j-community-VERSION-unix`
* `$NEO4J_HOME/bin/neo4j console` (or `$NEO4J_HOME/bin/neo4j start` for background process)
* Visit `http://localhost:7474` to verify installation

See Neo4j [docs](https://neo4j.com/docs/operations-manual/current/installation/) for more details. Mac users 
can [automate](https://arstechnica.com/gadgets/2011/03/howto-build-mac-os-x-services-with-automator-and-shell-scripting/) Neo4j startup.
See also Travis [integration](https://docs.travis-ci.com/user/database-setup/#Neo4j).

## Build

`gradle build` should install all dependencies (including projects-specific ones in requirements.txt), and run tests.

## References

* [NetworkX](https://networkx.github.io)
* [NetworkX API for Neo4j Graph Algorithms](https://github.com/neo4j-graph-analytics/networkx-neo4j)
* [NetworkX-Neo4j](https://medium.com/neo4j/experimental-a-networkx-esque-api-for-neo4j-graph-algorithms-4002baac45be)
* [Longitudinal Networks](https://toreopsahl.com/tnet/longitudinal-networks/)
* [Longitudinal Methods of Network Analysis](https://www.stats.ox.ac.uk/~snijders/siena/Longi_Net.pdf)
* [Social Network Image Animator](https://web.stanford.edu/group/sonia/index.html)
* [DAG Generator](http://daggenerator.com/#)
* [Probabilistic Programming](http://www.probabilistic-programming.org/wiki/Home)
