from inspect import signature
from sympy import symbols, Function, tan, sin, cos, cot, simplify, lambdify
import random
import numpy as np

x = symbols("x")
y = symbols("y")
z = symbols("z")
r = symbols("r")
s = symbols("s")
f = Function("f")
g = Function("g")


def f(x, y):
    return x + y


expr = "- f(x, f(y, z)) + f(f(x, y), z)"

print("------------------------------------------")
# proof by simplification
proved = eval(
    f"simplify({expr})",
    {
        "f": f,
        "x": symbols("x"),
        "y": symbols("y"),
        "z": symbols("z"),
        "r": symbols("r"),
        "s": symbols("s"),
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "cot": cot,
        "simplify": simplify,
    },
)
print(f"proof: {proved == 0}")

if len(signature(f).parameters) == 1:
    f = lambdify(x, f(x))
else:
    f = lambdify([x, y], f(x, y))
# dynamic checking

DOMAIN = "D"
SMALL_DOMAIN = True
print("------------------------------------------")
errors = []
print("Generating 30 random points...")
n = 30
print(f"evaluating: {expr}")
for i in range(n):
    if DOMAIN == "R":
        if SMALL_DOMAIN:
            x = random.random() * 10 - 5
            y = random.random() * 10 - 5
            z = random.random() * 10 - 5
            r = random.random() * 10 - 5
            s = random.random() * 10 - 5
        else:
            # standard range
            x = random.random() * 1000 - 500
            y = random.random() * 1000 - 500
            z = random.random() * 1000 - 500
            r = random.random() * 1000 - 500
            s = random.random() * 1000 - 500
    else:
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        z = random.randint(-1000, 1000)
        r = random.randint(-1000, 1000)
        s = random.randint(-1000, 1000)

    errors.append(
        eval(
            expr,
            {
                "x": x,
                "y": y,
                "z": z,
                "r": r,
                "s": s,
                "f": f,
                "g": g,
                "sin": sin,
                "cos": cos,
                "tan": tan,
            },
        )
    )
    # print(f"error: {errors[-1]}, x: {x}, y: {y}")


print(f"mean error: {np.mean(errors)}")
print("------------------------------------------")
