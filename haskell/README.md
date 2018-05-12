# Haskell

> That is the fundamental point: algorithms are defined on algebraic structures... To deal with the real problems you need multisorted algebras - families of interfaces 
that span multiple types. [A. Stepanov](http://www.stlport.org/resources/StepanovUSA.html)

## Install

### Platform-specific installation

See [Haskell Platform](https://www.haskell.org/platform/) for details.

MacOS:

* `brew cask install haskell-platform`

Linux - Ubuntu

* `sudo apt-get install haskell-platform` 

### Verify

* Run GHCi, the Glasgow Haskell Compiler (interactive):

```
$ ghci
GHCi, version 8.2.2: http://www.haskell.org/ghc/  :? for help
Prelude> f a b = a ++ ", " ++ b
Prelude> f "OK" "Computer"
"OK, Computer"
``` 

* Quit using `:q`

### Docs

* [Main](https://www.haskell.org/documentation)
* Haskell [Wikibook](https://en.wikibooks.org/wiki/Haskell)

### Reading

* Mark P. Jones, Luc Duponcheel. Composing Monads [link](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2605)
* T. van Laarhoven. Dependently typed DAGs [link](https://www.twanvl.nl/blog/haskell/dependently-typed-dags)
* Functional Programming with Structured Graphs ([slides](http://www.cs.nott.ac.uk/~psxbv/Away_Day/fplad12-talk_henrik.pdf), 
[paper](https://www.cs.utexas.edu/~wcook/Drafts/2012/graphs.pdf))
* Y. Kashiwagi, D. S. Wise. Graph Algorithms in a Lazy Functional Programming Language. [link](https://www.cs.indiana.edu/pub/techreports/TR330.pdf)
* M. I Cole. Algorithmic Skeletons: Structured Management of Parallel Computation. [link](https://homepages.inf.ed.ac.uk/mic/Pubs/skeletonbook.pdf)
* S. Marlow, R. Newton, S. P. Jones. A Monad for Deterministic Parallelism. [link](https://simonmar.github.io/bib/papers/monad-par.pdf)
