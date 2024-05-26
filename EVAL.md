# Learning Nonlinear Invariants using Regression Analysis and Dimensionality Reduction

# Evaluation of Bitween Framework
=================================

## TABLE -- Comparison with DIG and SymInfer -- nla-digbench comparison (invariant generation for integer benchmarks) --

Trace Locs.: Number of trace locations (vtrace)
Max. Deg.: Maximum degree of the invariants
Trace Vars.: Number of trace variables that 
Type of Program: Integer, Double, and Mixed

|-------------------|--------------------------------||----------------------------||-------------------------||-----------------------------||
|      SV-COMP      |          Program               ||  Bitween (Pure Dynamic)    ||  DIG (Pure Dynamic)     || SymInfer (DIG+Symb. States) ||
|----|--------------|-------|-------|------|---------||---------|---------|--------||-------|---------|-------||----------|---------|--------||
|  # | nla-digbench | Trace | Trace | Max. | Type    || Bitween | Samples |  Time  ||  DIG  | Samples | Time  || SymInfer | Samples | Time   ||
|    |              | Locs. | Vars. | Deg. |         ||         |   (n)   |  (s)   ||       |   (n)   | (s)   ||          |   (n)   | (s)    ||
|----|--------------|-------|-------|------|---------||---------|---------|--------||-------|---------|-------||----------|---------|--------||
|  1 | Bresenham    |   2   |   5   |  2   | Integer ||    ✓    |    2112 |   2.19 ||   ✓   |   10712 |  3.05 ||    ✓     |    3836 |  16.71 ||
|  2 | CohenCu      |   2   |   5   |  3   | Integer ||    ✓    |    1556 |   3.69 ||   ✓   |    3760 |  3.08 ||    ✓     |    8881 |  10.75 ||
|  3 | CohenDiv     |   3   |   6   |  2   | Integer ||    ✓    |      96 |   3.73 ||   ✓   |     634 |  0.98 ||    ✓     |     255 |  19.04 ||
|  4 | Dijkstra     |   3   |   5   |  3   | Integer ||    ✓    |     208 |   6.95 ||   ✓   |     301 |  2.85 ||    ✓     |     513 |   9.57 ||
|  5 | Divbin       |   3   |   5   |  2   | Integer ||    ✓    |      90 |   2.02 ||   ✓   |     679 |  0.92 ||    ✓     |     212 |   6.41 ||
|  6 | Egcd         |   2   |   8   |  2   | Integer ||    ✓    |     299 |   6.59 ||   ✓   |    4580 |  7.81 ||    ✓     |    3564 |  48.91 ||
|  7 | Egcd2        |   3   |  10   |  3   | Integer ||    ✓    |     629 |   9.21 ||   ✓   |    4342 | 43.50 ||    ✓     |   11635 |  72.07 ||
|  8 | Egcd3        |   4   |  12   |  2   | Integer ||    ✓    |     562 |  16.84 ||   ✓-  |    2457 |  3.63 ||    ✓-    |    1693 |  15.05 ||
|  9 | Fermat1      |   4   |   5   |  2   | Double  ||    ✓    |     965 |   4.94 ||   ✓   |    9578 |  1.46 ||    ✗**   |      -- |   6.09 ||
| 10 | Fermat2      |   2   |   5   |  2   | Double  ||    ✓    |     336 |   5.59 ||   ✓   |    2805 |  1.29 ||    ✓     |     157 |  15.74 ||
| 11 | Freire1_int  |   1   |   3   |  2   | Integer ||    ✓    |     175 |   1.36 ||   ✓   |     417 |  0.64 ||    ✓     |     223 |   5.57 ||
| 12 | Freire1      |   1   |   3   |  2   | Double  ||    ✓    |     111 |   1.42 ||   ✗^  |      -- |  0.45 ||    ✗^    |      -- |   2.09 ||
| 13 | Freire2      |   1   |   3   |  3   | Double  ||    ✓    |      39 |   1.22 ||   ✗^  |      -- |  0.45 ||    ✗^    |      -- |   4.71 ||
| 14 | Geo1         |   2   |   4   |  2   | Integer ||    ✓    |      54 |   2.58 ||   ✓   |     140 |  0.76 ||    ✓     |     114 |   7.05 ||
| 15 | Geo2         |   2   |   4   |  2   | Integer ||    ✓    |      60 |   2.66 ||   ✓   |     140 |  0.75 ||    ✓     |     115 |   6.69 ||
| 16 | Geo3         |   2   |   5   |  3   | Integer ||    ✓    |     166 |   5.77 ||   ✗   |     159 |  0.49 ||    ✗     |     438 |  10.78 ||
| 17 | Hard         |   3   |   6   |  2   | Integer ||    ✓    |      44 |   3.35 ||   ✓   |     659 |  1.07 ||    ✓     |     264 |   7.01 ||
| 18 | Knuth*       |   2   |   8   |  3   | Mixed   ||    ✓    |     144 |  21.99 ||   ✗!  |      -- |  1.16 ||    ✗$    |      -- |   5.43 ||
| 19 | Lcm1         |   3   |   6   |  2   | Integer ||    ✓    |     238 |   3.41 ||   ✗   |    4253 |  1.16 ||    ✗$    |      -- |   5.26 ||
| 20 | Lcm2         |   2   |   6   |  2   | Integer ||    ✓    |     153 |   2.38 ||   ✓   |    4881 |  1.84 ||    ✗$    |    1719 |  43.40 ||
| 21 | Mannadiv     |   2   |   5   |  2   | Integer ||    ✓    |    1230 |   2.42 ||   ✓   |   10586 |  1.59 ||    ✓     |    2916 |   7.20 ||
| 22 | Prod4br      |   2   |   6   |  2   | Integer ||    ✓    |     127 |   2.26 ||   ✓   |     810 |  5.22 ||    ✓     |    1056 |  49.30 ||
| 23 | Prodbin      |   2   |   5   |  2   | Double  ||    ✓    |      95 |   2.21 ||   ✓   |     790 |  0.94 ||    ✓     |     256 |  23.52 ||
| 24 | Ps1          |   1   |   3   |  1   | Integer ||    ✓    |    1128 |   1.39 ||   ✓   |    3950 |  0.68 ||    ✗$    |      -- |   5.19 ||
| 25 | Ps2          |   2   |   3   |  2   | Integer ||    ✓    |      35 |   1.88 ||   ✓   |     228 |  0.62 ||    ✓     |     324 |   6.67 ||
| 26 | Ps3          |   2   |   3   |  3   | Integer ||    ✓    |     164 |   2.56 ||   ✓   |     228 |  0.77 ||    ✓     |     324 |   6.67 ||
| 27 | Ps4          |   2   |   3   |  4   | Integer ||    ✓    |     223 |   2.63 ||   ✓   |     228 |  1.07 ||    ✓     |     468 |   7.44 ||
| 28 | Ps5          |   2   |   3   |  5   | Integer ||    ✓&   |     154 |  11.36 ||   ✓   |     154 |  1.25 ||    ✓     |     251 |   7.19 ||
| 29 | Ps6          |   2   |   3   |  6   | Integer ||    ✓&   |     154 |  22.65 ||   ✓   |     229 |  2.57 ||    ✓     |     350 |   8.05 ||
| 30 | Rd_Wr***     |   2   |   6   |  2   | Integer ||    ✓    |     559 |   4.40 ||   ?   |    ToDo |  ToDo ||    ✗--   |      -- |   5.19 ||
| 31 | Sqrt         |   2   |   4   |  2   | Integer ||    ✓    |     146 |   2.81 ||   ✓   |     281 |  0.70 ||    ✓     |     225 |   6.08 ||
| 32 | Wensley2     |   2   |   7   |  2   | Float   ||    ✓    |     208 |   7.54 ||   ✗^  |      -- |  0.45 ||    ✗^    |      -- |   2.09 ||
|----|--------------|-------|-------|------|---------||---------|---------|--------||-------|---------|-------||----------|---------|--------||
                                                     ||   30    |   11493 | 169.19 ||  27   |   67981 | 92.75 ||   22     |   39789 | 445.64 || 
                                                     ||---------|---------|--------||-------|---------|-------||----------|---------|--------||

+ & Due to numerical instability, first we couldn't find the invariants for Ps5 and Ps6 benchmarks. Then, we have used more advanced scaling technique to find the invariants for these benchmarks.
+ ^ DIG couldn't find the invariants for these benchmarks since the program has floating-point operations.
+ $ SymInfer's underlying Symbolic Execution engine couldn't do external function calls for these benchmarks (gcd/lcm/sqrt functions). 
+ ! DIG couldn't call the external sqrt function 
+ - DIG and SymInfer couldn't find all target invariants for these benchmarks.
+ * We obtained new invariants for the post conditions of the Knuth benchmark, which are not reported in the literature.
+ ** SymInfer's underlying Symbolic Execution engine couldn't reach the end of the program for these benchmarks.
+ *** This benchmark includes Non-deterministic choice.
+ -- Symbolic Execution didn't work due to the non-deterministic choice in the benchmark.

This can be a figure as follows

![Time Comparison Example Figures](images/time_comparison_example.png)

* This is to show the effect of sample size on the term size of the invariants generated by Bitween vs. DIG
* For each benchmark, the largest number of samples that DIG/SymInfer cannot generate invariants is used as the sample size for Bitween


## TABLE -- Random Self-Reducible Property Generation (Mathematical Properties)

Dims.: Dimensions
Deg. : The Degree that the property is discovered
V    : Verified
?    : Ground Truth is unknown (if there is a known functional equation in the literature.)
Vars : Univariate, Bivariate, Trivariate, etc.

|----|--------------|-----|-----|---------------|------||------------|--------||---------|------|--------||-----|---|
|  # |    Problem   | Vars| Deg.| Template      | Dims.|| Eager MILP |  Time  || Bitween | MILP |  Time  || RSR | V |
|    |  (rsr-bench) |     |     | Used          |      || (baseline) |   (s)  || Result  | used |   (s)  ||  ?  |   |
|----|--------------|-----|-----|---------------|------||------------|--------||---------|------|--------||-----|---|
|  1 |  Identity    |  1  |  1  | Addition Thm. |    5 ||            |        ||    ✓    |  -   |   0.70 ||  ✓  | ✓ |
|  2 |  Exp         |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.49 ||  ✓  | ✓ |
|  3 |  Sigmoid     |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.39 ||  ✓  | ✓ |
|  4 |  Exp1        |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.60 ||  ✓  | ✓ |
|  5 |  ExpDivByX   |  1  |  5  | Addition Thm. |  126 ||            |        ||    ?    |  +   |  89.63 ||  ?  | - |
|  6 |  Floudas     |  2  |  1  | Addition Thm. |    6 ||            |        ||    ✓    |  -   |   0.72 ||  ✓  | ✓ |
|  7 |  Mean        |  3  |  1  | Addition Thm. |    8 ||            |        ||    ✓    |  -   |   0.73 ||  ✓  | ✓ |
|  8 |  Tan         |  1  |  3  | Addition Thm. |   35 ||            |        ||    ✓    |  -   |   3.07 ||  ✓  | ✓ |
|  9 |  Cot         |  1  |  3  | Addition Thm. |   35 ||            |        ||    ✓    |  -   |   2.56 ||  ✓  | ✓ |
| 10 |  Tanh        |  1  |  3  | Addition Thm. |   35 ||            |        ||    ✓    |  -   |   3.89 ||  ✓  | ✓ |
| 11 |  Sub_x2_y2   |  2  |  3  | Addition Thm. |  165 ||            |        ||    ✓    |  -   |  95.09 ||  ✓  | ✓ |
| 12 |  Sqrt_Add    |  1  |  5  | Addition Thm. |  126 ||            |        ||    ?    |  +   |  97.49 ||  ?  | - |
| 13 |  Inverse     |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.28 ||  ✓  | ✓ |
| 14 |  Inv_add     |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   0.94 ||  ✓  | ✓ |
| 15 |  Inv_Cot_Add*|  1  |  3  | Addition Thm. |   20 ||            |        ||    ✓*   |  -   |   1.18 ||  ✓  | ✓ |
| 16 |  Inv_Tan_Add*|  1  |  3  | Addition Thm. |   20 ||            |        ||    ✓*   |  -   |   1.02 ||  ✓  | ✓ |
| 17 |  Inv_Sub^    |  1  |  3  | Addition Thm. |   15 ||            |        ||    ✓^   |  -   |   1.09 ||  ✓  | ✓ |
| 18 |  Inv_Sub2^   |  1  |  3  | Addition Thm. |   15 ||            |        ||    ✓^   |  -   |   1.22 ||  ✓  | ✓ |
| 19 |  Cos         |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.00 ||  ✓  | ✓ |
| 20 |  Cosh        |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.05 ||  ✓2 | ✓ |
| 21 |  Squared     |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.08 ||  ✓1 | ✓ |
| 22 |  Sin         |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.04 ||  ✓1 | ✓ |
| 23 |  Sinh        |  1  |  2  | Addition Thm. |   15 ||            |        ||    ✓    |  -   |   1.17 ||  ✓1 | ✓ |
|----|--------------|-----|-----|---------------|------||------------|--------||---------|------|--------||-----|---|
                                                 
* Templates: F[f(x+y), f(x), f(y), 1] = 0 for others: F[f(x-y), f(x+y), f(x), f(y), 1] = 0. 
  The reduction is done by Groebner basis. However, we cannot reduce where we use the second template.
^ When degree is 3, we are not able to reduce/refine the properties to a simpler form. However, it works at degree 2.
? we couldn't infer any property. We couldn't detect any functional equation for this property in the literature, 


## TABLE -- Float Benchmarks - (post condition generation with different templates)

V  : Verified
LoC: Lines of Code

|----|------------------|-----|----------------|-----||---------|------|------||---|
|  # | SV-COMP          | Ref.| Template       | LoC || Bitween | MILP | Time || V |
|    | (float-bench)    |     |                |     || Result  | used | (s)  ||   |
|----|------------------|-----|----------------|-----||---------|------|------||---|
|  1 | addsub           | [?] | Addition Thm.  |  18 ||    ✓    |  -   | ?    || ✓ |
|  2 | arctan_Pade      | [?] | Odd Function   |  36 ||    ✓    |  -   | ?    || ✓ |
|  3 | cos_polynomial   | [?] | Addition Thm.  |  40 ||    ✓    |  -   | ?    || ✓ |
|  4 | exp_loop         | [?] | Exponential    |  59 ||    ✓    |  -   | ?    || ✓ |
|  5 | filter_iir       | [?] | Addition Thm.  |  41 ||    ✓    |  -   | ?    || ✓ |
|  6 | inv_Newton-1     | [?] | Addition Thm.  |  36 ||    ✓    |  -   | ?    || ✓ |
|  7 | inv_Newton-2     | [?] | Addition Thm.  |  45 ||    ✓    |  -   | ?    || ✓ |
|  8 | inv_sqrt_Quake   | [?] | Multiplicative |  22 ||    ✓    |  -   | ?    || ✓ |
|  9 | inv_square_int   | [?] | Multiplicative |  23 ||    ✓    |  -   | ?    || ✓ |
| 10 | inv_square-1     | [?] | Multiplicative |  23 ||    ✓    |  -   | ?    || ✓ |
| 11 | Muller_Kahan     | [?] | Addition Thm.  |  30 ||    ✓    |  -   | ?    || ✓ |
| 12 | sin_interpolated | [?] | Addition Thm.  | 140 ||    ✓    |  -   | ?    || ✓ |
| 13 | sqrt_householder | [?] | Inverse        |  34 ||    ✓    |  -   | ?    || ✓ |
| 14 | sqrt_poly        | [?] | Inverse        |  24 ||    ✓    |  -   | ?    || ✓ |
| 15 | sqrt_poly2       | [?] | Inverse        |  48 ||    ✓    |  -   | ?    || ✓ |
| 16 | water_pid        | [?] | Addition Thm.  |  45 ||    ✓    |  -   | ?    || ✓ |
| 17 | zonotope         | [?] | Addition Thm.  |  26 ||    ✓    |  -   | ?    || ✓ |
| 18 | zonotope_2       | [?] | Addition Thm.  |  31 ||    ✓    |  -   | ?    || ✓ |
| 19 | zonotope_3       | [?] | Addition Thm.  |  38 ||    ✓    |  -   | ?    || ✓ |
|----|------------------|-----|----------------|-----||---------|------|------||---|

TODO: add references from C files. Explain the nature of examples. Explain the importance of the templates, and the difficulty of the benchmarks.
share some interesting results.

## TABLE -- FPBench -- Real-Valued Nonlinear Loop Invariants 

Dims. = Dimensions
LoC = Lines of Code
A = Accuracy (Approximate or Exact)
For each benchmark, the precondition is defined by FPBench, and the postcondition or loop invariant is generated by Bitween.
For instance, in the Odomentry Robotics Arm benchmark, the precondition is given as conjuction of intervals, 
such that  `(0.05 < sl* < 2 * PI) and (0.05 < sr* < 2 * PI)`

|----|-------------------------|-------------|-------|-----|------|-------|-----|------||----------|---|------||---------|---|------|
|  # | FPBench                 | Problem     | Ref.  | LoC | Inv. | Trace | Max.| Dims.|| Eq. Sol. | A | Time || Bitween | A | Time |
|    | (Salsa & Rosa Bench)    | Domain      |       |     | Type | Vars. | Deg.|      ||(baseline)|   | (s)  || Result  |   | (s)  |
|----|-------------------------|-------------|-------|-----|------|-------|-----|------||----------|---|------||---------|---|------|
|  1 | Odometry Robotics Arm   | Controls    |[1]    | 57  | Loop |       |  2  |      ||          |   |      ||    ✓    |   |      |
|  2 | PID Controller          | Controls    |[1,2]  | 24  | Loop |       |  3  |      ||          |   |      ||    ✓    |   |      |
|  3 | Rocket Trajectory       | Controls    |[3]    | 82  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  4 | Lead-lag System         | Controls    |[4,1]  | 38  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  5 | Runge-Kutta Diff. Eq.   | Mathematics |[1]    | 27  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  6 | Trapeze                 | Mathematics |[1]    | 26  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  7 | Jacobi's Method         | Mathematics |[5]    | 28  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  8 | Newton-Raphson's Method | Mathematics |[5]    | 18  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
|  9 | Eigenvalue Computation  | Mathematics |[6]    | 28  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
| 10 | Iterative Gram-Schmidt  | Mathematics |[7,6,8]| 36  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
| 11 | N Body Simulation       | Science     |[10]   | 46  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
| 12 | Pandelum                | Science     |[10]   | 23  | Loop |       |     |      ||          |   |      ||    ✓    |   |      |
| 13 | Jet Engine              | Science     |[9,10] | 14  | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 14 | Sine Newton             | Mathematics |[10]   | 16  | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 15 | Doppler                 | Science     |[10]   | 4   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 16 | Smart Root              | Mathematics |[10]   | 20  | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 17 | Rigid Body 1            | Science     |[9,10] | 6   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 18 | Rigid Body 2            | Science     |[9,10] | 6   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 19 | Turbine 1               | Science     |[9,10] | 5   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 20 | Turbine 2               | Science     |[9,10] | 3   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 21 | Turbine 3               | Science     |[9,10] | 5   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 22 | Verhulst                | Science     |[9,10] | 4   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 23 | Predator Prey           | Science     |[9,10] | 5   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 24 | Carbon Gas              | Science     |[9,10] | 5   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 25 | Sine                    | Mathematics |[10]   | 4   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 26 | Sqrt Approx.            | Mathematics |[10]   | 4   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 27 | Sine Order 3            | Mathematics |[10]   | 3   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 28 | Smart Root              | Science     |[10]   | 20  | Post |       |     |      ||          |   |      ||    ✓    |   |      |
| 29 | Bspline                 | Science     |[10]   | 3   | Post |       |     |      ||          |   |      ||    ✓    |   |      |
|----|-------------------------|-------------|-------|-----|------|-------|-----|------||----------|---|------||---------|---|------|
                                                                                  
[1]  `Intra-procedural Optimization of the Numerical Accuracy of Programs` (damouche-martel-chapoutot-fmics15)
[2]  `Transformation of a PID Controller for Numerical Accuracy` (damouche-martel-chapoutot-nsv14)
[3]  `Optimizing the Accuracy of a Rocket Trajectory Simulation by Program Transformation` (damouche-martel-chapoutot-cf15)
[4]  `From Control Systems to Control Software` (feron-ieee10)
[5]  `An Introduction to Numerical Analysis` (atkinson-1989)
[6]  `Matrix Computations (3rd Ed.)` (golub-vanloan-1996)
[7]  `Round off error analysis for Gram-Schmidt method and solution of linear least squares problems` (abdelmalek-bit71)
[8]  `A survey of software for sparse eigenvalue problems` (hernandez-roman-tomas-vidal-tr07)
[9]  `Sound Compilation of Reals`. (darulova-kuncak-2014) 
[10] `Rigorous Estimation of Floating-Point Round-off Errors with Symbolic Taylor Expansions` (solovyev-et-al-2015)


# Sensitivity Studies: Analyzing Bitween Framework Workflows and Configurations.
================================================================================

## TABLE -- Evaluation of Bitween Property Inferrence Pipeline (ablation study)
An ablation study in the context of a research paper, particularly in fields like machine learning, computer science, and bioengineering, 
is a systematic method of analyzing the contribution of individual components of a system or process to understand their impact on the overall 
performance or functionality. 

1. Baseline System: Establish a baseline by evaluating the performance of the complete system, which includes all components or features.
2. Component Removal: One by one, remove or "ablate" components from the system. This could involve disabling specific features, algorithms, or parts of a model.
3. Impact Assessment: After each removal, the system is re-evaluated to determine the impact of the missing component on the overall performance. 
This helps identify which components are essential and which are less impactful.
4. Result Analysis: The results from each iteration (with different components removed) are compared to the performance of the baseline system. 
This comparison helps to illustrate the relative importance of each component.

|----|-------------|-------------||------------||-------------|-----------|-----------||----------|-----------|-----------|
|  # | Benchmark   | Total # of  || Eager MILP || (1) Multiple| (2) LR    | (3) MILP  || Property | Groebner  | Z3        |
|    | (Integer)   | Target Invs.|| (baseline1)|| Regression  | Refinement| Refinement|| Testing  | Reduction | Reduction |
|----|-------------|-------------||------------||-------------|-----------|-----------||----------|-----------|-----------|
|  1 | Bresenham   |             ||            ||             |           |           ||          |           |           |
|  2 | CohenCu     |             ||            ||             |           |           ||          |           |           |
|  3 | CohenDiv    |             ||            ||             |           |           ||          |           |           |
|  4 | Dijkstra    |             ||            ||             |           |           ||          |           |           |
|  5 | Divbin      |             ||            ||             |           |           ||          |           |           |
|  6 | Egcd        |             ||            ||             |           |           ||          |           |           |
|  7 | Egcd2       |             ||            ||             |           |           ||          |           |           |
|  8 | Egcd3       |             ||            ||             |           |           ||          |           |           |
|  9 | Fermat1     |             ||            ||             |           |           ||          |           |           |
| 10 | Fermat2     |             ||            ||             |           |           ||          |           |           |
| 11 | Freire1_int |             ||            ||             |           |           ||          |           |           |
| 12 | Freire1     |             ||            ||             |           |           ||          |           |           |
| 13 | Freire2     |             ||            ||             |           |           ||          |           |           |
| 14 | Geo1        |             ||            ||             |           |           ||          |           |           |
| 15 | Geo2        |             ||            ||             |           |           ||          |           |           |
| 16 | Geo3        |             ||            ||             |           |           ||          |           |           |
| 17 | Hard        |             ||            ||             |           |           ||          |           |           |
| 18 | Knuth       |             ||            ||             |           |           ||          |           |           |
| 19 | Lcm1        |             ||            ||             |           |           ||          |           |           |
| 20 | Lcm2        |             ||            ||             |           |           ||          |           |           |
| 21 | Mannadiv    |             ||            ||             |           |           ||          |           |           |
| 22 | Prod4br     |             ||            ||             |           |           ||          |           |           |
| 23 | Prodbin     |             ||            ||             |           |           ||          |           |           |
| 24 | Ps1         |             ||            ||             |           |           ||          |           |           |
| 25 | Ps2         |             ||            ||             |           |           ||          |           |           |
| 26 | Ps3         |             ||            ||             |           |           ||          |           |           |
| 27 | Ps4         |             ||            ||             |           |           ||          |           |           |
| 28 | Ps5         |             ||            ||             |           |           ||          |           |           |
| 29 | Ps6         |             ||            ||             |           |           ||          |           |           |
| 30 | Sqrt        |             ||            ||             |           |           ||          |           |           |
|----|-------------|-------------||------------||-------------|-----------|-----------||----------|-----------|-----------|

* Groebner Basis: We use Groebner basis to reduce the properties to a simpler form (http://www.scholarpedia.org/article/Groebner_basis)

TODO: the most frequent terms used in regression models is also a model, add this to the table
TODO: forward selection + LR is missing.


## Figure -- Compare Bitween with MILP solver backends (gurobi vs pulp)

Gurobi: commercial solver while Pulp and GLPK are open-source solvers.

|----|------------|---------|------------||--------|--------------||--------|--------------||--------|--------------|
|  # | Benchmark  | Samples | Ave. Dims. || Gurobi | Gurobi       || Pulp   | Pulp         || GLPK   | GLPK         |
|    | (Integer)  | Used    | After      || (time) | (# of props) || (time) | (# of props) || (time) | (# of props) |
|    |            |         | Refinement ||        |              ||        |              ||        |              |
|----|------------|---------|------------||--------|--------------||--------|--------------||--------|--------------|
|  1 | Bresenham  |   30    |            ||        |              ||        |              ||        |              |
|  2 | CohenCu    |         |            ||        |              ||        |              ||        |              |
|  3 | CohenDiv   |         |            ||        |              ||        |              ||        |              |
|  4 | Dijkstra   |         |            ||        |              ||        |              ||        |              |
|  5 | Divbin     |         |            ||        |              ||        |              ||        |              |
|  6 | Egcd       |         |            ||        |              ||        |              ||        |              |
|  7 | Egcd2      |         |            ||        |              ||        |              ||        |              |
|  8 | Egcd3      |         |            ||        |              ||        |              ||        |              |
|  9 | Fermat1    |         |            ||        |              ||        |              ||        |              |
| 10 | Fermat2    |         |            ||        |              ||        |              ||        |              |
| 11 | Freire1_int|         |            ||        |              ||        |              ||        |              |
| 12 | Freire1    |         |            ||        |              ||        |              ||        |              |
| 13 | Freire2    |         |            ||        |              ||        |              ||        |              |
| 14 | Geo1       |         |            ||        |              ||        |              ||        |              |
| 15 | Geo2       |         |            ||        |              ||        |              ||        |              |
| 16 | Geo3       |         |            ||        |              ||        |              ||        |              |
| 17 | Hard       |         |            ||        |              ||        |              ||        |              |
| 18 | Knuth      |         |            ||        |              ||        |              ||        |              |
| 19 | Lcm1       |         |            ||        |              ||        |              ||        |              |
| 20 | Lcm2       |         |            ||        |              ||        |              ||        |              |
| 21 | Mannadiv   |         |            ||        |              ||        |              ||        |              |
| 22 | Prod4br    |         |            ||        |              ||        |              ||        |              |
| 23 | Prodbin    |         |            ||        |              ||        |              ||        |              |
| 24 | Ps1        |         |            ||        |              ||        |              ||        |              |
| 25 | Ps2        |         |            ||        |              ||        |              ||        |              |
| 26 | Ps3        |         |            ||        |              ||        |              ||        |              |
| 27 | Ps4        |         |            ||        |              ||        |              ||        |              |
| 28 | Ps5        |         |            ||        |              ||        |              ||        |              |
| 29 | Ps6        |         |            ||        |              ||        |              ||        |              |
| 30 | Sqrt       |         |            ||        |              ||        |              ||        |              |
|----|------------|---------|------------||--------|--------------||--------|--------------||--------|--------------|


## Table 5-- Confusion Matrix of Bitween for NLA DIG Benchmarks (loop invariant generation)
...

## Table 5-- Confusion Matrix of Bitween for NLA Float Benchmarks (post condition generation)

## Table 6-- Stability of Bitween
...

## Figure -- Model parameters and how many of them are used in the final model that pinpoints an invariant for each benchmark

|-------------------||-------------------||----------------------------------------------------------------------||----------------------------------------------------------------------|
|      SV-COMP      || Linear Regression ||                                Lasso                                 ||                                Ridge                                 |
|----|--------------||-------------------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------|
|  # | nla-digbench ||     Intercept     ||           Intercept              ||         No Intercept             ||           Intercept              ||         No Intercept             |
|    |              ||---------|---------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------|
|    |              ||  Yes    |   No    || 1e-3 | 1e-2 | 1e-1 | 1e+1 | 1e+2 || 1e-3 | 1e-2 | 1e-1 | 1e+2 | 1e+3 || 1e-3 | 1e-2 | 1e-1 | 1e+2 | 1e+3 || 1e-3 | 1e-2 | 1e-1 | 1e+2 | 1e+3 |
|----|--------------||---------|---------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------|
|  1 | Bresenham    ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  2 | CohenCu      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  3 | CohenDiv     ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  4 | Dijkstra     ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  5 | Divbin       ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  6 | Egcd         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  7 | Egcd2        ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  8 | Egcd3        ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|  9 | Fermat1      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 10 | Fermat2      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 11 | Freire1_int  ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 12 | Freire1      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 13 | Freire2      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 14 | Geo1         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 15 | Geo2         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 16 | Geo3         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 17 | Hard         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 18 | Knuth        ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 19 | Lcm1         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 20 | Lcm2         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 21 | Mannadiv     ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 22 | Prod4br      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 23 | Prodbin      ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 24 | Ps1          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 25 | Ps2          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 26 | Ps3          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 27 | Ps4          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 28 | Ps5          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 29 | Ps6          ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
| 30 | Sqrt         ||         |         ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      ||      |      |      |      |      |
|----|--------------||---------|---------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------||------|------|------|------|------|