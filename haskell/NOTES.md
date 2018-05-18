# Sketches for Haskell

> ...il est vrai que l’appétit ne saurait toujours parvenir entièrement à toute la perception, où il tend, mais il en obtient toujours quelque chose, et parvient à des 
perceptions nouvelles. (G. W. Leibniz)

## History

* J. Backus. Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs. 
[link](https://www.thocp.net/biographies/papers/backus_turingaward_lecture.pdf)  
    * Programming models  
       * Foundations: tersness, completeness  
       * History sensitivity: states are not programs  
       * Abstraction: process is not computation  
    * von Neumann architecture  
       * Programming language replicates machine architecture  
       * "The assignment statement is the von Neumann bottleneck of programming languages and keeps us thinking in word-at-a-time terms..."  
       * Statements vs expressions: imperatives vs compositions  
       * "Applicative computing systems' lack of storage and history sensitivity is the basic reason they have not provided a foundation for computer design." (cf. FPGA)  
    * Framework, composable parts, combining forms  
        * "Let us distinguish two parts of a programming language. First, its _framework_ gives the overall rules of the system, and second, its changeable parts, whose existence is anticipated by the framework but whose particular behavior is not specified by it."
        * "Perhaps the most important element in providing powerful changeable parts in a language is the availability of combining forms that can be generally used to build new procedures from old ones."

* P. Hudak, J. Hughes, S. P. Jones, P. Wadler. A History of Haskell: Being Lazy with Class. [link](http://haskell.cs.yale.edu/wp-content/uploads/2011/02/history.pdf)  
    * Haskell is lazy  
    * Haskell is pure  
    * Haskell is statically typed  

## Sketch

* Compositional laws  
    * Left identity: `id . f = f`  
    * Right identity: `f . id = f`  
    * Associativity: (f . g) . h = f . (g . h)  

* Functions: `:i (->)`  
    * Definitions:  
        * `id :: (a -> a)`  
        * `(.) :: (b -> c) -> (a -> b) -> (a -> c)`  
    * Currying and Partial application  
    * Function "$": application  
    * Function ".": composition  

* Functors: `:i Functor`  
    * Definitions:  
        * `fmap :: (a -> b) -> (f a -> f b)`   
    * Laws:  
        * Identity: `fmap id = id`  
        * Composition: `fmap (f . g) = fmap f . fmap g`  
    * Curio:
        * List is functor but not Set since Set is only defined over equatable types, and hence restricts functions defined on it

* Applicative functor: `:i Applicative`  
    * Definitions:  
        * `pure :: a -> f a`  
        * `(<*>) :: f (a -> b) -> fa -> fb`  
    * Laws:  
        * Identity: `pure id <*> f = f`  
        * Homomorphism: `pure f <*> pure x = pure (f x)`  
        * Interchange: `f <*> pure x = pure ($ x) <*> f`  
        * Composition: `pure (.) <*> f <*> g <*> x = f <*> (g <*> x)`  
    * Curio:
        * `(*2) . (*5) . [1, 2, 3]` vs `pure((*2) . (*5)) <*> [1, 2, 3]` vs `fmap ((*2) . (*5)) [1, 2, 3]`

* Semigroup: `:i Semigroup`  

* Monoid  

* Monad  
    * Definitions:  
    * Laws:  
    * Types:
        * IO Monad  
        * Free Monad  

* Group  

* Ring  

* Field  
