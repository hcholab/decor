import math


def cot(x):
    return 1 / math.tan(x)


# FUNCTIONS


def simple(x):
    return 2 * x + 4


def tanFunc(x):
    return math.tan(x)


def cotFunc(x):
    return cot(x)


def tanhFunc(x):
    return math.tanh(x)


def overEasyFunc(x):
    return 10 / (x)


def cotOverFunc(x):
    return 1 + cot(x)


def tanOverFunc(x):
    return 1 + math.tan(x)


def overFunc(x):
    return 10 * x / (1 - 10 * x)


def minusOverFunc(x):
    return -10 * x / (1 - 10 * x)


def linearFunc(x):
    return 10 * x + 7


def cosSimpleFunc(x):
    return math.cos(x)


def coshSimpleFunc(x):
    return math.cosh(x)


def squareFunc(x):
    return x * x


def multFunc(x):
    return x


def constFunc(x):  # noqa: U100
    return 17


def sinSimpleFunc(x):
    return math.sin(x)


def sinhSimpleFunc(x):
    return math.sinh(x)


def sinTaylor(x, terms=80):
    # f(x+y) = (f(x)^2 - f(y)^2)/(f(x-y))
    result = 0.0

    for n in range(terms):
        # print(n)
        numerator = (-1) ** n
        denominator = 1

        for i in range(1, 2 * n + 2):
            denominator *= i

        term = numerator * (x ** (2 * n + 1)) / denominator
        result += term
        # print(f"The {n}-th term is {numerator}*x^[{2*n+1}]/{denominator} and the value is {term}. The result so far is {result}")

    return result


functions = [
    tanFunc,
    cotFunc,
    tanhFunc,
    overEasyFunc,
    cotOverFunc,
    tanOverFunc,
    overFunc,
    minusOverFunc,
    linearFunc,
    cosSimpleFunc,
    coshSimpleFunc,
    squareFunc,
    multFunc,
    constFunc,
    sinSimpleFunc,
    sinhSimpleFunc,
    sinTaylor,
]
