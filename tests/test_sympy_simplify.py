# from sympy import sin, cos, simplify
# from sympy.abc import x
# from sympy import symbols, Function
from sympy import Function, Abs, sqrt, sin, cos, simplify, symbols, sqrt, tan, cot


if __name__ == "__main__":
    # e = sin(x) ** 2 + cos(x) ** 2

    # print(simplify(e))

    x0, x1, c = symbols("x0 x1 c")
    f = Function("f")

    # print(type(f(x + y)))

    # e = f(x)

    # print(simplify(e))

    # e = f(x - y) - 2 * f(x) - 2 * f(y) + f(x + y)
    # print(simplify(e))

    expr = (
        4 * c**2
        + 4 * x0**2
        # + x0
        - sqrt(c**2)
        + 4 * sqrt(x0**2)
        # - f(x0, c)
        # + 2 * sin(c * x0)
        # + cos(x0)
        + Abs(c)
        # - 4 * Abs(c**2)
        - 4 * Abs(x0)
        - 4 * Abs(x0**2)
        # + 1
    )

    exp = (
        -x0
        + 3 * sqrt(c**2)
        + 3 * sqrt(x0**2)
        + f(x0, c)
        - 2 * sin(c * x0)
        - cos(x0)
        - 3 * Abs(c)
        - 3 * Abs(x0)
        - 1
    )

    print(simplify(expr))

    exit()

    def f(x):
        return x**2

    expr = "f(x - y) - 2 * f(x) - 2 * f(y) + f(x + y)"

    def f(x):
        return tan(x)

    expr = "- f(x+y) + f(y) + f(y)*f(x)*f(x+y) + f(x)"

    print(
        eval(
            f"simplify({expr})",
            {
                "f": f,
                "x": symbols("x"),
                "y": symbols("y"),
                "sin": sin,
                "cos": cos,
                "tan": tan,
                "cot": cot,
                "simplify": simplify,
            },
        )
    )
