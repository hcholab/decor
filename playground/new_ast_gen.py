from itertools import product
import random

from sympy import (  # noqa F401
    Expr,
    Symbol,
    cosh,
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


x, y, z, r, s, t = symbols("x y z r s t")
# f = Function("f")(x, y)
# g = Function("g")(x)
# h = Function("h")(x, y)


# Function to generate all expressions up to a given depth
def generate_all_expressions(leaf_terms, symbolic_functions, depth):
    if depth == 0:
        return [sympify(term) for term in leaf_terms]

    prev_level_exprs = generate_all_expressions(
        leaf_terms, symbolic_functions, depth - 1
    )
    all_exprs = set(prev_level_exprs)

    for func in symbolic_functions:
        if not isinstance(func, Expr):
            func = sympify(func)
        arg_count = len(func.free_symbols)
        for args in product(prev_level_exprs, repeat=arg_count):
            all_exprs.add(func.subs(zip(func.free_symbols, args)))

    return list(all_exprs)


def sample(variables: list[str | Symbol]):
    values = {}
    for var in variables:
        values[str(var)] = random.random() * 10 - 5

    return values


# Example usage

n = 2  # number of random points to generate
# Generate all expressions
all_expressions = generate_all_expressions(
    leaf_terms=["x", "y"], symbolic_functions=["g(x)", "f(x,y)", "h(x,y)"], depth=2
)

for i, expr in enumerate(all_expressions):
    print(i, ":", expr)


# Define the actual operations for f, g, h
def f(x, y):
    return x * y


def g(x):
    return sin(x)


def h(x, y):
    return x + y


implementation_map = {"f": f, "g": g, "h": h}

variables = set()
for expr in all_expressions:
    for var in expr.free_symbols:
        variables.add(str(var))


values = []
print(f"generating {n} random points...")
print(f"evaluating: {expr}")
for k in range(n):
    for i, expr in enumerate(all_expressions):
        variables = sample(variables)
        try:
            values.append(
                eval(
                    str(expr),
                    implementation_map | variables,
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

        print(i, ":", expr, "=", values[i])
    print(f"--Sample {k+1}--")
