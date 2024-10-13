import math
import sympy

from bitween.main import infer_property, verify
from bitween.sampler import Domain, Distribution

from bitween import miscs
from bitween.config import Config, MILPSolver

from time import time

config = Config()
log = miscs.getLogger(__name__, config.logger_level)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        n=80,
    )

    def f(x):
        return sympy.tanh(x)

    for eq in equations:
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


def test_exp_div_by_x_composite():
    def F(x):
        return math.exp(x) / x

    def H(x):
        return math.exp(x)

    def P(x, y):
        return x + y

    equations = infer_property(
        Domain.Real,
        Distribution.Tiny,
        ["F(x+y)", "H(x)", "H(y)", "P(x,y)"],
        ["f(x+y)", "h(x)", "h(y)", "p(x,y)"],
        F,
        H,
        P,
        max_degree=2,
        n=150,
    )

    def f(x):
        return sympy.exp(x) / x

    def h(x):
        return sympy.exp(x)

    def p(x, y):
        return x + y

    for eq in equations:
        verify(eq, f, h, p)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


def test_inverse_square():

    def F(x):
        return 1 / (x**2)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x)", "F(y)", "F(x-y)"],
        ["f(x+y)", "f(x)", "f(y)", "f(x-y)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x):
        return 1 / (x**2)

    for eq in equations:
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        epsilon=0.001,
    )

    def f(x):
        return x / (1 - x)

    for eq in equations:
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


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
        verify(eq, f)


def test_cube():

    def F(x):
        return x**3

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
        return x**3

    for eq in equations:
        verify(eq, f)


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
        verify(eq, f)


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
        return 2 / (1 + sympy.exp(-x))

    for eq in equations:
        verify(eq, f)


def test_logistic(L=3, k=2, x0=0):

    def F(x):
        return L / (1 + math.exp(-k * (x - x0)))

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
        return L / (1 + sympy.exp(-k * (x - x0)))

    for eq in equations:
        verify(eq, f)


def test_softmax2_1():
    def F(x, y):
        return math.exp(x) / (math.exp(x) + math.exp(y))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y, y+z)", "F(x, y)", "F(y, z)", "F(x, z)"],
        ["f(x+y, y+z)", "f(x, y)", "f(y, z)", "f(x, z)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x, y):
        return sympy.exp(x) / (sympy.exp(x) + sympy.exp(y))

    for eq in equations:
        verify(eq, f)


def test_softmax2_2():
    def F(x, y):
        return math.exp(y) / (math.exp(x) + math.exp(y))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y, y+z)", "F(x, y)", "F(y, z)", "F(x, z)"],
        ["f(x+y, y+z)", "f(x, y)", "f(y, z)", "f(x, z)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x, y):
        return sympy.exp(y) / (sympy.exp(x) + sympy.exp(y))

    for eq in equations:
        verify(eq, f)


def test_softmax2_alt_1():
    def F(x, y):
        return math.exp(x) / (math.exp(x) + math.exp(y))

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x1+x2, y1+y2)", "F(x1, y1)", "F(x2, y1)", "F(x1, y2)", "F(x2, y2)"],
        ["f(x1+x2, y1+y2)", "f(x1, y1)", "f(x2, y1)", "f(x1, y2)", "f(x2, y2)"],
        F,
        max_degree=2,
        n=150,
    )

    def f(x, y):
        return sympy.exp(x) / (sympy.exp(x) + sympy.exp(y))

    for eq in equations:
        verify(eq, f)


def test_arctan():
    def F(x):
        return math.atan(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Tiny,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=3,
        n=200,
        milp=MILPSolver.GLPK,
    )

    def f(x):
        return sympy.atan(x)

    for eq in equations:
        verify(eq, f)


def test_mod():
    def F(x, R=101):
        return x % R

    equations = infer_property(
        Domain.Positive_Integer,
        Distribution.Small,
        ["F(x+y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x)", "f(y)"],
        F,
        max_degree=1,
        n=100,
    )

    def f(x, R=101):
        return sympy.Mod(x, R)

    for eq in equations:
        verify(eq, f)


def test_mod_mult():
    def F(x, y, R=100001):
        return (x * y) % R

    equations = infer_property(
        Domain.Positive_Integer,
        Distribution.Small,
        ["F(x1+x2, y1+y2)", "F(x1, y1)", "F(x2, y1)", "F(x1, y2)", "F(x2, y2)"],
        ["f(x1+x2, y1+y2)", "f(x1, y1)", "f(x2, y1)", "f(x1, y2)", "f(x2, y2)"],
        F,
        max_degree=1,
        n=100,
    )

    def f(x, y, R=100001):
        return (x * y) % R

    for eq in equations:
        verify(eq, f)


def test_mult():
    def F(x, y):
        return x * y

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x1+x2, y1+y2)", "F(x1, y1)", "F(x2, y1)", "F(x1, y2)", "F(x2, y2)"],
        ["f(x1+x2, y1+y2)", "f(x1, y1)", "f(x2, y1)", "f(x1, y2)", "f(x2, y2)"],
        F,
        max_degree=1,
        n=150,
    )

    def f(x, y):
        return x * y

    for eq in equations:
        verify(eq, f)


def test_sinc_composite():
    def F(x):
        return math.sin(x) / x

    def RSR_SIN(x, y):
        return (math.sin(x) ** 2 - math.sin(y) ** 2) / math.sin(x - y)

    def RSR_X(x, y):
        return x + y

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "RSR_SIN(x,y)", "RSR_X(x,y)"],
        ["f(x+y)", "rsr_sin(x,y)", "rsr_x(x,y)"],
        F,
        RSR_SIN,
        RSR_X,
        max_degree=2,
        n=50,
    )

    def f(x):
        return sympy.sin(x) / x

    def rsr_sin(x, y):
        return (sympy.sin(x) ** 2 - sympy.sin(y) ** 2) / sympy.sin(x - y)

    def rsr_x(x, y):
        return x + y

    for eq in equations:
        verify(eq, f, rsr_sin, rsr_x)


def test_sinc():
    def F(x):
        return math.sin(x) / x

    def P(x, y):
        return x + y

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "sin(x)", "sin(y)", "sin(x-y)", "P(x,y)"],
        ["f(x+y)", "sin(x)", "sin(y)", "sin(x-y)", "p(x,y)"],
        F,
        P,
        sum,
        max_degree=3,
        n=150,
    )

    def f(x):
        return sympy.sin(x) / x

    def p(x, y):
        return x + y

    for eq in equations:
        verify(eq, f, p)


def test_log():
    def F(x):
        return math.log(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x*y)", "F(x)", "F(y)"],
        ["f(x*y)", "f(x)", "f(y)"],
        F,
        max_degree=1,
        n=50,
    )

    def f(x):
        return sympy.log(x)

    for eq in equations:
        verify(eq, f)


def test_square_loss():
    def F(v):
        return (1 - v) ** 2

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
        return (1 - x) ** 2

    for eq in equations:
        verify(eq, f)


if __name__ == "__main__":
    st = time()

    # test_identity()
    # test_exp()
    # test_sigmoid()
    # test_exp_minus_one()
    # test_exp_div_by_x()  # no solution
    # test_exp_div_by_x_composite()
    # test_floudas()
    # test_mean()
    # test_tan()
    # test_cot()
    # test_tanh()
    # test_diff_x2_y2()
    # test_inverse_square()
    # test_inverse()
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
    # test_arctan()  # No solution
    # test_mod()
    # test_mod_mult()
    # test_mult()

    # https://en.wikipedia.org/wiki/Logistic_function
    # test_logistic()

    # https://en.wikipedia.org/wiki/Softmax_function
    # test_softmax2_1()
    # test_softmax2_2()
    # test_softmax2_alt_1()  # no solution

    # https://en.wikipedia.org/wiki/Sinc_function
    test_sinc()
    # test_sinc_composite()

    # test_cube()
    # test_log()

    # loss functions:https://en.wikipedia.org/wiki/Loss_functions_for_classification
    test_square_loss()

    log.debug(f"Total Time: {time() - st:.2f}s")
