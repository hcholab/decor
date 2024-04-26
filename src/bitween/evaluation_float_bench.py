import math
import sympy

from bitween.main import infer_property, verify
from bitween.sampler import Domain, Distribution


def test_sin():
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

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return sympy.sin(x)

    for eq in equations:
        assert verify(eq, f)


def test_sqrt():

    def F(x):
        return math.sqrt(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        # [MILP(k=4, timeout=3, max_bound=10, obj=1e-12)],  # methods
        ["F(x)", "F(x+1)", "x", "1"],
        ["f(x)", "f(x+1)", "x", "1"],
        F,
        max_degree=2,
        n=30,
    )
    # NOTE: x - f(x + 1)**2 + 1 = 0
    # NOTE: f(x)**2 - f(x + 1)**2 + 1 = 0
    # NOTE: x - f(x)**2 = 0

    def f(x):
        return sympy.sqrt(x)

    for eq in equations:
        assert verify(eq, f)


def test_sin_periodic():
    def f(x):
        return math.sin(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["f(x+pi)", "f(x-pi)", "f(x)", "f(-x)", "1"],
        ["f(x+pi)", "f(x-pi)", "f(x)", "f(-x)", "1"],
        f,
        max_degree=1,
        n=30,
        epsilon=1e-13,
    )

    def f(x):
        return sympy.sin(x)

    for eq in equations:
        assert verify(eq, f)


test_sin()
test_sqrt()
