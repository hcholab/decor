from sympy import symbols, Function, Eq, sqrt

# Define symbolic variables
x, y = symbols("x y")
f = Function("f")

# Define the equation
equation = Eq(f(x + y), f(x) * f(y) + sqrt(f(x) ** 2 - 1) * sqrt(f(y) ** 2 - 1))

# Square both sides
squared_equation = Eq(equation.lhs**2, equation.rhs**2)

print(squared_equation)
