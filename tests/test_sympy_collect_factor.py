from sympy import (  # noqa F401
    symbols,
    Function,
    init_printing,
    collect,
    factor,
    sympify,
    simplify,
    apart,
)

x, y, z = symbols("x y z")
f = Function("f")
init_printing(use_unicode=True)

expr = sympify(
    "2*f(x)*f(y)*f(x - y) - f(x)*f(y) - f(x)*f(x - y) + f(x) - f(y)*f(x - y)"
)
print(expr)

print(expr.collect(f(x) * f(y) * f(x - y)))
print(expr.collect(f(x)))
print(expr.collect(f(x - y)))
# print(simplify(expr))
# print(factor(expr))
# print(collect(expr, f(x)))
