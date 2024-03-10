from sympy import symbols, Function, Symbol, sin, cos, tan, sqrt


def generate_terms(functions, depth, base_terms=[Symbol("x")]):
    """
    Generate all possible terms from a set of functions based on a given depth.

    :param functions: List of function symbols.
    :param depth: Depth of nesting.
    :param base_terms: List of terms to start with.
    :return: List of generated terms.
    """
    if depth == 0:
        return base_terms

    previous_terms = generate_terms(functions, depth - 1, base_terms)
    new_terms = []

    for func in functions:
        for term in previous_terms:
            new_terms.append(func(term))

    return new_terms


if __name__ == "__main__":
    # Example usage:
    x, y = symbols("x y")
    functions = [sin, cos, tan]
    base_terms = [x, y, x * y, x**2, y**2, sqrt(x), sqrt(y)]
    depth = 1
    print(generate_terms(functions, depth, base_terms))

    print("--------------------------------------------------")

    x, y = symbols("x y")
    f = Function("f")
    g = Function("g")
    h = Function("h")
    functions = [f, g, h, sqrt]
    base_terms = [x, y]
    depth = 2
    print(generate_terms(functions, depth, base_terms))
