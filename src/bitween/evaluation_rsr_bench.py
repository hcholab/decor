import math
import sympy

from bitween.main import infer_property, verify
from bitween.sampler import Domain, Distribution
from bitween.settings import MILPSolver


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


def test_cos():
    def F(x):
        return math.cos(x)

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
        return sympy.cos(x)

    for eq in equations:
        assert verify(eq, f)


def test_tan():
    def F(x):
        return math.tan(x)

    equations = infer_property(
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

    equations = infer_property(
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


def test_identity():
    def F(x, c=5):
        return c * x

    equations = infer_property(
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
        return 1 / x

    for eq in equations:
        assert verify(eq, f)


def test_inverse_add():
    def F(x):
        return 1 / (x + 1)

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
        return 1 / (x + 1)

    for eq in equations:
        assert verify(eq, f)


# double sqrt_add(double x) { return 1.0 / (sqrt((x + 1.0)) + sqrt(x)); }
def test_sqrt_add():
    def F(x):
        return 1.0 / (math.sqrt((x + 1.0)) + math.sqrt(x))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=5,
        n=1000,
        precondition=lambda x: x > 0,
        milp=MILPSolver.GLPK,
    )

    def f(x):
        return 1.0 / (sympy.sqrt((x + 1.0)) + sympy.sqrt(x))

    for eq in equations:
        assert verify(eq, f)


def test_exp():
    def F(x):
        return math.exp(x)

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
        return sympy.exp(x)

    for eq in equations:
        assert verify(eq, f)


# double exp1x(double x) { return (exp(x) - 1.0) / x; }
def test_exp_div_by_x():
    def F(x):
        return math.exp(x) / x

    equations = infer_property(
        Domain.Real,
        Distribution.Tiny,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=5,
        n=200,
    )

    def f(x):
        return sympy.exp(x) / x

    for eq in equations:
        assert verify(eq, f)


# double exp1x_log(double x) { return (exp(x) - 1.0) / log(exp(x)); }
def test_exp_div_by_log():
    def F(x):
        return (math.exp(x) - 1.0) / math.log(math.exp(x))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return (sympy.exp(x) - 1.0) / sympy.log(sympy.exp(x))

    for eq in equations:
        assert verify(eq, f)


# double floudas(double x1, double x2) { return x1 + x2; }
def test_floudas():
    def F(x1, x2):
        return x1 + x2

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        [
            "F(x1+x2,y1+y2)",
            "F(x2+x3,y2+y3)",
            "F(x1+x3,y1+y3)",
            "F(x1,y1)",
            "F(x2,y2)",
        ],
        [
            "f(x1+x2,y1+y2)",
            "f(x2+x3,y2+y3)",
            "f(x1+x3,y1+y3)",
            "f(x1,y1)",
            "f(x2,y2)",
        ],
        F,
        max_degree=1,
        n=150,
        precondition=lambda x1, x2: 0 <= x1 <= 2 and 0 <= x2 <= 3 and x1 + x2 <= 2,
    )

    def f(x1, x2):
        return x1 + x2

    for eq in equations:
        assert verify(eq, f)


def test_mean():
    def F(x, y, z):
        return 1 / 3 * (x + y + z)

    equations = infer_property(
        Domain.Integer,
        Distribution.Small,
        # fmt: off
        ["F(x1+x2+x3, y1+y2+y3, z1+z2+z3)", "F(x1+x2,y1+y2,z1+z2)", "F(x2+x3,y2+y3,z2+z3)", "F(x1+x3,y1+y3,z1+z3)", "F(x1,y1,z1)", "F(x2,y2,z2)", "F(x3,y3,z3)"],
        ["f(x1+x2+x3, y1+y2+y3, z1+z2+z3)", "f(x1+x2,y1+y2,z1+z2)", "f(x2+x3,y2+y3,z2+z3)", "f(x1+x3,y1+y3,z1+z3)", "f(x1,y1,z1)", "f(x2,y2,z2)", "f(x3,y3,z3)"],
        # fmt: on
        F,
        max_degree=1,
        n=150,
    )

    def f(x, y, z):
        return 1 / 3 * (x + y + z)

    for eq in equations:
        assert verify(eq, f)


def test_diff_x2_y2():
    def F(x1, x2):
        return x1**2 - x2**2

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        # fmt: off
        ["F(x-a,y-b)", "F(x+a,y-b)", "F(x,y)", "F(a,b)", "F(x-a, y)", "F(x+a, y)", "F(x, y-a)", "F(x, y+a)"],
        ["f(x-a,y-b)", "f(x+a,y-b)", "f(x,y)", "f(a,b)", "f(x-a,y)", "f(x+a,y)", "f(x,y-a)", "f(x,y+a)"],
        # fmt: on
        F,
        max_degree=3,
        n=1000,
    )

    def f(x1, x2):
        return x1**2 - x2**2

    for eq in equations:
        assert verify(eq, f)


def test_exp_minus_one():
    def F(x):
        return math.exp(x) - 1

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
        return sympy.exp(x) - 1

    for eq in equations:
        assert verify(eq, f)


def test_cot():
    def F(x):
        return 1 / math.tan(x)

    equations = infer_property(
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

    def F(x):
        return 1 / (1 / math.tan(x) + 1)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
        # milp=MILPSolver.GUROBI,
        # var_bound=4,
    )

    def f(x):
        return 1 / (1 / sympy.tan(x) + 1)

    for eq in equations:
        assert verify(eq, f)


def test_inverse_tan_plus_one():

    def F(x):
        return 1 / (math.tan(x) + 1)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return 1 / (sympy.tan(x) + 1)

    for eq in equations:
        assert verify(eq, f)


def test_x_over_one_minus_x():
    def F(x):
        return x / (1 - x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=2,
        n=1000,
        delta=0.001,
    )

    def f(x):
        return x / (1 - x)

    for eq in equations:
        assert verify(eq, f)


def test_minus_x_over_one_minus_x():
    def F(x):
        return -x / (1 - x)

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
        return -x / (1 - x)

    for eq in equations:
        assert verify(eq, f)


# f(x)=\frac{\sin cx}{\sin(cx+a)
def test_sin_over_sin():
    def F(x, a=math.radians(90), c=1):
        return math.sin(c * x) / math.sin(c * x + a)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=3,
        n=300,
    )

    def f(x):
        return sympy.sin(x) / sympy.sin(x + 1)

    for eq in equations:
        verify(eq, f)


# f(x)=\frac{\sinh cx}{\sinh(cx+a)
def test_sinh_over_sinh():
    def F(x, a=1, c=1):
        return math.sinh(c * x) / math.sinh(c * x + a)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return sympy.sinh(x) / sympy.sinh(x + 1)

    for eq in equations:
        assert verify(eq, f)


def test_cosh():
    def F(x):
        return math.cosh(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return sympy.cosh(x)

    for eq in equations:
        assert verify(eq, f)


def test_squared():
    def F(x):
        return x**2

    equations = infer_property(
        Domain.Integer,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return x**2

    for eq in equations:
        assert verify(eq, f)


def test_sinh():
    def F(x):
        return math.sinh(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return sympy.sinh(x)

    for eq in equations:
        assert verify(eq, f)


def test_sigmoid():
    def F(x):
        return 1 / (1 + math.exp(-x))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return 1 / (1 + sympy.exp(-x))

    for eq in equations:
        assert verify(eq, f)


# test_identity()
# test_exp()
# test_sigmoid()
# test_exp_minus_one()
# test_exp_div_by_x()  # no solution
# test_floudas()
# test_mean()
# test_tan()
# test_cot()
# test_tanh()
# test_diff_x2_y2()
# test_sqrt_add()  # no solution
test_inverse()
# test_inverse_add()
# test_inverse_cot_plus_one()
# test_inverse_tan_plus_one()
# test_x_over_one_minus_x()
# test_minus_x_over_one_minus_x()
# test_sin_over_sin() # TODO fails
# test_sinh_over_sinh() # TODO fails
# test_cos()
# test_cosh()
# test_squared()
# test_sin()
# test_sinh()
