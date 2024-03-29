from sympy import sympify, Symbol, Expr, simplify

# Example expression in string format
expr_str = "- f(x) + 3*f(x)*f(y)*f(x+y) + 2*f(x)*f(y) + 4*f(x+y) + 6*f(y)**2 + 7"
# expr_str = "2*Y*x + 2*Y - v - 2*x*y - x + 2*y + 1"
# Convert the string to a SymPy expression
expr: Expr = sympify(expr_str)

print(expr.args)

mapping = {}
for e in expr.args:
    if e.is_Mul:
        for arg in e.args:
            if arg.is_Pow:
                mapping[arg.base] = Symbol(str(arg.base))
            elif not arg.is_number:
                mapping[arg] = Symbol(str(arg).replace(" ", ""))
    else:
        if not e.is_number:
            mapping[e] = Symbol(str(e))

print(mapping)
print(expr)
expr = expr.subs(mapping)

print(simplify(expr))
print(expr.free_symbols)
