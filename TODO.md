# Paper Writing
* Integrate the dig bench table (run analysis 5 times) and discuss details, give some examples.
* Integrate the RSR figure and discuss, give some interesting examples.
* Integrate the big figure comparing ML approaches and discuss.
* Integrate a figure that compares with symbolic regression methods (gplearn, pays, kan).

* Create two motivation example (rsr prop over sin, periyodik, etc.) and the motivating example having mixed integer and reals; put the vtrace tables. 

* introduce this vtrace as a function basis like F[a, b, v, n, 1] = 0

## Learning Algorithms
Discuss a section for MILP formulation.
Discuss a section for Regression-based algorithms.

## Compare it with Meta's regression tool
Discuss Symbolic Regression.
**Test GPLEARN**
**Test PySR**
**Test KAN**


## Integrate PAC.


# TODO: improvements
1. Add Advanced scaling (http://www.gurobi.cn/download/GuNum.pdf).
2. NNL?
3. Linear regression, with intercept wo intercept, searching an intercept.


# LATEX NOTES FOR THE PAPER

## Discuss the complexity of multiple regression analysis. 

All learning methods that we used is polynomial in the size of the data (number of samples and number of features).

```tex
\subsection{Ordinary Least Squares Complexity}
The least squares solution is computed using the singular value decomposition of \(X\). If \(X\) is a matrix of shape \((n_{\text{samples}}, n_{\text{features}})\), this method has a cost of \(O(n_{\text{samples}} n_{\text{features}}^2)\), assuming that \(n_{\text{samples}} \geq n_{\text{features}}\).
Source: https://scikit-learn.org/stable/modules/linear_model.html

\subsection{Ridge Complexity}
This method has the same order of complexity as Ordinary Least Squares.
Source: https://scikit-learn.org/stable/modules/linear_model.html

\subsection{Lasso Complexity}
Let the number of candidate variables (features, columns) be $K$ and the sample size (number of observations, rows) be $n$. Consider LASSO implemented using LARS algorithm ([Efron et al., 2004][1]). The computational complexity of LASSO is $\mathcal{O}(K^3 + K^2 n)$ (*ibid.*)

* For $K<n$, $K^3 < K^2 n$ and the computational complexity of LASSO is $\mathcal{O}(K^2 n)$, which is the same as that of a regression with $K$ variables ([Efron et al., 2004][1], p. 443-444; also cited in [Schmidt, 2005][2], section 2.4; for computational complexity of a regression, see [this post][2]).
* For $K \geqslant n$, $K^3 \geqslant K^2 n$ and the computational complexity of LASSO is $\mathcal{O}(K^3)$ ([Efron et al., 2004][1]).

References:

* Efron, Bradley, et al. ["Least angle regression."][1] *The Annals of Statistics* 32.2 (2004): 407-499.
* Schmidt, Mark. ["Least squares optimization with l1-norm regularization."][2] *CS542B Project Report* (2005).

[1]: http://statweb.stanford.edu/~imj/WEBLIST/2004/LarsAnnStat04.pdf
[2]: http://www.di.ens.fr/~mschmidt/Software/lasso.pdf

Source: https://stats.stackexchange.com/a/190717
```

## PAC-style learning for the number of samples and the number of terms in the hypothesis.
1. What does PAC learnable mean?
2. What is a PAC learnable algorithm.
3. Sample Complexity: Theorem: Every finite hypothesis class is PAC learnable with sample complexity.
3. What is realizability assumption?
4. Our approach and how we define hypothesis class?
5. How we calculate finite hypotheses space in polynomial time complexity?
```tex
\subsection{Sample Size Calculation for Polynomial Hypothesis Space}

\begin{theorem}{}
Every finite hypothesis class is PAC learnable with sample complexity
\[
m_\mathcal{H}(\epsilon, \delta) \leq\left\lceil \frac{\log\left({|\mathcal{H}|}/{\delta}\right)}{\epsilon} \right\rceil.
\]
For any $\epsilon, \delta, m_\mathcal{H}(\epsilon, \delta)$ is the minimal integer that satisfies the requirements of PAC learning with accuracy $\epsilon$ and confidence $\delta$.
\end{theorem}

In our setting, the hypothesis space is finite, and this section outlines the calculation of the minimum sample size required for PAC (Probably Approximately Correct) learning, given specific parameters of a polynomial hypothesis space. The calculation takes into account the complexity of the hypothesis space and desired levels of accuracy and confidence. Our primary goal is to learn a function, \( h : \mathbb{R}^n \rightarrow \mathbb{R} \), using a hypothesis class composed of polynomials.

\paragraph{Learning Goals and Hypothesis Class}
Our objective is to approximate an unknown target function as accurately as possible within a predefined confidence level. We utilize the hypothesis class of polynomials, which offers a structured approach to model relationships in the data. Given the uncertainty about the optimal degree \( d \) of the polynomial for modeling our data, we face a trade-off:
\begin{itemize}
    \item A lower degree may result in a polynomial that underfits the data, leading to a large approximation error.
    \item Conversely, a higher degree might fit the data too closely, resulting in overfitting and hence a large estimation error.
\end{itemize}

\paragraph{Realizability Assumption}
We operate under the realizability assumption, which posits that the true function being approximated is contained within our hypothesis class. This implies there exists at least one hypothesis in the class that could perfectly model the true function. A non-solution scenario corresponds to a polynomial where all coefficients and the bias term are zero, indicating no relationship captured by the chosen model.

\paragraph{Parameters and Definitions}
\begin{itemize}
    \item Number of variables (\( n \)): Total number of variables in the polynomial. 
    \item Maximum degree (\( d \)): Highest degree of any term in the polynomial. 
    \item Coefficient bound (\( b \)): Absolute limit on the polynomial coefficients, ranging from \(-b\) to \( b \). Default, \( b = 20 \).
    \item Maximum selected terms (\( k \)): Maximum number of monomial terms selected in any given hypothesis within the model. Default, \( k = 20 \).
    \item Coefficient precision (\( p \)): Precision (number of significant digits) to which coefficients are measured. Default, \( p = 2 \).
    \item Precision in learning (\( \epsilon \)): Allowable error in the learned model relative to the true model. Default, \( \epsilon = 0.1 \).
    \item Confidence (\( \delta \)): Probability that the learned model's error exceeds \( \epsilon \). Default, \( \delta = 0.2 \).
\end{itemize}

Example: For a trace location having 5 terms (e.g. `vtrace(x, y, z, a, b);`), up to degree 3, the number of monomials is 56, number of subsets is 785613562163430 and the hypothesis space size is 3221015604870063000.  

\subsubsection{Calculation}
\paragraph{Number of Monomials}
The number of different monomials in a polynomial with \( n \) variables up to degree \( d \) can be determined by the combinatorial formula:
\[ \text{Monomials} = \binom{n + d}{d} \]

\paragraph{Number of Subsets of Terms}
Given the number of monomials, the number of subsets of these terms that can be selected, where the size of each subset is up to \( k \), is calculated as:
\[ \text{Subsets} = \binom{\text{Monomials}}{k} \]

\paragraph{Hypothesis Space Size}
The hypothesis space size \( H \) considers the number of potential hypotheses generated by selecting subsets of terms and varying their coefficients within the given bounds and precision:
\[ H = (2b + 1) \times 10^p \times \text{Subsets} \]

Here, \( (2b + 1) \) accounts for all integer values a coefficient can take, from \(-b\) to \( b \), and \( 10^p \) represents the number of discrete steps within this range based on the precision.

\paragraph{Sample Size Bound}
To ensure that with probability at least \( 1 - \delta \), the empirical error is within \( \epsilon \) of the true error, the sample size \( m \) can be calculated as:
\[ m = \left\lceil \frac{\ln\left(\frac{H}{\delta}\right)}{\epsilon} \right\rceil \]

This formula calculates the necessary number of samples to achieve the desired confidence and accuracy in learning.
```

## Reduction Algorithm: 

<!-- For hypothesis classes that are countable, we can apply the Minimum Description Length scheme, where hypotheses with shorter descriptions are preferred, following the principle of Occam’s razor -->

```tex
\subsection{Algorithm to Reduce the Set of Equalities}
This section describes the methodology implemented to normalize a set of inferred polynomial equations, merge them into equivalence classes, and select the most aesthetically pleasing or simplest polynomial from each class based on a specific scoring system. The final reduction steps refines the selected polynomials further using Groebner basis reduction and other techniques to ensure the most concise and interpretable forms are retained. 

Example:
\[
\begin{aligned}
    \text{eq3} & = x - \frac{y^5}{5} - \frac{y^4}{2} - \frac{33y^3}{100} + \frac{3y}{100} = 0 \quad (\text{score: } 10.4) \\
    \text{eq4} & = -5x + y^5 + \frac{5y^4}{2} + \frac{167y^3}{100} - \frac{17y}{100} = 0 \quad (\text{score: } 12.5) \\
    \text{eq4} & = -30x + 6y^5 + 15y^4 + 10y^3 - y = 0 \quad (\text{score: } 25)
\end{aligned}
\]

\paragraph{Normalization and Merging into Equivalence Classes}
The algorithm begins by normalizing each polynomial equation. Coefficients are Rational numbers converted from floating point numbers inferred during the learning process. Each equation is ordered lexicographically, and if the leading term is negative, the entire expression is multiplied by \(-1\) to ensure a positive leading term. Using a union-find data structure, equations are then grouped into equivalence classes by merging equations that are considered similar.

The algorithm begins by normalizing each equation in the input set of learned equations, ensuring that they are in a consistent form that facilitates comparison. This is achieved through lexicographical ordering of terms within each polynomial expression, and if the leading term is negative, the entire expression is multiplied by \(-1\) to ensure a positive leading term.

Using a union-find data structure, the algorithm then groups similar equations. Two equations are considered similar if they share identical terms, enabling the formation of equivalence classes. Each class theoretically represents a unique polynomial identity but can contain multiple equivalent expressions due to differences in coefficients that are stemmed from the numerical errors of floating point operations in the learning process.

\paragraph{Scoring System and Selection}
Within each equivalence class, a "best looking" polynomial is selected based on a scoring system that adheres to Occam's razor. This system prioritizes integer coefficients and simple fractions such as multiples of \(0.5\), \(0.25\), and effectively integers for multiples of \(0.33\). A penalty is applied based on decimal complexity, discouraging coefficients with complex decimal representations.
The polynomial with the highest score within each class is chosen as the representative for that class.

\paragraph{Final Reduction}
After selecting the best representatives, the polynomials undergo several final reduction steps:
\begin{enumerate}
  \item \textbf{Denominator Elimination:} Integer denominators are eliminated from the equations to simplify terms.
  \item \textbf{Removal of Ugly Classes:} If, after denominator elimination, any polynomial in a class contains coefficients that exceed a configurable threshold or are deemed too large or complex (as per a predefined 'ugliness' factor), the entire class is removed. This step ensures that only polynomials with manageable and aesthetically pleasing coefficients are retained.
  \item \textbf{Groebner Basis Reduction:} For the remaining polynomial classes, the set of equations is further reduced using a Groebner basis. This step is designed to minimize the set of equations while maintaining their mathematical implications. However, this process can sometimes result in a larger set of equations or get computationally stuck; thus, it is applied cautiously. We use the SymPy library for Groebner basis computation, which uses an improved implementation of the Buchberger algorithm~\cite{?} is used to compute the reduced set of equations.
\end{enumerate}

The described method systematically simplifies and selects polynomial equations by reducing complexity and ensuring that the simplest, most interpretable forms are retained. This approach balances mathematical rigor with practical considerations for polynomial representation and computational efficiency.
```

## Interpolation and Regression Comparison for Non-linear Invariants

```tex

This shows nicely that higher degree polynomials can fit the data better. But
at the same time, too high powers can show unwanted oscillatory behaviour
and are particularly dangerous for extrapolation beyond the range of fitted
data. 

This is an advantage of B-splines. They usually fit the data as well as
polynomials and show very nice and smooth behaviour. They have also good
options to control the extrapolation, which defaults to continue with a
constant. Note that most often, you would rather increase the number of knots.


Polynomial interpolation are not accurate enough, they are interprarable but high degree polynomials are particularly dangerous for extrapolation beyond the range of fitted data.
Spline Interpolation not interpretable, but they are accurate with the increasing number of knots. 
MLP Regressor is not interpretable, but it is accurate to some extent, requires a lot of data.
KAN is interpretable and accurate in fitting data, but symbolic intepratation requires manuel analysis, and not scalable.

Explainability vs. predictive power trade-off.
```

## Paper Writing

* Integrate the dig bench table (run analysis 5 times) and discuss details, give some examples.
* Integrate the RSR figure and discuss, give some interesting examples.
* Integrate the big figure and discuss.
* Create two motivation example (rsr prop over sin, periyodik, etc.) and the motivating example having mixed integer and reals; put the vtrace tables. 

+ Learning Algorithms
 * Formal Definition of the problem.
 * We don't know which one is the dependent variable (target) and others are explanatory variables.
 * Discuss a section for MILP formulation.
 * Discuss a section for Regression-based algorithms.
 * Discuss their complexity and hyper-parameters.

+ Discuss Symbolic Regression.
+ Compare with Regressiong Tools

## TODO
* Test GPLEARN (done)

* Test PySR (done)
> you are running with 10 features or more. Genetic algorithms like used in PySR scale poorly with large numbers of features. 
> You should run PySR for more `niterations` to ensure it can find the correct variables, or, alternatively, 
> do a dimensionality reduction beforehand. For example, `X = PCA(n_components=6).fit_transform(X)`, using scikit-learn's 
> `PCA` class, will reduce the number of features to 6 in an interpretable way, as each resultant feature will be a linear 
> combination of the original features. 

## Regression Problems:
- Exactly repeated terms in the invariants. (repeated features in the regression model)
x2 gives no new information if x1 is already in the model.
f(x1, x2) = 4x1
f(x1, x2) = w1*x1 + w2*x2 where w1 + w2 = 4 
- Linearly dependent terms in the invariants. (redundant features in the regression model)
f(x1, x2) = w1*x1 + w2*x2 where w1 = 2w2, then all functions with w1 + 2w2 = k are the same.

## Questions that I received from the audience:
From Jakub’s students, I’ve received these questions:

1. What is the difference between our approach and the existing symbolic regression methods?
   * We compared the results with the symbolic regression backends we integrated into our method.
   * GP-based symbolic regression methods are not scalable, and they sometimes miss some invariants, particularly when the number of features is high and the data/invariant is integer-valued.
   * Symbolic Regression methods consider composition of terms and therefore more general; Bitween only considers polynomial interaction of terms since the benchmarks suits are in this format. However, Bitween is able to cope with several depths of composition of functions, but this is not evaluated. We configured symbolic regression only to look for mul, sub, and sum
   * We integrated PySR and GPlearn symbolic regression methods in Bitween. The results are considerably less accurate in general, and about 100x slower.

2. What is the difference between our approach and the existing ML-based regression methods?
   * We compared the results with the MLP regressor, Polynomial Interpolation, B-spline Interpolation, and KAN regressor.
   * The MLP regressor is not interpretable and requires a lot of data to fit the model. Polynomial regression is interpretable but not accurate enough, and high-degree polynomials are particularly dangerous for extrapolation beyond the range of fitted data. B-spline interpolation is not interpretable, but it becomes more accurate with an increasing number of knots. KAN is interpretable and accurate in fitting data, but symbolic interpretation requires manual analysis and is not scalable. ML methods mostly generate a black-box model whose inner workings are not easily interpretable, though their predictive power is high. Our method generates a symbolic model that is interpretable and can be used to understand the underlying relationships in the data. We need symbolic representation for the invariants for formal verification and testing purposes.
   * We integrated KAN regressor in Bitween, the results are slow and inaccurate.

3. How do we know the template?
   * For program invariants, we collect the template from those invariants at the location of the program. It is automatic. We can also include some function calls using cheap static analysis.
   * For invariants over function calls such as Random Self-Reducible properties, we provide a template library to the user, derived from mathematical identities, and the user can select the template from the library, or use them all in one shot. 

4. How do we handle the linear regression problems such as collinearity, overfitting, underfitting, etc.?
   * We use Lasso and Ridge regression methods to handle these problems. Additionally, we use the forward selection method to reduce the dimensionality of the problem and the Groebner basis to simplify the invariants. We also pivot the terms and select each as the dependent variable, allowing the method to try different regression models for each term. We also always fall back to MILP models after dimensionality reduction, but in general the use of MILP is costly.

5. How do we handle extrapolation? Is the model robust to unseen data?
   * We deal with mostly continuous functions, not piecewise functions. Therefore, if we predict the model without any error, it is robust to unseen data. Therefore, we expect the users have some knowledge about the domain of the function a priori.

## Reasoning about inequalities
https://chatgpt.com/share/09813f37-323d-427f-882b-f33dcbe6d66c


## Feature Selection
The features are considered unimportant and removed if the corresponding importance of the feature values are below the provided threshold parameter. 

## Forward Feature Selection:
https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SequentialFeatureSelector.html
Transformer that performs Sequential Feature Selection. This Sequential Feature Selector adds (forward selection) or removes (backward selection) features to form a feature subset in a greedy fashion. At each stage, this estimator chooses the best feature to add or remove based on the cross-validation score of an estimator

## Bitween paper

* There has been little progress on the generation of Non-linear invariants involving real-valued variables.
* In this paper, we present a technique to generate algebraic inductive assertions of the form p(x1,...,xn) = 0, where p is a polynomial of fixed degree with real coefficients.
However, the theory used for linear invariants is different from that needed for algebraic invariants. In the linear case, Farkas’ Lemma provides a straightforward way to encode the conditions for being an invariant. 
For the non-linear case, we demonstrate that Groebner bases can be used to reduce the invariant generation problem to a non-linear constraint solving problem that is shown to be in the parametric linear form [2]. We then discuss solution techniques to these constraints, and show that any solution to these constraints is an invariant, thus proving the soundness of our tech- nique. Even though completeness seems achievable in theory,

1. Methods:
	Main Insight: 
		1) Reducing Dimensinality: 
			- Pivoting due regression model, automatically reduces dimension.
                     - Create a model for each term as independent variable.
			- Create models at different degrees from 1 to N
              2) Track coeefficients as Rational numbers in order to support non-integer coeefficients.
              3) Property Testing: Each model should pass this phase over the all dataset.
              4) Construct a model based on most frequent dimensions seen in Regression.

	Multiprocessing: All steps get executed parallel.
	
	1. Contruct Multiple Linear Regression Models (linear, ridge, lasso) with Cross Validation (parallel)
		Reduces Dimension.	
		Generates a linear model for each term.
		Eliminate Dimension having small coefficients

	      * For each linear model, we iteratively run several Linear Regression with reduced dimensions (Serial)
	
	2. Construct MILP Models from Refined Regression Models (parallel):
		Relaxed Encoding with a Linearized Objective Function (L1 distance)
		Scaling for numerical instability due to huge matrix coeefficient ranges (Advanced Scaling): 

		Blocking Evaluation (Serial) to generate simpler models.
              General enough to plug different backends (Gurobi and MILP)

	3. Frequency Refinement Models:
		From each linear model, we collect a Frequency Table, Dimension Reduction (parallel)
		We construct another model from this table. 

	4. If the total dimension of the problem is small, we automatically run MILP over the all dimensions in parallel.

	* We keep all coeefficients as Rational numbers. We can use lcm to eliminate denominators and have integral coeefficients. If the coeeficients are too high we exclude them. Therefore, we don’t need to have always integer coeefficients.

2. Reductions with Groebner Basis.
3. Reductions with Implications.
4. Check satisfiability of the model with Z3


## Forward Selection:
	Decay Rate:

The rate \( r_n \) for a given degree \( n \) is calculated using the formula:

\[ r_n = r_1 \times (1 - p)^{n - 1} \]

where:

\begin{itemize}
    \item \( r_n \) is the rate for degree \( n \),
    \item \( r_1 \) is the initial rate for degree 1,
    \item \( p \) is the decay rate,
    \item \( n \) is the degree.
\end{itemize}

This formula applies an exponential decay to the initial rate \( r_1 \) as the degree \( n \) increases. The term \( (1 - p)^{n - 1} \) represents the decay factor, reducing the initial rate \( r_1 \) as \( n \) becomes larger, which reflects the decreasing rate of feature selection as the degree increases.


