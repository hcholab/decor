from sympy import Expr, Function, simplify, sympify


def make_set(x: Expr) -> set[Expr]:
    return {x}


def find_set(x: Expr, sets: list[set[Expr]]) -> set[Expr]:
    for s in sets:
        if x in s:
            return s
    return None


def union_sets(s1: set, s2: set) -> set:
    return s1.union(s2)


def create_equivalence_classes(expressions: list[Expr]) -> list[set[Expr]]:
    sets = [make_set(x) for x in expressions]
    for i in range(len(expressions)):
        for j in range(i + 1, len(expressions)):
            if simplify(expressions[i] - expressions[j]) == 0:
                s1 = find_set(expressions[i], sets)
                s2 = find_set(expressions[j], sets)
                if s1 != s2:
                    sets.remove(s1)
                    sets.remove(s2)
                    sets.append(union_sets(s1, s2))
    return sets


def get_smallest_properties(classes: list[set[Expr]]) -> set[Expr]:
    """Get the smallest expression in a set of expressions"""
    sets: set[Expr] = set()
    for cls in classes:
        smallest: Expr = None
        for e in cls:
            e = sympify(e)
            if smallest is None or e.count_ops() < smallest.count_ops():
                smallest = e
        sets.add(smallest)
    return sets


def check_sets_equal(list1: list[set[Expr]], list2: list[set[Expr]]) -> bool:
    """Check if two lists of sets are equal"""
    if len(list1) != len(list2):
        return False
    for set1 in list1:
        found_match = False
        for set2 in list2:
            if set1 == set2:
                found_match = True
                break
        if not found_match:
            return False
    return True


def test_create_equivalence_classes():
    x = Symbol("x", real=True)
    f = Function("f")

    properties = [
        (f(x) ** 3 + f(x) ** 2 - f(x) - 1) / (f(x) ** 2 + 2 * f(x) + 1),
        f(x) - 1,
        (f(x) + 1) * (f(x) - 2) - (f(x) - 1) * f(x),
        -2,
        f(x) + 3,
    ]
    for e in properties:
        print(f"{sympify(e).count_ops()} -- {e}")

    expected = [
        {(f(x) ** 3 + f(x) ** 2 - f(x) - 1) / (f(x) ** 2 + 2 * f(x) + 1), (f(x) - 1)},
        {(f(x) + 1) * (f(x) - 2) - (f(x) - 1) * f(x), -2},
        {f(x) + 3},
    ]
    eq_classes = create_equivalence_classes(properties)
    print(eq_classes)
    assert check_sets_equal(eq_classes, expected)
    smallest = {-2, f(x) + 3, f(x) - 1}
    found = get_smallest_properties(eq_classes)
    print(f"smallest: {smallest}")
    print(f"found   : {found}")
    assert smallest == found

    properties = [
        f(x) ** 2 - 1,
        (f(x) - 1) * (f(x) + 1),
        f(x) ** 2 - 4,
        f(x) ** 2 - 2 * f(x) + 1,
    ]
    expected = [
        {f(x) ** 2 - 2 * f(x) + 1},
        {f(x) ** 2 - 1, (f(x) - 1) * (f(x) + 1)},
        {f(x) ** 2 - 4},
    ]
    smallest = {f(x) ** 2 - 1, f(x) ** 2 - 4, f(x) ** 2 - 2 * f(x) + 1}
    eq_classes = create_equivalence_classes(properties)
    assert check_sets_equal(eq_classes, expected)
    found = get_smallest_properties(eq_classes)
    print(f"smallest: {smallest}")
    print(f"found   : {found}")
    assert smallest == found


if __name__ == "__main__":  # noqa E123
    from sympy import Symbol

    test_create_equivalence_classes()
