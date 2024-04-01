import math  # noqa
import sympy

from bitween.main import generate_input_data, verify
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

    equations = generate_input_data(
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


test_sin()
