from gurobipy import GRB
import gurobipy as gp
import csv
import time

from sklearn.feature_selection import (  # noqa F401
    SelectKBest,
    f_regression,
    mutual_info_regression,
)
from sklearn.metrics import mean_absolute_error  # noqa F401
from sklearn.model_selection import train_test_split  # noqa F401
from sympy import sin, cos, tan, cot, exp, symbols, Function  # noqa F401
from sympy import sqrt, sign, Abs, log  # noqa F401
import numpy as np

from sklearn.linear_model import Lasso, LinearRegression  # noqa F401

from rsr_property_generation.milp.sampler import Domain, Distribution, sample
from rsr_property_generation.milp.terms import canonicalize, get_values_terms
from rsr_property_generation.milp.utilities import pp
from rsr_property_generation.milp.verifier import property_test, verify

if __name__ == "__main__":  # noqa E123
    degree = None
    importantVarName = "?"
    block = None
    domain = Domain.Real
    distribution = Distribution.Small
    BOUND = 2
    N = 300

    ERROR_BOUND = 0.3  # 0.05

    x, y, z, r, s, t = symbols("x y z r s t")
    f = Function("f")
    g = Function("g")
    h = Function("h")
    u = Function("u")
    v = Function("v")
    w = Function("w")
    F = Function("F")
    G = Function("G")
    H = Function("H")
    U = Function("U")
    V = Function("V")
    W = Function("W")

    def g():
        return 1

    def h():
        return 1

    def u():
        return 1

    def var():
        return 1

    def w():
        return 1

    # start timer
    start = time.time()

    # clear the file
    with open("data.csv", mode="w", newline="") as file:
        file.write("")  # Write an empty string to clear the file

    with open("data.csv", mode="a", newline="\n") as file:
        writer = csv.writer(file)

        important = None

        to_be_removed_from_model = []

        k = N
        while k > 0:
            # print(".", end="", flush=True)
            x, y, z, r, s, t = tuple(
                sample(domain, distribution, ["x", "y", "z", "r", "s", "t"]).values()
            )

            # TODO: add x+y = 0 or x-y = 0 or x = 0 or y = 0
            # TODO: add x+y = 1 or x-y = 1 or x = 1 or y = 1

            # def f(x, y):
            #     return 1 + 2 * sin(x * y) + cos(x) + y**2

            # degree = 3
            # importantVarName = "f(x, y)"
            # BOUND = 10
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x, y), x, y, 1],
            #     ["f(x, y)", "x", "y", "1"],
            #     "1",
            #     "x",
            #     "sin(x)",
            #     "cos(x)",
            #     "tan(x)",
            #     "sign(x)",
            #     "Abs(x)",
            #     # "log(x)",
            #     depth=1,
            # )

            # def f(x):
            #     return cos(x)

            # degree = 5
            # importantVarName = "f(x+y)"
            # BOUND = 10
            # # block = "f(x-y)*f(x+y)"
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH:   f(x+y) + f(x-y) = 2 f(x)*f(y)
            # NOTE: LIN-REG: f(x+y) = + -1.0*f(x-y) + 2.0*f(y)*f(x) + -0.05*f(y)*f(y) + -0.05*f(x)*f(x) + 0.05*f(x-y)*f(x+y)  + 0.05
            # NOTE: MILP OK: f(x-y) - 2*f(y)*f(x) + f(x+y) = 0 (-4.996003610813204e-16) (block: f(x-y)*f(x+y)) (bound: 2)
            # NOTE: MILP OK: f(x-y) - 2*f(y)*f(x) - 2*f(y)*f(y) - 2*f(x)*f(x) + 2*f(x-y)*f(x+y) + f(x+y) + 2*1 = 0 (-3.1086244689504383e-15) (block: None) (bound: 2)
            # NOTE: (https://chat.openai.com/share/d4e86e99-df69-4aff-9854-a47f625ddf11)

            # def f(x):
            #     return sqrt(x)

            # if x + y < 0 or x - y < 0 or x < 0 or y < 0:
            #     continue

            # def P(x, precision=0.0001):
            #     guess = x / 2.0
            #     while abs(guess * guess - x) > precision:
            #         guess = (guess + x / guess) / 2.0
            #     return guess

            # degree = 2
            # importantVarName = "f(y)*f(y)"
            # # importantVarName = "f(x+y)"
            # BOUND = 4
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: f(x)**2 - f(y)**2 - f(x - y)**2 = 0

            # def f(x):
            #     return 1 / sqrt(x)

            # import ctypes
            # import os

            # pwd = os.path.dirname(os.path.abspath(__file__))
            # so_file = pwd + "/quake.so"

            # functions = ctypes.CDLL(so_file)

            # invsqrt = functions.invsqrt
            # invsqrt.argtypes = [ctypes.c_float]
            # invsqrt.restype = ctypes.c_float

            # if x > 0 or sqrt(x) == 0:
            #     print(f"sqrt({x}) = {sqrt(x)}")
            #     continue

            # def P(x):
            #     return invsqrt(x)

            # degree = 1
            # importantVarName = "f(x)"
            # BOUND = 1
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [P(x), x, y, 1.0],
            #     ["f(x)", "x", "y", "1"],
            #     "1",
            #     "x",
            #     # "sin(x)",
            #     # "cos(x)",
            #     # "tan(x)",
            #     # "sign(x)",
            #     # "Abs(x)",
            #     "sqrt(x)",
            #     depth=1,
            # )

            # def f(x, y):
            #     return sqrt(x * y)

            # if (
            #     x * y < 0
            #     or (x + r) * (y + s) < 0
            #     or (x + r) * s < 0
            #     or r * (y + s) < 0
            #     or r * s < 0
            # ):
            #     continue

            # def P(x, y, precision=0.0001):
            #     guess = x * y / 2.0
            #     while abs(guess * guess - x * y) > precision:
            #         guess = (guess + x * y / guess) / 2.0
            #     return guess

            # degree = 2
            # # importantVarName = "f(x+r,y+s)"
            # importantVarName = "f(x,y)*f(x,y)"
            # BOUND = 10
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x, y), f(x + r, y + s), f(x + r, s), f(r, y + s), f(r, s), "1"],
            #     ["f(x,y)", "f(x+r,y+s)", "f(x+r,s)", "f(r,y+s)", "f(r,s)", "1"],
            #     "1",
            # )
            # NOTE: f(r, s)**2 - f(r, s + y)**2 - f(x, y)**2 - f(r + x, s)**2 + f(r + x, s + y)**2 = 0

            # def factorial(n):
            #     if n == 0:
            #         return 1
            #     else:
            #         return n * factorial(n - 1)

            # def P(x, terms=60):
            #     # NOTE: when terms=20 or 40, the prop does not meet the obj. func
            #     """
            #     sigmoid function
            #     ----------------
            #     Taylor approximation of sigmoid function
            #     `S(x) = 1/2 + x/4 - x^3/48 + x^5/4800 - ...`
            #     """
            #     exp_approx = 1 + sum(
            #         [((-1) ** n) * (x**n) / factorial(n) for n in range(1, terms)]
            #     )
            #     return 1 / (1 + 1 / exp_approx)

            # def f(x):
            #     return 1 / (1 + exp(-x))

            # degree = 3
            # importantVarName = "f(x)"
            # # importantVarName = "f(x+y)"
            # BOUND = 10
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x * y), f(x + y), f(x - y), f(x), f(y), 1.0],
            #     ["f(x*y)", "f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: 2*f(x)*f(y)*f(x - y) - f(x)*f(y) - f(x)*f(x - y) + f(x) - f(y)*f(x - y) = 0

            # def f(x):
            #     return x * (sign(x) + 1) / 2

            # degree = 3
            # importantVarName = "f(y)*f(y)"
            # # importantVarName = "f(x)*f(x)"
            # # importantVarName = "f(y)*f(x)"
            # # importantVarName = "f(x+y)"
            # BOUND = 4
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1.0],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE:

            # def cot(x):
            #     return 1 / tan(x)

            # def f(x):
            #     return 1 / (1 + cot(x))

            # degree = 3
            # importantVarName = "f(x)"
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x) = + 1.0*f(x+y) + -1.0*f(y) + 2.0*f(y)*f(x) + -2.0*f(y)*f(x)*f(x+y)
            # NOTE: milp property: - f(x+y) + f(y) - 2*f(y)*f(x) + 2*f(y)*f(x)*f(x+y) + f(x) = 0 (-1.1821099654696354e-13) (block: None) (bound: 2)

            # def f(x):
            #     return 1 / x

            # degree = 3
            # importantVarName = "f(y)*f(x)"
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH:   f(x+y)f(x) + f(x+y)f(y) =  f(x)*f(y)
            # NOTE: lin. property: f(y)*f(x) = + 1.0*f(y)*f(x+y) + 1.0*f(x)*f(x+y)
            # NOTE: milp property: - f(y)*f(x+y) - f(x)*f(x+y) + f(y)*f(x) = 0 (-2.914335439641036e-16) (block: None) (bound: 2)
            # NOTE: Scale

            # def f(x):
            #     return x * x

            # degree = 1
            # importantVarName = "f(x+y)"
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # #######################################
            # degree = 6
            # importantVarName = "f(x+y)"
            # BOUND = 10
            # (terms, termNames) = get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH:   f(x+y) + f(x-y) = 2f(x) + 2f(y)
            # NOTE: LIN-REG: f(x+y) = + -1.0*f(x-y) + 2.0*f(x) + 2.0*f(y)
            # NOTE: MILP OK: f(x-y) - 2 f(x) - 2 f(y) + f(x+y) = 0 (-6.574794042535359e-10)
            # ----
            # NOTE: MILP OK: f(x-y) - 2 f(x) - 2 f(y) - f(y)*f(x+y) - f(y)*f(x-y) + 2 f(y)*f(x) + 2 f(y)*f(y) + f(x+y) = 0 (-1.1292754439895525e-09
            # (Scale)
            # https://chat.openai.com/share/912e5c03-ca22-4f5c-b2d7-326c8d4040bc

            # c = 14

            # def f(x):
            #     return c * x

            # degree = 1
            # importantVarName = "f(x+y)"
            # # importantVarName = "f(x-y)*f(x+y)"
            # domain = Domain.Integer
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x+y) = + 1.0*f(x) + 1.0*f(y)
            # NOTE: milp property: - f(x) - f(y) + f(x+y) = 0 (0.0) (block: None) (bound: 1)
            # NOTE: milp property: - f(x-y) - 2*f(y) + f(x+y) = 0 (-7.105427357601002e-15) (block: None) (bound: 2)
            # NOTE: milp property: - 2*f(x-y) + f(x) - 3*f(y) + f(x+y) = 0 (-1.4210854715202004e-14) (block: None) (bound: 3)

            # def f(x):
            #     return x * x + x + 1

            # degree = 2
            # importantVarName = "f(x+y)"
            # domain = Domain.Integer
            # BOUND = 4
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x+y) = + -1.0*f(x-y) + 2.0*f(x) + 0.03*f(y) + 0.01*f(y)*f(x+y) + 0.01*f(y)*f(x-y) + -0.03*f(y)*f(x) + -0.01*f(y)*f(y) + 1.34*f(x)*f(x+y) + 1.34*f(x)*f(x-y) + -2.66*f(x)*f(x) + 0.32*f(x-y)*f(x+y) + -0.17*f(x-y)*f(x-y) + -0.17*f(x+y)*f(x+y)  + -0.01
            # NOTE: milp property: f(x-y) - 2*f(x) + 2*f(y) + f(y)*f(x+y) + f(y)*f(x-y) - 2*f(y)*f(x) - f(y)*f(y) - f(x)*f(x+y) - f(x)*f(x-y) + 3*f(x)*f(x) - f(x-y)*f(x+y) + f(x+y) - 1 = 0 (0.0) (block: None)
            # NOTE: milp property: f(x-y) - 2*f(x) + 14*f(y) + 7*f(y)*f(x+y) + 7*f(y)*f(x-y) - 14*f(y)*f(x) - 7*f(y)*f(y) + f(x)*f(x+y) + f(x)*f(x-y) + 5*f(x)*f(x) - 5*f(x-y)*f(x+y) - f(x-y)*f(x-y) - f(x+y)*f(x+y) + f(x+y) - 7*1 = 0 (0.0) (block: None)
            # NOTE: DIG:           8*f(x)*f(x) - 16*f(x)*f(y) - 4*f(x) - f(x-y)^2 - 6*f(x-y)*f(x+y) + 8*f(x-y)*f(y) + 2*f(x-y) - f(x+y)*f(x+y) + 8*f(x+y)*f(y) + 2*f(x+y) - 8*f(y)*f(y) + 16*f(y) - 8 = 0;

            # def f(x):
            #     return x * x * x + 1

            # degree = 2
            # importantVarName = "f(y)*f(x+y)"
            # domain = Domain.Integer
            # BOUND = 8
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: milp property: 2*f(x+y) + 4*f(x-y) - 6*f(x) + 8*f(y) - f(y)*f(x-y) - 4*f(y)*f(y) - f(x)*f(x+y) - f(x)*f(x-y) + 4*f(x)*f(x) - 2*f(x-y)*f(x+y) + f(y)*f(x+y) - 4*1 = 0 (0.0) (block: None) (bound: 8)
            # NOTE: DIG          : 4*f(x)*f(x) - f(x)*f(x-y) - f(x)*f(x+y) - 6*f(x) - 2*f(x-y)*f(x+y) - f(x-y)*f(y) + 4*f(x-y) + f(x+y)*f(y) + 2*f(x+y) - 4*f(y)*f(y) + 8*f(y) - 4 = 0

            # def f(x):
            #     return x * x + x + 2

            # def g(x):
            #     # g(x+y) + g(x-y) = 2*g(x) + 2*g(y)
            #     # g(x) = 1/2 * g(x+y) + 1/2 * g(x-y) - g(y)
            #     return x * x

            # def h(x):
            #     # h(x+y) + h(x-y) = 2*h(x)
            #     # h(x) = 1/2 * h(x+y) + 1/2 * h(x-y))
            #     return x + 2

            # degree = 1
            # importantVarName = "f(x)"
            # domain = Domain.Integer
            # distribution = Distribution.Small
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), g(x), h(x), 1],
            #     [
            #         "f(x+y)",
            #         "f(x-y)",
            #         "f(x)",
            #         "f(y)",
            #         "(1/2*g(x+y) + 1/2*g(x-y) - g(y))",
            #         "(1/2*h(x+y) + 1/2*h(x-y))",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(x) = + 1.0*(1/2*g(x+y) + 1/2*g(x-y) - g(y)) + 1.0*(1/2*h(x+y) + 1/2*h(x-y))
            # NOTE: milp property: - (1/2*g(x+y) + 1/2*g(x-y) - g(y)) - (1/2*h(x+y) + 1/2*h(x-y)) + f(x) = 0 (0.0) (block: None) (bound: 2)

            # def f(x):
            #     return x**2 + sin(x)

            # def g(x):
            #     # g(x+y) + g(x-y) = 2*g(x) + 2*g(y)
            #     # g(x) = 1/2 * g(x+y) + 1/2 * g(x-y) - g(y)
            #     return x**2

            # def h(x):
            #     # h(x) = h(y)*h(y)/h(x) + h(x-y)*h(x+y)/h(x)
            #     return sin(x)

            # degree = 1
            # importantVarName = "f(x)"
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x), g(x), h(x), 1],
            #     [
            #         "f(x)",
            #         "(1/2*g(x+y) + 1/2*g(x-y) - g(y))",
            #         "(1/h(x)*(h(y)*h(y)) + 1/h(x)*(h(x-y)*h(x+y)))",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(x) = + 1.0*(1/2*g(x+y) + 1/2*g(x-y) - g(y)) + 1.0*(1/h(x)*(h(y)*h(y)) + 1/h(x)*(h(x-y)*h(x+y)))
            # NOTE: milp property: - (1/2*g(x+y) + 1/2*g(x-y) - g(y)) - (1/h(x)*(h(y)*h(y)) + 1/h(x)*(h(x-y)*h(x+y))) + f(x) = 0 (-1.2187473252822656e-13) (block: None) (bound: 2)

            # def f(x):
            #     return x * x - 5 * x + 6

            # degree = 2
            # importantVarName = "f(x+y)*f(x+y)"
            # domain = Domain.Integer
            # BOUND = 16
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x+y)*f(x+y) = + 1.91*f(x+y) + 1.91*f(x-y) + -3.81*f(x) + -0.19*f(y) + -0.02*f(y)*f(x+y) + -0.02*f(y)*f(x-y) + 0.03*f(y)*f(x) + 0.02*f(y)*f(y) + 8.02*f(x)*f(x+y) + 8.02*f(x)*f(x-y) + -16.05*f(x)*f(x) + 2.02*f(x-y)*f(x+y) + -1.0*f(x-y)*f(x-y)  + 0.57
            # NOTE: milp property:  - 2*f(x+y) - 2*f(x-y) + 4*f(x) - 8*f(x)*f(x+y) - 8*f(x)*f(x-y) + 16*f(x)*f(x) - 2*f(x-y)*f(x+y) + f(x-y)*f(x-y) + f(x+y)*f(x+y) = 0 (-9.325873406851315e-15) (block: None)
            # NOTE: DIG:         : NONE
            # https://chat.openai.com/share/7eea81f5-73cd-4d77-907e-ea66872a1447

            # c = 1

            # def f(x):
            #     return e ** (c * x)

            # degree = 2
            # importantVarName = "f(x+y)"
            # # importantVarName = "f(y)*f(x)"
            # block = "f(x-y)*f(x+y)"
            # # block = "f(y)*f(x-y)"
            # try:
            #     (terms, termNames) =  get_values_terms(
            #         degree,
            #         [f(x + y), f(x - y), f(x), f(y), 1],
            #         ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #         "1",
            #     )
            # except OverflowError as e:
            #     print(f"OverflowError: {e}; x: {x}; y: {y}")
            #     continue
            # NOTE: lin. property: f(x+y) = + 1.0*f(y)*f(x)
            # NOTE: milp property: - 2*f(x) + 2*f(y)*f(x-y) - f(y)*f(x) - 2*f(x)*f(x) + 2*f(x-y)*f(x+y) + f(x+y) = 0 (-1.6985323598035484e-09)
            # https://www6b3.wolframalpha.com/input?i=2*e%5Ex+-+2*e%5Ey*e%5E%28x-y%29+-+e%5Ey*e%5Ex+-+2*e%5Ex*e%5Ex+%2B+2*e%5E%28x-y%29*e%5E%28x%2By%29+%2B+e%5E%28x%2By%29+%3D+0&lang=en
            # NOTE: block = "f(y)*f(x-y)"
            # NOTE: milp property: - f(y)*f(x) - 2*f(x)*f(x) + 2*f(x-y)*f(x+y) + f(x+y) = 0 (-7.752691351847925e-12)
            # https://www.wolframalpha.com/input?i=-+e%5E%28y%29*e%5E%28x%29+-+2*e%5E%28x%29*e%5E%28x%29+%2B+2*e%5E%28x-y%29*e%5E%28x%2By%29+%2B+e%5E%28x%2By%29+%3D+0

            # def f(x):
            #     return x / (1 - x)

            # degree = 3
            # importantVarName = "f(x)"
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH:  f(x+y) - f(x+y)f(x)f(y) = f(x) + f(y) -2 f(x)f(y)
            # NOTE: LIN-REG: f(x) = + 1.0*f(x+y) + -1.0*f(y) + -2.0*f(y)*f(x) + -1.0*f(y)*f(x)*f(x+y)
            # NOTE: MILP OK: - f(x+y) + f(y) + 2 f(y)*f(x) + f(y)*f(x)*f(x+y) + f(x) = 0 (-3.4924596548080444e-10)

            # def f(x):
            #     return 1 / (1 - tan(x))

            # degree = 3
            # importantVarName = "f(x)"
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH: 2f(x)f(x+y) + 2f(y)f(x+y) - 2f(x)f(y)f(x+y) + f(x+y) = f(x) + f(y) - 1 (TODO)
            # NOTE: LIN-REG: f(x) = + -1.0*f(x+y) + -1.0*f(y) + 2.0*f(y)*f(x+y) + 2.0*f(x)*f(x+y) + -2.0*f(y)*f(x)*f(x+y)  + 1.0
            # NOTE: MILP OK: f(x+y) + f(y) - 2 f(y)*f(x+y) - 2 f(x)*f(x+y) + 2 f(y)*f(x)*f(x+y) + f(x) - 1 = 0 (-1.4904744105592727e-12)
            # NOTE: NO SCALE

            def f(x):
                return sin(x)

            def P(x, N=30):
                """sinTaylor"""
                sum = 0.0
                term = x

                for n in range(1, N + 1):
                    sum += term
                    term = -term * x * x / (2 * n * (2 * n + 1))

                return sum

            degree = 2
            # importantVarName = "f(y)*f(y)"
            importantVarName = "f(x)*f(x)"
            ERROR_BOUND = 0.1
            (terms, termNames) = get_values_terms(
                degree,
                [P(x + y), P(x - y), P(x), P(y), 1.0],
                ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
                "1",
            )
            # NOTE: lin. property: f(x)*f(x) = + 1.0*f(y)*f(y) + 1.0*f(x-y)*f(x+y)
            # NOTE: milp property:  - f(y)*f(y) - f(x-y)*f(x+y) + f(x)*f(x) = 0 (-2.230854390106174e-14) (block: None) (bound: 2)

            # def f(x):
            #     return sympy.sin(x)

            # degree = 2
            # # importantVarName = "f(y)*f(y)"
            # importantVarName = "f(x)*f(x)"
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + y), f(x - y), f(x), f(y), 1],
            #     ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],
            #     "1",
            # )
            # NOTE: TRUTH: f(x+y)*f(x-y) = f(x)*f(x) - f(y)*f(y)
            # NOTE: LIN-REG: f(x)*f(x) = + -0.38*f(x)*f(y) + 0.24*f(y)*f(y) + 0.67*f(x)*f(x) + 0.1*f(x-y)*f(x+y) + 0.12*f(x-y)*f(x-y) + 0.12*f(x+y)*f(x+y) + 0.47*f(x)*f(y)*f(x)*f(x)
            # NOTE: MILP OK: - 2 f(y)*f(y) + f(x)*f(x) - 2 f(x-y)*f(x+y) + f(x)*f(x) = 0 (-1.314888207538424e-13)

            # def f(x):
            #     return sin(x)

            # def g(x):
            #     return cos(x)

            # degree = 1
            # importantVarName = "g(x)*g(x)"
            # # importantVarName = "f(x)*f(x)"
            # domain = Domain.Real
            # distribution = False
            # BOUND = 1
            # # fmt: off
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [
            #         f(x) * f(x), g(x) * g(x), f(y) * f(y), g(y) * f(y),
            #         f(x + y), g(x + y), f(x - y), g(x - y), f(x), f(y), g(x), g(y), 1,
            #     ],
            #     [
            #         "f(x)*f(x)", "g(x)*g(x)", "f(y)*f(y)", "g(y)*g(y)",
            #         "f(x+y)", "g(x+y)", "f(x-y)", "g(x-y)", "f(x)", "f(y)", "g(x)", "g(y)", "1",
            #     ],
            #     "1",
            # )

            # fmt: on
            # NOTE: f(x)*f(x) = + -1.0*g(x)*g(x)  + 1.0
            # NOTE: g(x)*g(x) + f(x)*f(x) - 1 = 0 (-9.992007221626409e-16)

            # def f(x, y):
            #     return x * y

            # degree = 1
            # importantVarName = "f(x,y)"
            # domain = Domain.Integer
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + r, y + s), f(x, y), f(x, s), f(r, y), f(r, s), 1],
            #     ["f(x+r,y+s)", "f(x,y)", "f(x,s)", "f(r,y)", "f(r,s)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x,y) = + 1.0*f(x+r,y+s) + -1.0*f(x,s) + -1.0*f(r,y) + -1.0*f(r,s)
            # NOTE: milp property:  - f(x+r,y+s) + f(x,s) + f(r,y) + f(r,s) + f(x,y) = 0 (0.0) (block: None) (bound: 2)

            # degree = 1
            # importantVarName = "f(x,y)"
            # domain = Domain.Integer
            # BOUND = 4
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x + r, y + s), f(r, y + s), f(x + t, s), f(t, s), 1],
            #     [
            #         "f(x,y)",
            #         "f(x+r,y+s)",
            #         "f(r,y+s)",
            #         "f(x+t,s)",
            #         "f(t,s)",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(x,y) = + 1.0*f(x+r,y+s) + -1.0*f(r,y+s) + -1.0*f(x+t,s) + 1.0*f(t,s)
            # NOTE: milp property:  - f(x+r,y+s) + f(r,y+s) + f(x+t,s) - f(t,s) + f(x,y) = 0 (0.0) (block: None) (bound: 4)

            # def f(x, y):
            #     return x * y + x

            # degree = 2
            # importantVarName = "f(r,s)*f(x-r,y-s)"
            # domain = Domain.Integer
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x - r, y - s), f(x - r, s), f(r, y - s), f(r, s), 1],
            #     [
            #         "f(x,y)",
            #         "f(x-r,y-s)",
            #         "f(x-r,s)",
            #         "f(r,y-s)",
            #         "f(r,s)",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(r,s)*f(x-r,y-s) = + 1.0*f(r,y-s)*f(x-r,s)
            # NOTE: milp property:  - f(r,y-s)*f(x-r,s) + f(r,s)*f(x-r,y-s) = 0 (0.0) (block: None) (bound: 2)

            # degree = 2
            # importantVarName = "f(r,s)*f(x+r,y+s)"
            # domain = Domain.Integer
            # BOUND = 2
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x + r, y + s), f(x + r, s), f(r, y + s), f(r, s), 1],
            #     [
            #         "f(x,y)",
            #         "f(x+r,y+s)",
            #         "f(x+r,s)",
            #         "f(r,y+s)",
            #         "f(r,s)",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(r,s)*f(x+r,y+s) = + 1.0*f(r,y+s)*f(x+r,s)
            # NOTE: milp property:  - f(r,y+s)*f(x+r,s) + f(r,s)*f(x+r,y+s) = 0 (-6.661338147750939e-16) (block: None) (bound: 2)

            # def f(x, y):
            #     return x * y + x + y

            # degree = 2
            # importantVarName = "f(r,s)"
            # domain = Domain.Integer
            # BOUND = 1
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x + r, y + s), f(x + r, s), f(r, y + s), f(r, s), 1],
            #     [
            #         "f(x,y)",
            #         "f(x+r,y+s)",
            #         "f(x+r,s)",
            #         "f(r,y+s)",
            #         "f(r,s)",
            #         "1",
            #     ],
            #     "1",
            # )
            # NOTE: lin. property: f(r,s) = + -1.0*f(x+r,y+s) + 1.0*f(x+r,s) + 1.0*f(r,y+s) + -1.0*f(r,s)*f(x+r,y+s) + 1.0*f(r,y+s)*f(x+r,s)
            # NOTE: milp property: f(x+r,y+s) - f(x+r,s) - f(r,y+s) + f(r,s)*f(x+r,y+s) - f(r,y+s)*f(x+r,s) + f(r,s) = 0 (-3.9968028886505635e-15) (block: None) (bound: 2)

            # def f(x, y):
            #     return x + y

            # degree = 1
            # importantVarName = "f(x,y)"
            # domain = Domain.Integer
            # BOUND = 1
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x + r, y + s), f(x, y), f(x, s), f(r, y), f(r, s), 1],
            #     ["f(x+r,y+s)", "f(x,y)", "f(x,s)", "f(r,y)", "f(r,s)", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x,y) = + 0.67*f(x+r,y+s) + 0.33*f(x,s) + 0.33*f(r,y) + -1.0*f(r,s)
            # NOTE: milp property:  - f(x,s) - f(r,y) + f(r,s) + f(x,y) = 0 (0.0) (block: None) (bound: 1)
            # NOTE: milp property: f(x+r,y+s) - 2*f(x,s) - 2*f(r,y) + f(r,s) + f(x,y) = 0 (0.0) (block: None) (bound: 2)

            # def f(x, y):
            #     return x + y

            # degree = 1
            # importantVarName = "f(x, f(x, y))"
            # domain = Domain.Integer
            # BOUND = 1
            # # block = "f(f(x, y), f(x, y))"
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x, f(x, y)), f(f(x, y), y), f(f(x, y), f(x, y)), 1],
            #     ["f(x, y)", "f(x, f(x, y))", "f(f(x, y), y)", "f(f(x, y), f(x, y))", "1"],
            #     "1",
            # )
            # NOTE: lin. property: f(x, f(x, y)) = + 0.6*f(x, y) + -1.0*f(f(x, y), y) + 1.2*f(f(x, y), f(x, y))
            # NOTE: milp property:  - f(x, y) + f(f(x, y), y) - f(f(x, y), f(x, y)) + f(x, f(x, y)) = 0 (0.0) (block: None) (bound: 1)

            # def f(x, y):
            #     return x + y

            # degree = 1
            # importantVarName = "f(f(x, y), z)"
            # domain = Domain.Integer
            # BOUND = 1
            # block = "f(f(x, y), f(x, y))"
            # # fmt: off
            # (terms, termNames) =  get_values_terms(
            #     degree,
            #     [f(x, y), f(x, f(x, y)), f(f(x, y), y), f(f(x, y), f(x, y)), f(f(x, y), z), f(x, f(y, z)), 1, ],
            #     ["f(x, y)", "f(x, f(x, y))", "f(f(x, y), y)", "f(f(x, y), f(x, y))", "f(f(x, y), z)", "f(x, f(y, z))", "1", ],
            #     "1",
            # )
            # fmt: on
            # NOTE:lin. property: f(f(x, y), z) = + 1.0*f(x, f(y, z))
            # NOTE: milp property:  - f(x, f(y, z)) + f(f(x, y), z) = 0 (0.0) (block: f(f(x, y), f(x, y))) (bound: 1)

            # add the index of a term that results in a complex solution to the to_be_removed_from_model list
            # there is no complex valued terms in the model, check if there is any nan or inf
            # if so continue to select a new set of terms with fress random values.
            # no_complex = True
            # for i in range(len(terms)):
            #     if not terms[i].is_integer and not terms[i].is_real:
            #         to_be_removed_from_model.append(i)
            #         no_complex = False
            # if no_complex:
            #     if any(math.isnan(x) and math.isinf(x) for x in terms):
            #         continue

            # putting important term to the end
            important = termNames.index(importantVarName)
            terms = terms[:important] + terms[important + 1 :] + [terms[important]]
            termNames = (
                termNames[:important]
                + termNames[important + 1 :]
                + [termNames[important]]
            )

            # removing constant
            constant = termNames.index("1")
            terms = terms[:constant] + terms[constant + 1 :]
            termNames = termNames[:constant] + termNames[constant + 1 :]

            if k == N:
                k = len(terms) + 10

            k -= 1

            writer.writerow(terms)

    # print("")
    # print(terms)
    # print to_be_removed_from_model termNames and terms if any
    # if len(to_be_removed_from_model) > 0:
    #     print("to_be_removed_from_model:")
    #     for index in to_be_removed_from_model:
    #         print(f"{termNames[index]}: {terms[i]}")

    print(termNames)

    # Load the CSV file into a numpy array
    data = np.genfromtxt("data.csv", delimiter=",")

    # Split the data into X and y
    X = data[:, :-1]  # Select all columns except the last one
    y = data[:, -1]  # Select the last column

    features = []
    r_squared = []
    print("------------------------------------------")
    lr_prop = ""
    lr_expr = ""
    intercept_included = True
    n = 0
    for n in range(10):
        prev_X = X
        prev_termNames = termNames
        to_be_removed_from_model = []
        to_be_likely_removed_from_model = []
        try:
            # Create a linear regression model and fit it to the data
            model = LinearRegression(copy_X=True, fit_intercept=intercept_included).fit(
                X, y
            )
            # Print the coefficients of the regression line
            # print(f"Coefficients: {model.coef_}")
            # print(f"Intercept: {model.intercept_}")
            print(f"Features: {model.n_features_in_}")
            features.append(model.n_features_in_)

            print("------------------------------------------")
            max_len = max([len(x) for x in termNames])
            # print all the coefficients and their corresponding variables
            for i in range(len(model.coef_)):
                print(f"%{max_len}s = %2s" % (termNames[i], (round(model.coef_[i], 5))))
            # print the intercept
            if intercept_included:
                print(f"%{max_len}s = %2s" % ("1", model.intercept_))
            print("------------------------------------------")
            # print R^2 score
            print(f"R^2 score: {model.score(X, y)}")
            r_squared.append(model.score(X, y))

            # printing the solution
            lr_prop = importantVarName + " = "
            lr_expr = "-" + importantVarName + " "
            res = 0
            for i in range(len(model.coef_)):
                res += model.coef_[i] * terms[i]
                if abs(model.coef_[i]) > BOUND:
                    to_be_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.05 and len(termNames) < 10:
                    rounded = round(model.coef_[i], 2)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.4 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.01 and len(termNames) < 40:
                    rounded = round(model.coef_[i], 2)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.3 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.001:
                    rounded = round(model.coef_[i], 3)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.1 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                else:
                    to_be_removed_from_model.append(i)

            if intercept_included and abs(round(model.intercept_, 2)) > 0.01:
                lr_prop += " + " + str(round(model.intercept_, 2))
                lr_expr += " + " + str(round(model.intercept_, 2))
                intercept_included = False

            print("------------------------------------------")
            print(lr_prop)
            print(f"error: {res}")

        except ValueError as e:
            print(f"ValueError: {e}")
        if (
            len(to_be_removed_from_model) == 0
            and len(to_be_likely_removed_from_model) == 0
        ):
            print("------------------------------------------")
            print("no more terms to remove!!!")
            break
        else:
            X = np.delete(
                X, to_be_removed_from_model + to_be_likely_removed_from_model, 1
            )
            termNames = np.delete(
                termNames, to_be_removed_from_model + to_be_likely_removed_from_model
            )

        # if n > 0 and r_squared[n] < r_squared[n - 1]:
        #     print("r_square decreased!")
        #     break

    # print("------------------------------------------")
    # proved = verify(canonicalize(lr_expr), f, g, h)
    # print("------------------------------------------")
    # functions = [f, g, h, u, v, w]
    # passed = property_test(
    #     lr_expr,
    #     *functions,
    #     domain=domain,
    #     distribution=distribution,
    #     epsilon=1e-13,
    #     n=30,
    # )

    # exit()
    #######################################
    print("------------------------------------------")

    # X = data
    # append the y values to the X matrix
    X = np.append(X, np.array([y]).T, axis=1)

    # traverse the data columnwise. If the average is less than 1e-6, set SCALE to 1e5.
    # If the average is greater than 1e6, set SCALE to 1e-5.
    SCALE = 1  # scaling factor for a pulse value
    for i in range(len(X[0])):
        avg = 0
        for j in range(len(X)):
            avg += X[j][i]
        avg /= len(X)
        if avg < 1e-7:
            SCALE = 1e5
        if avg > 1e7:
            SCALE = 1e-5

    print(f"SCALE: {SCALE:e}")

    # find the minimum and maximum values of X
    minX = 0
    maxX = 0
    for i in range(len(X)):
        for j in range(len(X[i])):
            if X[i][j] < minX:
                minX = X[i][j]
            if X[i][j] > maxX:
                maxX = X[i][j]

    INTEGRALITY_FOCUS = 1
    # MIPFOCUS = 2
    NUMERIC_FOCUS = 3
    # OPTIMALITY_TOL = 1e-9
    # SOS1 = False
    # ERROR_BOUND = 0.1  # 0.05
    ROUND = None
    SCALE = 1

    m = gp.Model("synthesis of random self-reducible properties")
    m.setParam("TimeLimit", 3)
    m.setParam("IntegralityFocus", INTEGRALITY_FOCUS)
    # m.setParam("MIPFocus", MIPFOCUS)
    # m.setParam("OptimalityTol", OPTIMALITY_TOL)
    m.setParam("NumericFocus", NUMERIC_FOCUS)

    # For each term, create an integer decision variable and
    for i in range(len(termNames)):
        m.addVar(vtype=GRB.INTEGER, name=f"term_{i}", lb=-BOUND, ub=BOUND)
        m.update()
        if termNames[i] == importantVarName:  # e.g. "f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 1, name=f"term_{i}_ub")
            # m.getVarByName(f"term_{i}").setAttr("BranchPriority", 1000)
        if block is not None and termNames[i] == block:  # e.g. "f(x-y)*f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 0, name=f"term_{i}_ub")

    # NOTE: add the last constant as a term
    m.addVar(vtype=GRB.INTEGER, name=f"term_{len(termNames)}", lb=-BOUND, ub=BOUND)
    m.update()

    # m.addConstr(gp.quicksum(m.getVars()) >= -20, name="sum_terms")
    # m.addConstr(gp.quicksum(m.getVars()) <= -15, name="sum_terms")

    abs_vars_name = {}
    abs_vars_expr = {}
    for i in range(len(X)):
        # create a continous error variable.
        var_error = m.addVar(
            vtype=GRB.CONTINUOUS, name=f"error_{i}", lb=-ERROR_BOUND, ub=ERROR_BOUND
        )
        abs_vars_name[f"error_{i}"] = var_error
        vals = []
        for j in range(len(X[i])):
            # TODO: round the value of X[i][j] to ? decimal places
            if ROUND is None:
                vals.append(X[i][j] * SCALE * m.getVarByName(f"term_{j}"))
            else:
                vals.append(round(X[i][j], ROUND) * SCALE * m.getVarByName(f"term_{j}"))
            # vals.append(X[i][j] * m.getVarByName(f"term_{j}"))

        # add the last constant as a term
        vals.append(m.getVarByName(f"term_{len(termNames)}"))

        # create an expression for the sum of the datapoint times the decision variable.
        sum_terms = gp.quicksum(vals)
        abs_vars_expr[f"error_{i}"] = sum_terms
        m.addConstr(sum_terms == var_error, name=f"error_{i}_ub")
        # m.addConstr(sum_terms <= ERROR_BOUND, name=f"error_{i}_ub")
        # m.addConstr(sum_terms >= -ERROR_BOUND, name=f"error_{i}_lb")

    # convexify the absolute value function in the objective function
    # NOTE: set objective function
    for name in abs_vars_name.keys():
        var = abs_vars_name[name]
        lr_expr = abs_vars_expr[name]
        # m.addConstr(expr <= var, name=f"sum_{name}_ub")
        # m.addConstr(-expr <= var, name=f"sum_{name}_lb")

    # TODO:
    # m.addConstr(gp.quicksum(abs_vars_name.values()) <= 1e4, name="obj_ub")

    m.setObjective(gp.quicksum(abs_vars_name.values()), GRB.MINIMIZE)

    m.write("synthesis.lp")

    try:
        print("------------------------------------------")
        m.optimize()
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))

    print("------------------------------------------")
    ordered_gates = {}
    if m.Status == GRB.OPTIMAL:
        print("Optimal objective: %g" % m.ObjVal)
    elif m.Status == GRB.INF_OR_UNBD:
        print("Model is infeasible or unbounded")
        exit(0)
    elif m.Status == GRB.INFEASIBLE:
        print("Model is infeasible")
        print("------------------------------------------")
        print(
            f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
        )
        print("------------------------------------------")
        print(f"scale: {SCALE:e}")
        print("------------------------------------------")
        exit(0)
    elif m.Status == GRB.UNBOUNDED:
        print("Model is unbounded")
        exit(0)
    else:
        print("Optimization ended with status %d" % m.Status)
        print("------------------------------------------")
        print(
            f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
        )
        print("------------------------------------------")
        exit(0)

    milp_expr = ""
    first_term = True

    # NOTE: add the last constant as a term
    termNames = np.append(termNames, "1")

    for var in m.getVars():
        # if v.X != 0:
        #     print('%s %g' % (v.VarName, v.X))
        if var.VarName.startswith("term_"):  # NOTE
            # find the length of the longest term in termNames
            max_len = max([len(x) for x in termNames])
            print(
                f"%8s | %{max_len}s = %2s"
                % (var.VarName, termNames[int(var.VarName[5:])], pp(var.X))
            )
            if var.X != 0:
                coeff = ""
                if var.X > 0 and not first_term:
                    coeff = " + "
                if var.X > 0 and first_term:
                    coeff = ""
                if var.X < 0:
                    coeff = " - "
                if var.X != 1 and var.X != -1:
                    coeff += f"{pp(abs(var.X))}*"
                milp_expr += f"{coeff}{termNames[int(var.VarName[5:])]}"
                first_term = False

    # for v in m.getVars():
    #     if v.VarName.startswith("error_"):  # NOTE
    #         print('%s %g' % (v.VarName, v.X))

    milp_expr = milp_expr.strip()
    print("------------------------------------------")
    print(f"Time: {round(m.runTime, 2)}s")
    print("Optimal objective: %g" % m.ObjVal)
    print("------------------------------------------", end=" ")
    m.printStats()
    print("------------------------------------------", end=" ")
    m.printQuality()
    print("------------------------------------------")
    print(
        f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
    )
    print("------------------------------------------")
    print(
        f"MILP property: {milp_expr} = 0 ({m.ObjVal}) (block: {block}) (bound: {BOUND})"
    )
    print("------------------------------------------")
    print(f"scale: {SCALE:e}")

    print("------------------------------------------")
    proved = verify(milp_expr, f, g, h)
    print("------------------------------------------")
    functions = [f, g, h, u, v, w]
    passed = property_test(
        milp_expr,
        *functions,
        domain=domain,
        distribution=distribution,
        epsilon=0.1,
        n=30,
    )
    print("------------------------------------------")
    print(f"{canonicalize(milp_expr)} = 0")
    print("------------------------------------------")
    # print the elapsed time
    print(f"Time: {round(m.runTime, 2)}s")
    print("------------------------------------------")
