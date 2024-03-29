from sympy import preorder_traversal, Rational, symbols, nsimplify


def evaluate_rationals_tree(expr):
    # Function to evaluate rational numbers within the expression tree
    def eval_rationals(node):
        if isinstance(node, Rational):
            # Convert to float, then to integer if the decimal part is zero
            float_val = float(node)
            return int(float_val) if float_val.is_integer() else float_val
        return node

    # Traverse and replace rational numbers in the expression tree
    evaluated_expr = expr
    for sub_expr in preorder_traversal(expr):
        if isinstance(sub_expr, Rational):
            evaluated_expr = evaluated_expr.subs(sub_expr, eval_rationals(sub_expr))
    return evaluated_expr


# Example usage


# Example usage
x, y = symbols("x y")

expr = x * 2.0 + y * 3.21 + 0.58
print(expr)

expr = nsimplify(expr)
print(expr)

expr_tree_evaluated = evaluate_rationals_tree(expr)
print(expr_tree_evaluated)
