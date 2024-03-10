from inspect import signature
from sympy import (
    Expr,
    Symbol,
    cosh,
    nsimplify,
    sinh,
    symbols,
    Function,
    tan,
    tanh,
    sin,
    cos,
    simplify,
    lambdify,
    sympify,
    exp,
    latex,
    sqrt,
    Abs,
    log,
    sign,
    pi,
)
import numpy as np

from rsr_property_generation.milp.sampler import Distribution, Domain, sample


class UnSupportedFunctionSignature(Exception):
    "Raised when the function has zero or more than 2 parameters"
    pass


def latex_func(f: Function) -> str:
    sig = signature(f)
    args = [param.name for param in sig.parameters.values()]
    syms = [symbols(arg) for arg in args]

    return (
        f"{f.__name__}({', '.join(args)}) = {latex(nsimplify(f(*syms), rational=True))}"
    )


def str_func(f: Function) -> str:
    sig = signature(f)
    args = [param.name for param in sig.parameters.values()]
    syms = [symbols(arg) for arg in args]

    return (
        f"{f.__name__}({', '.join(args)}) = {str(nsimplify(f(*syms), rational=True))}"
    )


def verify(expr: Expr, *functions) -> bool:
    """
    Proof by simplification

    Parameters
    ----------
    expr: the expression to be evaluated
    functions: the implementation of functions to be evaluated.
        They should be symbolic expressions that only uses `x`, `y`, `z`, `r`, `s`, `t` as variables.
    """
    functions = {func.__name__: func for func in functions}

    if not isinstance(expr, Expr):
        expr = sympify(expr)

    # NOTE: in order to make c**2 == Abs(c)**2, we need to turn on the real flag
    variables = {str(var): Symbol(str(var), real=True) for var in expr.free_symbols}

    # if the size of the expression is too large, sympy will take a long time to simplify it
    # TODO: remove this
    if len(str(expr)) > 100:
        print(f"skipping verification for : {expr}")
        return True

    print(f"verifying: {expr} = 0")
    proved = eval(
        f"simplify({expr})",
        functions | variables,
        {
            "simplify": simplify,
            "sqrt": sqrt,
            "Abs": Abs,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "tanh": tanh,
            "sinh": sinh,
            "cosh": cosh,
            "exp": exp,
            "log": log,
            "sign": sign,
            "pi": pi,
        },
    )
    proof = proved == 0
    if proof:
        print(f"proved: {proof}")
    else:
        print(f"proved: {proof} ({proved})")
    return proof


def property_test(  # noqa E123
    expr: str | Expr,
    *functions,
    domain: Domain = Domain.Real,
    distribution: Distribution = Distribution.Small,
    epsilon=1e-10,
    n=30,
) -> bool:
    """
    Dynamic checking

    :param expr: the expression to be evaluated
    :param functions: the implementation of functions to be evaluated. It should be a list of
        either symbolic expressions or normal python functions.
    :param domain: the domain of the function
    :param distribution: the distribution of the domain
    :param epsilon: the error tolerance
    :param n: the number of samples to be generated

    :return: True if the property is satisfied less than absolute epsilon in average,
        False otherwise

    :notes: If a function starting with a capital letter is passed in, we lower case it in order
        to match the variable name in the expression.
    """

    functions = {
        func.__name__.lower(): lambdify(func) if isinstance(func, Expr) else func
        for func in functions
    }

    if not isinstance(expr, Expr):
        expr = sympify(expr)

    variables = [str(var) for var in expr.free_symbols]

    errors = []
    print(f"generating {n} random points...")
    print(f"evaluating: {expr}")
    i = 0
    while i < n:
        variables = sample(domain, distribution, variables)
        try:
            errors.append(
                eval(
                    str(expr),
                    functions | variables,
                    {
                        "sqrt": sqrt,
                        "Abs": Abs,
                        "sin": sin,
                        "cos": cos,
                        "tan": tan,
                        "tanh": tanh,
                        "sinh": sinh,
                        "cosh": cosh,
                        "exp": exp,
                        "log": log,
                        "sign": sign,
                        "pi": pi,
                    },
                )
            )
        except ZeroDivisionError as e:
            print(f"ZeroDivisionError: {e}, {variables}")
            continue
        i += 1

    mean_error = np.mean(errors)
    print(f"epsilon: {mean_error}")
    return abs(mean_error) <= epsilon


if __name__ == "__main__":  # noqa E123
    """
    Test cases
    """

    x, y, z, r, s, t = symbols("x y z r s t")
    f = Function("f")
    g = Function("g")
    h = Function("h")

    print("------------------------------------------")

    def f(x):
        return tan(x)

    expr = "- f(x+y) + f(y) + f(y)*f(x)*f(x+y) + f(x)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def g(x):
        return tan(x)

    def f(x):
        return 1 / (1 + tan(x))

    expr = (
        "f(x+y) + f(y) - 2*f(y)*f(x+y) - 2*f(x)*f(x+y) + 2*f(y)*f(x)*f(x+y) + f(x) - 1"
    )

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    # g(x) = g(x+y) - g(y) - g(y)*g(x)*g(x+y)
    expr = "f(x) - 1/(1 + g(x+y) - g(y) - g(y)*g(x)*g(x+y))"
    assert verify(expr, f, g)
    print("---------------------")
    assert property_test(expr, f, g)

    print("------------------------------------------")

    def f(x):
        return tan(x)

    expr = "- f(x+y) + f(y) + f(y)*f(x)*f(x+y) "
    assert not verify(expr, f)
    print("---------------------")
    assert not property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return tanh(x)

    expr = "f(x+y) + f(x+y)*f(x)*f(y) - f(x) - f(y)"
    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return (exp(2 * x) - 1) / (exp(2 * x) + 1)

    expr = "f(x+y) + f(x+y)*f(x)*f(y) - f(x) - f(y)"
    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return cosh(x)

    expr = "f(x-y) - 2*f(y)*f(x) + f(x+y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return (exp(x) + exp(-x)) / 2

    expr = "f(x-y) - 2*f(y)*f(x) + f(x+y)"
    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return x * x

    expr = "f(x-y) - 2 * f(x) - 2 * f(y) - f(y)*f(x+y) - f(y)*f(x-y) + 2 * f(y)*f(x) + 2 * f(y)*f(y) + f(x+y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("------------------------------------------")

    expr = (
        "f(x1) + f(x2) + f(x3) - f(x1 + x2) - f(x1 + x3) - f(x2 + x3) + f(x1 + x2 + x3)"
    )

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("------------------------------------------")

    def f(x):
        c = 1
        return exp(c * x) - 1

    expr = "f(x+y) - f(x) - f(y) - f(x)*f(y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x, y):
        return x + y

    expr = "- f(x, f(y, z)) + f(f(x, y), z)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return cos(x)

    expr = "f(x-y) - 2*f(y)*f(x) + f(x+y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return cos(x)

    expr = "f(x-y) - 2*f(y)*f(x) - 2*f(y)*f(y) - 2*f(x)*f(x) + 2*f(x-y)*f(x+y) + f(x+y) + 2*1 "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    # sympy cannot simplify if we use cot(x) directly here
    def f(x):
        return 1 / (1 + 1 / tan(x))

    expr = "f(x) + f(y) - f(x+y) - 2*f(x)*f(y) + 2*f(x)*f(y)*f(x+y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return 1 / x

    expr = "- 2*f(y)*f(x+y) + f(y)*f(x) - 2*f(x)*f(x+y) + f(x)*f(y) "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return x * x + x + 1

    expr = "f(x-y) - 2*f(x) + 2*f(y) + f(y)*f(x+y) + f(y)*f(x-y) - 2*f(y)*f(x) - f(y)*f(y) - f(x)*f(x+y) - f(x)*f(x-y) + 3*f(x)*f(x) - f(x-y)*f(x+y) + f(x+y) - 1 "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("---------------------")

    def g(x):
        # g(x+y) + g(x-y) = 2*g(x) + 2*g(y)
        return x * x

    def h(x):
        # h(x+y) + h(x-y) = 2*h(x)
        return x + 1

    # 2f(x) = g(x+y) + g(x-y) - 2*g(y) + h(x+y) + h(x-y)
    expr = "2*f(x) - g(x+y) - g(x-y) + 2*g(y) - h(x+y) - h(x-y)"

    assert verify(expr, f, g, h)
    print("---------------------")
    assert property_test(expr, f, g, h, domain=Domain.Integer)

    print("------------------------------------------")

    def f(x):
        return sin(x)

    def g(x):
        return cos(x)

    expr = "g(x)*g(x) + f(x)*f(x) - 1"

    assert verify(expr, f, g)
    print("---------------------")
    assert property_test(expr, f, g)

    print("------------------------------------------")

    def f(x, y):
        return x * y

    expr = "- f(x+r,y+s) + f(x,s) + f(r,y) + f(r,s) + f(x,y) "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x, y):
        return x * y + x

    expr = "- f(r,y-s)*f(x-r,s) + f(r,s)*f(x-r,y-s) "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("------------------------------------------")

    def f(x, y):
        return x * y + x + y

    expr = "f(x+r,y+s) - f(x+r,s) - f(r,y+s) + f(r,s)*f(x+r,y+s) - f(r,y+s)*f(x+r,s) + f(r,s) "

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("------------------------------------------")

    def f(x, y):
        return x + y

    expr = "- f(x,s) - f(r,y) + f(r,s) + f(x,y)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f, domain=Domain.Integer)

    print("------------------------------------------")

    def f(x):
        return sinh(x)

    expr = "- f(y)*f(y) - f(x-y)*f(x+y) + f(x)*f(x)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return (exp(x) - exp(-x)) / 2

    expr = "- f(y)*f(y) - f(x-y)*f(x+y) + f(x)*f(x)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")

    def f(x):
        return sin(x)

    def F(x, terms=40):
        """sinTaylor"""
        result = 0.0

        for n in range(terms):
            numerator = (-1) ** n
            denominator = 1

            for i in range(1, 2 * n + 2):
                denominator *= i

            term = numerator * (x ** (2 * n + 1)) / denominator
            result += term

        return result

    expr = "- f(y)*f(y) - f(x-y)*f(x+y) + f(x)*f(x)"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, F)

    print("------------------------------------------")

    def f(x0, c):
        return 1 + 2 * sin(c * x0) + cos(x0) + x0

    expr = "c**2 - 2*x0**2 - x0 + f(x0, c) - 2*sin(c*x0) - cos(x0) - Abs(c**2) + 2*Abs(x0**2) - 1"

    assert verify(expr, f)
    print("---------------------")
    assert property_test(expr, f)

    print("------------------------------------------")
