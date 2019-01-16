# Optimization

## People and Groups

* [Arkadi Nemirovski]()
* []

## Notes

#### Optimization techniques
* Newton’s method
  * Polyak’s paper on Kantorovich’s extension of Newton’s method to functional spaces (using Frechet derivative of nonlinear operators)
* Projection algorithms: Mirror prox

#### Diophantine approximation
* Strongly polynomial-time algorithms, KAM theory, Ergodicity, Discrepancy/approximation theory …
* Continued fractions, Euclid’s algorithm, randomization (?) …
* Multi-dimensional Euclid algorithm and basis reduction - any relation to Stern-Brocot?
  * Simultaneous diophantine approximation: Geometric Algorithms and Combinatorial Optimization, chap 5

#### Complementarity problems
* Relationship between LP, LCP and QP vis-a-vis minimax and Nash equilibriums
* Lemke-Howson algebra
  * Shapely, A note on the Lemke-Howson algorithm. Pivoting and extensions
    * Introduces the index of an equilibrium point, which is related to its stability. See Index and Stability in Bimatrix Games: A Geometric-Combinatorial Approach.
  * Avis, Rosenberg, Savani, Stengel, Enumeration of Nash equilibria for two-player games
* From Lemke-Howson to Scarf algorithm
* Smale on LCP in Algorithms For Solving Equations
* G. Isac, Topological Methods in Complementarity Theory (seem to give a more complete explanation of the relationship between LP, LCP and QP)

#### Harmonic analysis and convexity: 
* Can Fast Fourier Transform somehow be used to find the extremal points of a polyhedron?
  * Do FFT and separating hyperplane (Farkas Lemma) have any relationship?
* Vanderbei’s _Fast Fourier Optimization_
* _Convex Optimization in Normed Spaces: Theory, Methods and Examples_ 
* _Fourier Analysis and Convex Geometry_
* _Approximation Theory and Harmonic Analysis on Spheres and Balls_
* H. Groemer, _Fourier series and spherical harmonics in convexity_
* Frame and Bases - An Introductory Course
  * Bases in Hilbert space have expansion and uniques properties - frames don’t require the latter and can still represent functions well or better than bases

#### Concentration inequalities and convexity
* Could it be that concentration inequalities are essentially the reasons why...?
  * Gradient descent methods can be accelerated (Nesterov acceleration)
  * Gradient descent methods do not require accurate gradient estimates (Polyak averaging)
* Ailon-Chazelle transform uses FFT to speed up their Jordon-Lindenstrauss transform - is there a deeper connection based perhaps on the properties of certain normed spaces?

#### Generalized convexity
* Geometric programming
* AM-GM inequality
* Geodesic convexity
* Transforming convex functions to other convex functions
