# Synthesizing Random Self-Reducible Properties

Informally, a function $f$ is random-self-reducible if the evaluation of $f$ at any given instance $x$ can be reduced in polynomial time to the evaluation of $f$ at one or more random instances $y_i$.

Our work synthesizes random self-reducible properties for programs satisfying functional equations in the general form $\forall x, y .\ F[f(x-y), f(x+y), f(x), f(y)]=0$, where $F$ is an algebraic function, a function basis, that has the property that, given $f(x-y), f(x+y), f(x), f(y)$, $F$ can be used to efficiently solve for the remaining one. 

Here our goal is to attempt to synthesize this class of functional equation for program $P$ without knowing its specification function $f$. $P$ can compute polynomials and functions that are computable via applying a finite number of known functions (algebraic functions, hyperbolic functions, trigonometric functions, logarithmic and exponential functions).

Since these programs compute real-valued functions, several issues dealing with precision need to be addressed. (i) In many cases, the algorithm is only intended to compute an approximation, e.g., Newton's method. (ii) Representational limitations and round-off/truncation errors are inevitable in real-valued computations. (iii) The representation of some fundamental constants (e.g., $\pi$ = 3.14159...) is inherently imprecise. 

These properties are real-valued nonlinear invariants and they cannot be discovered by existing dynamic invariant generation tools as well as methods based on static analysis. 

## Installation

```bash
$ pip install rsr_property_generation
```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`rsr_property_generation` was created by Ferhat Erata, Timos Antonopoulos. It is licensed under the terms of the MIT license.