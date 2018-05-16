# Sketches for Haskell

> And when the Monad has decided, the thing will be done... (C. W. Leadbeater)

## History

* J. Backus. Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs. 
[link](https://www.thocp.net/biographies/papers/backus_turingaward_lecture.pdf)

* P. Hudak, J. Hughes, S. P. Jones, P. Wadler. A History of Haskell: Being Lazy with Class. [link](http://haskell.cs.yale.edu/wp-content/uploads/2011/02/history.pdf)
** Haskell is lazy
** Haskell is pure
** Haskell is statically typed

## Sketch

* Compositional laws
** Left identity: `id . f = f`
** Right identity: `f . id = f`
** Associativity: (f . g) . h = f . (g . h)

* Functions: `:i (->)`
** Definitions:
*** `id :: (a -> a)`
*** `(.) :: (b -> c) -> (a -> b) -> (a -> c)`
** Currying and Partial application
** Function "$": application
** Function ".": composition

* Functors: `:i Functor`
** Definitions:
*** `fmap :: (a -> b) -> (f a -> f b)` 
** Laws:
*** Identity: `fmap id = id`
*** Composition: `fmap (f . g) = fmap f . fmap g`

* Applicative functor: `:i Applicative`
** Definitions:
*** `pure :: a -> f a`
*** `(<*>) :: f (a -> b) -> fa -> fb`
** Laws:
*** Identity: `pure id <*> f = f`
*** Homomorphism: `pure f <*> pure x = pure (f x)`
*** Interchange: `f <*> pure x = pure ($ x) <*> f`
*** Composition: `pure (.) <*> f <*> g <*> x = f <*> (g <*> x)`

* Semigroup: `:i Semigroup`

* Monoid

* Monad

* Group

* Ring

* Field
