import math
import numpy
import sympy

from bitween.main import infer_property, verify
from bitween.sampler import Domain, Distribution

from bitween import miscs
from bitween.config import Config, MILPSolver

from time import time

config = Config()
log = miscs.getLogger(__name__, config.logger_level)


def test_sin():
    def F(x):
        return math.sin(x)

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
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
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
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
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
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=300,
    )

    def f(x):
        return sympy.tanh(x)

    for eq in equations:
        verify(eq, f)


def test_cosh():
    def F(x):
        return math.cosh(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        n=150,
    )

    def f(x):
        return sympy.cosh(x)

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


def test_sec():
    def F(x):
        return 1 / math.cos(x)

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
        return 1 / sympy.cos(x)

    for eq in equations:
        assert verify(eq, f)


def test_csc():
    def F(x):
        return 1 / math.sin(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        # ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=4,
        n=200,
    )

    def f(x):
        return 1 / sympy.sin(x)

    for eq in equations:
        verify(eq, f)


def test_arcsin():
    def F(x):
        return math.asin(x)

    equations = infer_property(
        Domain.Real,
        Distribution.UltraTiny,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        # ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=3,
        epsilon=1e-5,
        n=200,
    )

    def f(x):
        return sympy.asin(x)

    for eq in equations:
        verify(eq, f)


def test_arccos():
    def F(x):
        return math.acos(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Tiny,
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=5,
        epsilon=1e-5,
        n=200,
    )

    def f(x):
        return sympy.acos(x)

    for eq in equations:
        verify(eq, f)


def test_arccot():
    def F(x):
        return math.acot(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=3,
        n=200,
    )

    def f(x):
        return sympy.acot(x)

    for eq in equations:
        verify(eq, f)


def test_arcsinh():
    def F(x):
        return numpy.arcsinh(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],
        F,
        max_degree=4,
        n=200,
    )

    def f(x):
        return sympy.asinh(x)

    for eq in equations:
        verify(eq, f)


def test_cot():
    def F(x):
        return 1 / math.tan(x)

    equations = infer_property(
        Domain.Real,
        Distribution.Small,
        # ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        # ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        ["F(x+y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=4,
        n=150,
    )

    def f(x):
        return 1 / sympy.tan(x)

    for eq in equations:
        assert verify(eq, f)


if __name__ == "__main__":
    st = time()

    # Find closed formulas for the following:
    # 1. cosecont, secant, cotangent,
    # 2. arcsin(x), arccos(x), arctan(x), arccsc(x), arcsec(x), arccot(x), and
    # 3. all hyperbolic function

    # NOTE: sine
    # f(x)**2 - f(x+y)*f(x-y) - f(y)**2 = 0
    # test_sin()

    # NOTE: cosine
    # f(x)**2 - 2*f(x)*f(x+y)*f(y) + f(x+y)**2 + f(y)**2 - 1 = 0
    # 2*f(x)*f(y) - f(x+y) - f(x-y) = 0;
    # f(x)**2 - f(x+y)*f(x-y) + f(y)**2 - 1 = 0;
    # test_cos()

    # NOTE: tangent
    # f(x)*f(x+y)*f(y) + f(x) - f(x+y) + f(y) = 0
    # test_tan()

    # NOTE: secant
    # f(x)*f(x+y)*f(y) + f(x)*f(x-y)*f(y) - 2*f(x+y)*f(x-y) = 0
    # test_sec()

    # NOTE: cosecant
    # f(x)**2*f(x+y)*f(x-y) + f(x)**2*f(y)**2 - f(x+y)*f(x-y)*f(y)**2 = 0
    # test_csc()

    # NOTE: cotangent
    # f(x)*f(x+y) - f(x)*f(y) + f(x+y)*f(y) + 1 = 0
    # f(x)*f(x+y) - f(x)*f(x-y) - 2*f(x)*f(y) + f(x+y)*f(y) + f(x-y)*f(y) = 0
    # test_cot()

    # NOTE: hyperbolic tangent
    # f(x)*f(x+y)*f(y) - f(x) + f(x+y) - f(y) = 0
    # test_tanh()

    # NOTE: hyperbolic cosine
    # f(x)**2 - f(x+y)*f(x-y) + f(y)**2 - 1 = 0
    # 2*f(x)*f(y) - f(x+y) - f(x-y) = 0
    # f(x)**2 - 2*f(x)*f(x+y)*f(y) + f(x+y)**2 + f(y)**2 - 1 = 0
    # test_cosh()

    # NOTE: hyperbolic sine
    # f(x)**2 - f(x+y)*f(x-y) - f(y)**2 = 0
    # test_sinh()

    # NOTE: arcsine (inverse sine)
    # Not found
    # test_arcsin()

    # NOTE: arccosine (inverse cosine)
    # Not found
    # test_arccos()

    # NOTE: arctangent (inverse tangent)
    # Not found
    # test_arctan()

    # NOTE: arcsinh (inverse hyperbolic sine)
    # Not found
    test_arcsinh()

    log.debug(f"Total Time: {time() - st:.2f}s")
