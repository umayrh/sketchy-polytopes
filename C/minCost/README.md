# Minimum-cost optimization using GLPK

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
