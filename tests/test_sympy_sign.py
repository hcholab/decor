import sympy

expr = (
    "-2*f(x)**2 + f(x)*f(y) + 2*f(x) - 2*f(y)*f(x - y) + 2*f(x - y)*f(x + y) - f(x + y)"
)


expr = "-f(x) ** 2 + 2 * f(x) * f(y) + f(x - y) * f(x + y) - 2 * f(x + y)"

expr = sympy.sympify(expr)
print(expr)

# Extract the first term
first_term = expr.as_ordered_terms()[0]

print(f"first term: {first_term}")

sign_of_first_term = first_term.as_coeff_Mul()[0]

print(f"coefficient: {sign_of_first_term}")

print(f"sign: {sympy.sign(sign_of_first_term)}")

print(f"expr: {expr}")

if sympy.sign(sign_of_first_term) == -1:
    expr = -1 * expr

print(f"expr: {expr}")
