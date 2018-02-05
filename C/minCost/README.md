# Minimum-cost optimization using GLPK

## Build and run

To build, run `./gradlew clean mainExecutable`. 

To execute, run `./build/exe/main/main`.

## Performance

System specs:

```
      Processor Name: Intel Core i7
      Processor Speed: 1.7 GHz
      Number of Processors: 1
      Total Number of Cores: 2
      L2 Cache (per Core): 256 KB
      L3 Cache: 4 MB
      Memory: 8 GB
```

|           Task        |   (50K, 90K, 25K)  |  (50K, 90K, 250K)  | (100K, 100K, 100K) |
| ----------------------|:------------------:|:------------------:|:------------------:|
| glp_netgen            |       3.5s         |        3.2s        |     10.6s          |
| glp_mincost_relax4    |       24.9s        |      1261.6s       |     659.4s         |

The tuple (N, A, S) represents a problem instance, where:

N = number of nodes
A = number of arcs
S = total supply

## References

* [GLPK](https://www.gnu.org/software/glpk/)
* [GLPK Wikibook](https://en.wikibooks.org/wiki/GLPK)
* [GLPK Graph and Network Routines](http://www.chiark.greenend.org.uk/doc/glpk-doc/graphs.pdf)
* [DIMACS Implementation Challenge: Network Flows and Matchings](http://dimacs.rutgers.edu/pub/netflow/)
* [DIMACS-Graphviz](https://gist.github.com/maelvalais/755c16db4681e3a671c1)
* [MIT 15-082j](https://ocw.mit.edu/courses/sloan-school-of-management/15-082j-network-optimization-fall-2010/)
* [Network Programming, Katta Murty](http://www-personal.umich.edu/~murty/books/network_programming/)

## TODO

* Use glp_netgen to test performance to large graphs
* Update the dimacs_to_dot.py script
* Better variable names
* Function for extracting the solution
* Function for converting a custom input in to DIMACS. Format:
```
    producer_id capacity
    ...
    consumer_id capacity
    ...
    producer_id consumer_id cost
    ...
```
* Create unit test
* Hook up project with Travis
* Rename binary, create library, update gradle.build
* Ribify GLPK?
