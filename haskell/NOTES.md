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

![Haskell Typeclass Hierarchy](etc/typeclassopedia-diagram.png "Haskell typeclass hierarchy [5]")

* Compositional laws  
    * Left identity: `id . f = f`  
    * Right identity: `f . id = f`  
    * Associativity: `(f . g) . h = f . (g . h)`  
    * Commuting diagrams
        * Commuting triangles (association) and commuting loops (identity).

* Categories
    * "Much of the power of category theory rests in the fact that it reflects on itself."
    * A triune theory:
        * Category: a collection of objects and a collection of morphisms. The domains and combinations of morphisms obey compositional laws.
        * Functor: maps each object and each morphism in a category to another category such that the mapping obeys compositional laws.
        * Natural transformation: maps each functor and each morphism on functors such that the mapping obeys compositional laws (the commuting square).
            * Vertical composition: association across functors
            * Horizontal composition: identification across categories
    * Category theory vs. set theory: 
 
        | Set theory | Category theory |  
        |------------|-----------------|  
        | membership | -               |  
        | sets       | categories      |  
        | elements   | objects         |  
        | -          | morphisms/arrows |  
        | functions  | functors        |  
        | equations between elements | isomorphisms between objects |  
        | equations between sets | equivalences between categories |  
        | equations between functions | natural transformations between functors |  

* Morphism: `:i (->)`  
    * Definitions:  
        * `id :: (a -> a)`  
        * `(.) :: (b -> c) -> (a -> b) -> (a -> c)`  
    * Curio:
        * Currying and Partial application  
            * Functions with multiple arguments are _curried_ i.e. transformed into functions with one or none argument: `(+) :: a -> a -> a`
            * This allows _partial application_ i.e. extracting functions of fewer arguments: `inc = (+1)`
        * Application: `:i $`
        * Composition: `:i .`

<p align="center"> <img src="etc/morphism-composition.png" alt="Morphism composition [3]"/></p>


* Functors: `:i Functor`  
    * Definitions:  
        * `fmap :: (a -> b) -> (f a -> f b)`   
    * Laws:  
        * Identity: `fmap id = id`  
        * Composition: `fmap (f . g) = fmap f . fmap g`  
    * Curio:
        * Collections
            * Lists, sets and powersets are all examples of the  mathematical functor. Set is not a functor in Haskell because it requires objects to comparable to each other while `fmap` must be applicable to any type. Classes that constrain input types can extend e.g. `Foldable`
            * Functors also represent infinite collections or computations (e.g. the recursion `ones = 1 : ones`
        * Not-a-Functor
            * 

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
        * "`Functor` allows us to lift a “normal” function to a function on computational contexts. But `fmap` doesn’t allow us to apply a function which is itself in a context to a value in a context"
        * `(*2) . (*5) . [1, 2, 3]` vs `pure((*2) . (*5)) <*> [1, 2, 3]` vs `fmap ((*2) . (*5)) [1, 2, 3]`

* Semigroup: `:i Semigroup`  

* Monoid  

* Monad  
    * Definitions:  
    * Laws:  
    * Types:
        * Powerset, List 
        * IO Monad  
        * Free Monad  

* Group  

* Ring  

* Field  

## References

1. [The nLab](https://ncatlab.org/nlab/show/HomePage)
2. https://wiki.haskell.org/Category_theory
3. https://en.wikibooks.org/wiki/Haskell/Category_theory
4. https://www.haskell.org/tutorial/index.html
5. https://wiki.haskell.org/Typeclassopedia
