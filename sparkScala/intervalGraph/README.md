# Interval Graphs

"An interval graph is a subtree graph which has a intersection model whose underlying tree is a line." (1)

Some interesting applications (2-4) of [intervals graphs](https://en.wikipedia.org/wiki/Interval_graph) include:

* Given observations with start and end dates, grouping ones that overlap.
* Given tasks with stat and end dates, assigning them to executors without multi-tasking.
* Given partial reads from an unknown genome, reassembling the genome assuming read overlaps are known.
* Given a set of traffic streams and a definition of compatible traffic streams, phasing traffic lights for compatible streams.

## Two properties

###  Chordality

All cycles in interval graphs of 4 or more vertices have a _chord_ (aka _short-cut_, _short_circuit_) i.e. an edge 
that connects two vertices of cycle but isn't itself a part of the cycle. This makes every interval graph a kind of
[chordal graph](https://en.wikipedia.org/wiki/Chordal_graph), and a [simplicial complex](https://en.wikipedia.org/wiki/Simplicial_complex).

Intuitively, if in an interval graph, vertex _a_ is connected to _b_ and _c_, and vertex _d_ is connected to _b_ and _c_, then _a_ and _d_
must be connected since intersections of subintervals of the real line, under semi-order, form a transitive closure.

### Perfect elimination ordering

Precisely because interval graphs have _cliques_, there exists a scheme for removing all the vertices of the graph by removing one simplicial
vertex, i.e. a vertex in a clique, at a time. Thus, removing a _simplicial vertex_ (i.e. a vertex in a clique) in an interval graph results in another interval graph. Hence,
there exists an ordering, or a scheme, or simplicial vertex for an interval graph such that removing vertices in that ordering results in
the extinction of the graph. This property makes interval graphs a subclass of [perfect graphs](https://en.wikipedia.org/wiki/Perfect_graph).

## Three problems

A perfect elimination ordering can allow solving three graph problems in polynomial time:

* minimum graph coloring
* maximum clique
* maximum independent set

This is because, for interval graphs, (1) the chromatic number equals the maximum clique size, and (2) perfect elimination ordering arrange all cliques in a complete cover.

## An O(n)-time algorithm

An algorithm that can find all maximal cliques in an interval graph also trivially solves the three problem mentioned before. Here's an O(n)-time for it:

Given: 
* a table of observations, `n` in size, each with some interval within [0, 1]
* a definition of overlap between any two given intervals
* an encoding of each interval with a binary word of fixed length, `W`


```
* In one pass, transform each interval into an (possibly, encoded) bitset
* In one pass, take a union across all bitsets to create a distinct union-ed bitset
* 
* In one pass, for each bitset:
** 

```

## References

(1) T. Kashiwabara. "Algorithms for Some Intersection Graphs" [link](https://pdfs.semanticscholar.org/cd29/05237ab92257718f798c15626a917855ee14.pdf)
(2) J. E. Cohen, J. Komlos, and T. Mueller. "The Probability of an Interval Graph, and Why It Matters" 
[link](http://lab.rockefeller.edu/cohenje/PDFs/066CohenKomlosMuellerProcSymposPureMath1979.pdf)
(3) A. Hertz, "Quick on the Draw" [link](http://www.polymtl.ca/pub/sites/lagrapheur/en/index.php)
(4) F. S. Roberts. "Graph Theory and Its Applications to Problems of Society"
