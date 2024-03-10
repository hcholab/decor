
# NOTES: Investigate the followings:

* For instance, here some terms, should have different weights:

  We can randomized term selection by biasing the selection towards the terms with higher weights. How do we find the weights? In the probablistic case, we can find a lower bound to find the terms. Do we have a corpus of mathmatical functions? 

  ```python
  [sin(x), sin(y), sin(x*y), sin(x**2), sin(y**2), sin(sqrt(x)), sin(sqrt(y)), cos(x), cos(y), cos(x*y), cos(x**2), cos(y**2), cos(sqrt(x)), cos(sqrt(y)), tan(x), tan(y), tan(x*y), tan(x**2), tan(y**2), tan(sqrt(x)), tan(sqrt(y))]
  ```

* There should be also inner coefficients for each term. For instance, for `sin(x)`, we should have `c * sin(a*x)`. We can linearize `a*x` by introducing a new variable `z` and adding a constraint `z = a*x` as a new linear equation. Then, we can replace `c2*x` with `z`. 

* (DONE) Zero bias in sampling
* (DONE) Select a complex term and block it and solve again.
         complexity is measured by the number of variables in the term.
* (DONE) Add constant term to MILP approach.
* (DONE) Optimal Objective Value is a good measure of correctness.
* (DONE) Does the scaleing heuristics work for all cases?
         No, therefore we can create two MILP instances, one with scaling and one without.

* (DONE) Add correctness check to MILP after finding the property.

* (DONE) The coefficient interval is [-2, 2]. Is it enough? We should try bigger ones
         incrementally and see if the solver can find the optimal solution.

* We should repeat degrees from 1, 2, and 3 as Timos does in linear regression.
* We should traverse the important terms as Timos does in linear regression.
* (DONE) For each MILP run, we need to set a timeout of 30 seconds.

* (DONE) I feel we shouldn't increase the number of samples (30 is good) This is my observation.
         At some point, Vu also mentioned something similar.

* (DONE) We should try different input distributions.
         For small domains, and for polynomials, we should adjust the distribution.

* (DONE) Try it with arbitrary polynomials.
         Develop polynomial generator.

* Try Timos' new idea in Linear Regression: remove terms whose coefficients are less than the threshold, block them and solve again with Linear Regression. 

# Selling Points: 
Self-Correcting and Self-Testing.
Compare this with DIG approach:

1. Current nonlinear synthesizers does not support real-valued functions.
2. This method is black-box. It doesn't need to know the implemention of function.
3. This method uses new heuristics to find the optimal solution.
  It's not just a simple MILP.
   It supports elementary functions.
   It pivots the selected term.
   It (de)scales the input using a heuristic.
   It uses a MILP solver with small bursts.
   It uses the objective function error as a measure of correctness.
   If the implementation is given, it can be used to prove the correctness of the property.

