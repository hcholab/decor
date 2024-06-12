from lark import Lark, Transformer

# Define the grammar for parsing the IR
grammar = """
    start: statement+

    statement: nondet
             | assignment
             | guard
             | assertion

    nondet: var "==" "nondet_symbol" type "(" symex ")"
    assignment: "(" NUMBER ")" var "==" expr
    guard: "(" NUMBER ")" guard_var "==" logic_expr
    assertion: "(" NUMBER ")" "ASSERT(" logic_expr ")"

    var: CNAME "!" NUMBER "@" NUMBER "#" NUMBER
    guard_var: CNAME "#" NUMBER

    expr: var
        | INT
        | FLOAT
        | ESCAPED_STRING
        | var "+" expr
        | var "*" expr

    logic_expr: var "==" expr
              | var "!=" expr
              | var ">=" expr
              | var "<=" expr
              | var "<" expr
              | var ">" expr
              | logic_expr "&&" logic_expr
              | logic_expr "||" logic_expr
              | "!" logic_expr
              | "(" logic_expr ")"

    type: "<" ("signed int" | "float" | "unsigned int") ">"
    symex: "symex::" CNAME

    %import common.CNAME
    %import common.INT
    %import common.FLOAT
    %import common.ESCAPED_STRING
    %import common.WS
    %import common.DIGIT

    NUMBER: DIGIT+
    LESSTHAN: "<"
    GREATERTHAN: ">"

    %ignore WS
"""

parser = Lark(grammar, start="start", parser="lalr", lexer="contextual")


# Define the transformer to convert parsed data into Z3py format
class Z3Transformer(Transformer):
    def __init__(self):
        self.assignments = []
        self.guards = []
        self.assertions = []
        self.nondet_vars = {}

    def start(self, items):
        return {
            "assignments": self.assignments,
            "guards": self.guards,
            "assertions": self.assertions,
            "nondet_vars": self.nondet_vars,
        }

    def assignment(self, items):
        self.assignments.append(("assignment", items[0], items[1], items[2]))

    def guard(self, items):
        self.guards.append(("guard", items[0], items[1], items[2]))

    def assertion(self, items):
        self.assertions.append(("assertion", items[0], items[1]))

    def nondet(self, items):
        self.nondet_vars[items[0]] = (items[1], items[2])

    def var(self, items):
        return str(items[0])

    def guard_var(self, items):
        return str(items[0])

    def expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return f"({items[0]} {items[1]} {items[2]})"

    def logic_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return f"({items[0]} {items[1]} {items[2]})"
        elif len(items) == 2:
            return f"!{items[1]}"
        elif len(items) == 5:
            return f"({items[1]} {items[2]} {items[3]})"

    def type(self, items):
        return str(items[0])

    def symex(self, items):
        return str(items[0])


if __name__ == "__main__":
    # Example IR input
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
    # Parse and transform the IR example
    tree = parser.parse(ir_example)
    z3_transformed = Z3Transformer().transform(tree)

    # Output the transformed data
    print(z3_transformed)
