import sympy as sp


# Function to round the coefficients of an expression
def round_coefficients(expr, decimals):
    return expr.xreplace({n: round(n, decimals) for n in expr.atoms(sp.Number)})


# Define the variables
x, y, v, u, a, b = sp.symbols("x y v u a b")
# Define the expression
expr = 3.141592653589793 * x + 2.718281828459045 * y

# Round the coefficients to 2 decimal places
rounded_expr = round_coefficients(expr, 2)

print("Original expression:", expr)
print("Rounded expression:", rounded_expr)

expr = -2 * a * b + x * u + 1.0000000216107 * y * v - 5.10995751042976e-5

print("Original expression:", expr)
print("Rounded expression:", round_coefficients(expr, 2))
