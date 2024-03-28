import math
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


def test_cos():
    def F(x):
        return math.cos(x)

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
        return sympy.cos(x)

    for eq in equations:
        assert verify(eq, f)


def test_tan():
    def F(x):
        return math.tan(x)

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return sympy.tan(x)

    for eq in equations:
        assert verify(eq, f)


def test_tanh():
    def F(x):
        return math.tanh(x)

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return sympy.tanh(x)

    for eq in equations:
        assert verify(eq, f)


def test_cx():
    def F(x, c=5):
        return c * x

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=1,
        n=150,
    )

    def f(x):
        return sympy.Symbol("c") * x

    for eq in equations:
        assert verify(eq, f)


def test_inverse():
    def F(x):
        return 1 / x

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
        return 1 / x

    for eq in equations:
        assert verify(eq, f)


def test_exp():
    def F(x):
        return math.exp(x)

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
        return sympy.exp(x)

    for eq in equations:
        assert verify(eq, f)


def test_exp_minus_one():
    def F(x):
        return math.exp(x) - 1

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
        return sympy.exp(x) - 1

    for eq in equations:
        assert verify(eq, f)


def test_cot():
    def F(x):
        return 1 / math.tan(x)

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return 1 / sympy.tan(x)

    for eq in equations:
        assert verify(eq, f)


def test_inverse_cot_plus_one():
    def cot(x):
        return 1 / math.tan(x)

    def F(x):
        return 1 / (cot(x) + 1)

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return 1 / (sympy.cot(x) + 1)

    for eq in equations:
        assert verify(eq, f)


def test_inverse_tan_plus_one():

    def F(x):
        return 1 / (math.tan(x) + 1)

    equations = generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return 1 / (sympy.tan(x) + 1)

    for eq in equations:
        assert verify(eq, f)


# test_cx()
# test_exp()
# test_exp_minus_one()
# test_tan()
# test_cot()
# test_tanh()
# test_inverse()
# test_inverse_cot_plus_one()
test_inverse_tan_plus_one()

# test_sin()
# test_cos()
