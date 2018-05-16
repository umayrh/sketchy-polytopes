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
Prelude> f a b = a + b 
Prelude> :t f
f :: Num a => a -> a -> a
``` 

* Quit using `:q`

### Docs

* [Main](https://www.haskell.org/documentation)
* Haskell [Wikibook](https://en.wikibooks.org/wiki/Haskell)
* Haxl [README](http://hackage.haskell.org/package/haxl-0.5.1.0#readme)

### Reading

#### Haskell

* B. O'Sullivan, D. Stewart, J. Goerzen. Real World Haskell. [link](http://book.realworldhaskell.org/read/)
* S. Marlow. Fun With Haxl. [link](https://simonmar.github.io/posts/2015-10-20-Fun-With-Haxl-1.html)
* P. Fraenkl. Parallelize all the things -- Deconstructing Haxl, with Clojure macros, topological sorting and Quasar fibers. [link](http://blog.podsnap.com/qaxl.html)
* T. van Laarhoven. Dependently typed DAGs [link](https://www.twanvl.nl/blog/haskell/dependently-typed-dags)

#### Functional programming

* M. P. Jones, L. Duponcheel. Composing Monads [link](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.42.2605)
* Functional Programming with Structured Graphs ([slides](http://www.cs.nott.ac.uk/~psxbv/Away_Day/fplad12-talk_henrik.pdf), 
[paper](https://www.cs.utexas.edu/~wcook/Drafts/2012/graphs.pdf))
* Y. Kashiwagi, D. S. Wise. Graph Algorithms in a Lazy Functional Programming Language. [link](https://www.cs.indiana.edu/pub/techreports/TR330.pdf)
* M. I Cole. Algorithmic Skeletons: Structured Management of Parallel Computation. [link](https://homepages.inf.ed.ac.uk/mic/Pubs/skeletonbook.pdf)
* S. Marlow, R. Newton, S. P. Jones. A Monad for Deterministic Parallelism. [link](https://simonmar.github.io/bib/papers/monad-par.pdf)
* D. Ancona, E. Moggi. Program Generation and Components. [link](https://www.disi.unige.it/person/MoggiE/ftp/fmco04.pdf)
* nLab. Monads (in Computer Science). [link](https://ncatlab.org/nlab/show/monad+%28in+computer+science%29)

##### Incremental programming

* U. A. Acar, G. E. Blelloch, R. Harper. Adaptive Functional Programming. [link](https://www.cs.cmu.edu/~guyb/papers/popl02.pdf)
* D. Firsov, W. Jeltsch. Purely Functional Incremental Programming. [link](http://firsov.ee/incremental/incremental.pdf)
* M. Carlsson. Monds for Incremental Computing. [link](https://pdfs.semanticscholar.org/e001/67331939e77aa41cdb86712583b8f70c493d.pdf)

