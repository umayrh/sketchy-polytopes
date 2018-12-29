# Systems

## Themes

### Architecture

#### Evolutionary architectures

"Our definition of evolutionary architecture implies incremental change, meaning 
the architecture should facilitate change in small increments... We discuss two 
aspects of incremental change: development, which covers how developers build 
software, and operational, which covers how teams deploy software."
[More](https://files.thoughtworks.com/pdfs/Books/Building+evolutionary+architecture.pdf)

### Documentation

#### How-to and why-so

"Put another way: ‘code tells how, docs tell why.’ Code is constantly changing, 
so the more code you put into your docs, the faster they’ll go stale. To codify 
this further, let’s use the term “how-doc” for operational details like code 
snippets, and “why-doc” for narrative, contextual descriptions  3. We can mitigate 
staleness by limiting the amount we mix the how-docs with the why-docs."
[More](https://codeascraft.com/2018/10/10/etsys-experiment-with-immutable-documentation/)

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
