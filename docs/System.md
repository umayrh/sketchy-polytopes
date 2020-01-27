# Systems
## Themes
### Concepts
* [Linearizability](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf)
  * [Consistency models](https://aphyr.com/posts/313-strong-consistency-models)
* Distributed Consensus
  * [Raft](http://thesecretlivesofdata.com/raft/)
* Reading:
  * [Seminar](http://muratbuffalo.blogspot.com/2016/11/my-distributed-systems-seminars-reading.html)
  * [Papers, Love](https://github.com/yoavrubin/papers-i-love)

### Formal methods
#### Category Theory and Applications
* [Applied Category Theory](http://www.appliedcategorytheory.org)
* [Categorical Query Language](https://www.categoricaldata.net)
  * [Categorical Databases](https://www.categoricaldata.net/cql/Kensho-CategoricalDatabases_20190227.pdf)

#### TLA+, PlusCal
* [Lamport](http://lamport.azurewebsites.net/tla/high-level-view.html)
  * `brew cask install tla-plus-toolbox`
* [HLC in TLA](http://muratbuffalo.blogspot.com/2015/01/my-experience-with-using-tla-in.html)
* [CAS-Paxos](http://tbg.github.io/single-decree-paxos-tla-compare-and-swap)
* [Overview](https://github.com/osoco/pluscal-overview)
* [Formal methods at AWS](https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf)

#### Alloy
* [Case studies](http://alloytools.org/citations/case-studies.html)

### Architecture
#### Learning to build distributed systems
* [Marc Brooker](https://brooker.co.za/blog/2019/04/03/learning.html)
* [Postmortems, Dan Luu](https://danluu.com/postmortem-lessons/)
* [Theory, Henry Robinson](https://www.the-paper-trail.org/post/2014-08-09-distributed-systems-theory-for-the-distributed-systems-engineer/)
* [Notes, Jeff Hodges](https://www.somethingsimilar.com/2013/01/14/notes-on-distributed-systems-for-young-bloods/)
* [The Architecture of Open Source Applications](aosabook.org/en/index.html), [AOSA-Github](https://github.com/aosabook)

#### Evolution, Diversity, Robustness, Flexibility
"Our definition of evolutionary architecture implies incremental change, meaning 
the architecture should facilitate change in small increments... We discuss two 
aspects of incremental change: development, which covers how developers build 
software, and operational, which covers how teams deploy software."
[More](https://files.thoughtworks.com/pdfs/Books/Building+evolutionary+architecture.pdf)

"Suppose we have several independently implemented systems all designed to solve the same 
(imprecisely specified) general class of problems. Assume for the moment that each design is 
reasonably competent and actually correctly works for most of the problems that might be 
encountered in actual operation.  We know that we can make a more robust and reliable system 
by combining the given systems into a larger system"
[Robust Design](https://github.com/yoavrubin/papers-i-love/blob/master/philosophy/Sussman-Robust_Design_Through_Diversity.pdf); 
[Flexible Systems, The Power of Generic Operations](https://vimeo.com/151465912)

### Documentation
#### How-to and why-so
"Put another way: ‘code tells how, docs tell why.’ Code is constantly changing, 
so the more code you put into your docs, the faster they’ll go stale. To codify 
this further, let’s use the term “how-doc” for operational details like code 
snippets, and “why-doc” for narrative, contextual descriptions  3. We can mitigate 
staleness by limiting the amount we mix the how-docs with the why-docs."
[More](https://codeascraft.com/2018/10/10/etsys-experiment-with-immutable-documentation/)

### Metrics
### Linux Performance Metrics
* [Linux Performance](http://www.brendangregg.com/linuxperf.html)

## Problems
#### Cache congestion
"Every time a model was saved or deleted, the delete_cache method was called. 
This method performed a wildcard string search on every key in the cache 
(ElastiCache in staging and production, flat files in dev and test), deleting 
strings that matched. And of course, the model saved after every CREATE or INSERT 
statement, and was removed on every DELETE. That added up to a lot of 
delete_cache calls." 
[More](http://thedailywtf.com/articles/cache-congestion)

#### Single-line socket-reads
"Since rolling back the OS patch in production was never going to happen at 3AM, 
we wound up grepping through every line of code of that application and replacing 
all of the single-line socket-reads with the proper loop, with appropriate error 
checking:..." [More](https://thedailywtf.com/articles/assumptions-are-the-mother-of-all-bugs)

## References
[The Daily WTF](https://thedailywtf.com)
[ACM Queue](https://queue.acm.org)
