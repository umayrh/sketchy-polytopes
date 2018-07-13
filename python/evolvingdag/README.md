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
Some tests require that a Neo4j server is running with default configuration.

## References

### Graph libraries

* [NetworkX](https://networkx.github.io)
* [NetworkX API for Neo4j Graph Algorithms](https://github.com/neo4j-graph-analytics/networkx-neo4j)

### Neo4j

* [NetworkX-Neo4j](https://medium.com/neo4j/experimental-a-networkx-esque-api-for-neo4j-graph-algorithms-4002baac45be)
* [The Neo4j Developer Manual](https://neo4j.com/docs/developer-manual/current)
* [Driver for Python](https://neo4j.com/docs/api/python-driver/1.6/index.html)
* [Files](https://neo4j.com/docs/operations-manual/current/configuration/file-locations/)
* [Embedded Database](https://neo4j.com/docs/java-reference/current/tutorials-java-embedded/)
* [Blog](https://maxdemarzi.com)

### Analysis

* [Longitudinal Networks](https://toreopsahl.com/tnet/longitudinal-networks/)
* [Longitudinal Methods of Network Analysis](https://www.stats.ox.ac.uk/~snijders/siena/Longi_Net.pdf)
* [Probabilistic Programming](http://www.probabilistic-programming.org/wiki/Home)

### Visualization

* [Social Network Image Animator](https://web.stanford.edu/group/sonia/index.html)
* [DAG Generator](http://daggenerator.com/#)
* [Visualization](http://www.forensicswiki.org/wiki/Tools:Visualization)
* [Gource](http://gource.io)

### Longest Path Problems

* F. Baccelli, M. Canales. Parallel Simulation of Stochastic Petri Nets using Recurrence Equations [link](https://hal.inria.fr/inria-00075042/PS/RR-1520.ps)
* E. Bahalkeh. Efficient Algorithms for Calculating the System Matrix and the Kleene Star Operator for Systems Defined by Directed Acyclic Graphs over Dioids [link](https://etd.ohiolink.edu/!etd.send_file?accession=ohiou1440116216&disposition=inline)
* L. Chen. Parallel simulation by multi-instruction, longest-path algorithms [link](https://dl.acm.org/citation.cfm?id=597975)
* C. A. Alexander et al. Near–Critical Path Analysis: A Tool for Parallel Program Optimization [link](citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.56.5220&rep=rep1&type=pdf)
* C-Q. Yang, B. P. Miller. Critical Path Analysis for the Execution of Parallel and Distributed Programs [link](ftp://ftp.cs.wisc.edu/paradyn/technical_papers/CritPath-ICDCS1988.pdf)
* L. Chen, R. F. Serfozo. Performance Limitations of Parallel Simulation [link](www.kurims.kyoto-u.ac.jp/EMIS/journals/HOA/JAMSA/11/3397.pdf)
