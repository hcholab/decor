import re
import pprint
from z3 import Int, Real


# Helper functions for Z3py translation
def translate_var(var):
    if "int" in var or "signed" in var or "unsigned" in var:
        return Int(var.split(" ")[1].strip())
    elif "float" in var:
        return Real(var.split(" ")[1].strip())
    else:
        return None


def translate_guard(guard):
    guard = guard.replace("!", "Not")
    guard = guard.replace("&&", "And")
    guard = guard.replace("||", "Or")
    guard = guard.replace(">=", ">= ")
    guard = guard.replace("<=", "<= ")
    guard = guard.replace("==", "== ")
    guard = guard.replace("!=", "!= ")
    return guard


def translate_formula(formula):
    formula = formula.replace("?", "If")
    formula = formula.replace(":", ",")
    return formula


def parse_line(line):
    line = line.strip()
    match = re.match(r"^\((\d+)\)\s*(.*)\s*$", line)
    if match:
        number = int(match.group(1))
        content = match.group(2)
        return number, content
    return None, None


def parse_assignment(content):
    match = re.match(r"^(.*)\s*==\s*(.*)$", content)
    if match:
        var = match.group(1).strip()
        expr = match.group(2).strip()
        return var, expr
    return None, None


def parse_guard(content):
    match = re.match(r"^\\guard#(\d+)\s*==\s*(.*)$", content)
    if match:
        guard_num = int(match.group(1))
        guard_expr = match.group(2).strip()
        return guard_num, guard_expr
    return None, None


def parse_sliced(content):
    match = re.match(r"^\(sliced\)\s*(.*)\s*==\s*(.*)$", content)
    if match:
        var = match.group(1).strip()
        expr = match.group(2).strip()
        return var, expr
    return None, None


# Main parsing function
def parse_ir(ir_lines):
    result = {}
    non_deterministic_vars = {}
    assertions = []
    variables = {}
    substitutions = {}
    sliced = {}

    for line in ir_lines:
        number, content = parse_line(line)
        if number is None:
            # Handle sliced lines separately
            if "(sliced)" in line:
                var, expr = parse_sliced(line)
                sliced[var] = expr
            continue

        if "nondet_symbol" in content:
            var, expr = parse_assignment(content)
            non_deterministic_vars[var] = expr

        elif "guard" in content:
            guard_num, guard_expr = parse_guard(content)
            variables[f"guard{guard_num}"] = guard_expr

        elif "ASSERT" in content:
            assertions.append(content)

        elif "==" in content:
            var, expr = parse_assignment(content)
            result[var] = expr

    # Perform substitutions
    for var, expr in result.items():
        while any(ref_var in expr for ref_var in result.keys()):
            for ref_var, ref_expr in result.items():
                expr = expr.replace(ref_var, f"({ref_expr})")
        substitutions[var] = expr

    z3_vars = {k: translate_var(v) for k, v in non_deterministic_vars.items()}

    # Translating the parsed content into Z3py format
    z3py_output = {}
    for var, expr in substitutions.items():
        if "guard" in expr:
            guard_expr = translate_guard(expr)
            z3py_output[var] = f"{var} == {guard_expr}"
        else:
            z3py_output[var] = f"{var} == {expr}"

    # Adding sliced variables
    for var, expr in sliced.items():
        while any(ref_var in expr for ref_var in result.keys()):
            for ref_var, ref_expr in result.items():
                expr = expr.replace(ref_var, f"({ref_expr})")
        z3py_output[var] = f"{var} == {expr}"

    # Adding assertions
    for assertion in assertions:
        assertion_expr = translate_formula(assertion)
        z3py_output["ASSERT"] = assertion_expr

    return z3py_output


# Example IR
ir_example = """
(10) x!0@1#2 == nondet_symbol<signed int>(symex::nondet0)
(11) y!0@1#2 == nondet_symbol<signed int>(symex::nondet1)
(12) x!0@1#1 == x!0@1#2
(13) y!0@1#1 == y!0@1#2
(14) \\guard#1 == x!0@1#1 >= 1
(15) res!0@1#2 == x!0@1#1 + y!0@1#1 * 3
     guard: \\guard#1
(16) res!0@1#3 == x!0@1#1 + y!0@1#1 * 4
     guard: !\\guard#1
(17) res!0@1#4 == (\\guard#1 ? res!0@1#2 : res!0@1#3)
(18) ASSERT(x!0@1#1 >= 1 ? x!0@1#1 + y!0@1#1 * 3 == res!0@1#4 : x!0@1#1 + y!0@1#1 * 4 == res!0@1#4)
(sliced) candidate!0#1 == res!0@1#4
(sliced) return'!0#1 == candidate!0#1
"""

ir_lines = ir_example.strip().split("\n")
parsed_result = parse_ir(ir_lines)

pprint.pprint(parsed_result)
