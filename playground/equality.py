from sympy import symbols, Function, simplify, sympify

# Define the symbols and function
x, y = symbols("x y", real=True)
f = Function("f")(x)

# Define the two expressions
expr1 = sympify("f(x)**2 - f(y)**2")
expr2 = sympify("(f(x) + f(y)) * (f(x) - f(y))")

# Simplify the expressions
simplified_expr1 = simplify(expr1)
simplified_expr2 = simplify(expr2)

print(str(simplified_expr1))
print(str(simplified_expr2))
# Check if the two expressions are equal
assert str(simplified_expr1) == str(simplified_expr2)
