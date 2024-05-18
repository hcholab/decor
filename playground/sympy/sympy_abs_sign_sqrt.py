from sympy import Abs, Symbol, sqrt, sign

# x = Symbol("x", positive=True)
x = Symbol("x", real=True)

expr = sqrt(x**2)
print(expr)


expr = x**2 - Abs(x**2)
print(expr)


expr = 1 - sign(x**2)
print(expr)
