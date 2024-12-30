import numpy as np
from bitween.reporter import print_methods
from sympy import Function, symbols
from sympy import exp, Abs, sqrt, sin, cos, tan, log, sign  # noqa F401
from bitween.synthesizer import MILP, generate
from bitween.sampler import Distribution, Domain

# ------------------------------------------

x = symbols("x")
f = Function("f")


def encode(input_string):
    count = 1
    prev = ""
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst


# wrapper function to get input as 5 numbers and return encoded string
def encode_wrapper(a, b, c, d, e):
    return encode(str(a) + str(b) + str(c) + str(d) + str(e))


def decode(lst):
    q = ""
    for character, count in lst:
        q += character * count
    return q


print(f"{encode_wrapper(1, 2, 3, 4, 5)}")
print(f"{decode(encode_wrapper(1, 2, 3, 4, 5))}")


methods = generate(
    Domain.Real,
    Distribution(np.random.uniform, low=-5, high=5),
    [MILP(k=2, timeout=5, max_bound=2, obj=1e-12)],  # methods
    ["F(x+y)", "F(x-y)", "F(x)", "F(y)", "1"],  # how to call functions
    ["f(x+y)", "f(x-y)", "f(x)", "f(y)", "1"],  # function basis aka the template
    f,
    max_degree=2,
    n=30,
    epsilon=1e-13,
)

print("------------------------------------------")
print_methods(methods, f)
print("------------------------------------------")
