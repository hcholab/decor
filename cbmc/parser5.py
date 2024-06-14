import re
from collections import defaultdict


class ExpressionInfo:
    def __init__(self, expr, line_num, order, variable, function="main"):
        self.expr = expr
        self.line_num = line_num
        self.order = order
        self.variable = variable
        self.function = function

    def __repr__(self):
        return (
            f"ExpressionInfo(expr={self.expr}, line_num={self.line_num}, "
            f"order={self.order}, variable={self.variable}, function={self.function})"
        )


class IRParser:
    def __init__(self, ir_content):
        self.ir_content = ir_content
        self.nondet_var_pattern = re.compile(
            r"\((\d+)\) ([\w']+!)\d+@?(\d+)?#(\d+) == nondet_symbol<(.+?)>\(symex::nondet\d+\)"
        )
        self.expression_pattern = re.compile(
            r"\((\d+)\) ([\w']+!)\d+@?(\d+)?#(\d+) == (.+)"
        )
        self.assertion_pattern = re.compile(r"\((\d+)\) ASSERT\((.+)\)")
        self.guard_pattern = re.compile(r"\((\d+)\) \\guard#(\d+) == (.+)")
        self.line_comment_pattern = re.compile(r"line (\d+)")
        self.function_comment_pattern = re.compile(r"function (\w+)")
        self.last_line_numbers = defaultdict(int)
        self.expressions = []
        self.current_function = None

    def convert_variable(self, var):
        if "\\guard" in var:
            parts = var.split("#")
            return f"guard_{parts[1]}"
        parts = var.split("!")
        name = parts[0]
        thread_frame_ssa = parts[1].split("#")
        ssa = thread_frame_ssa[1]
        return f"{name}_{ssa}"

    def convert_expression(self, expr):
        expr = re.sub(
            r"([\w']+!)\d+@?(\d+)?#(\d+)",
            lambda m: self.convert_variable(m.group(0)),
            expr,
        )
        expr = re.sub(
            r"\\guard#(\d+)",
            lambda m: self.convert_variable(f"\\guard#{m.group(1)}"),
            expr,
        )
        expr = expr.replace("FLOAT+", "FLOAT_SUM").replace("FLOAT*", "FLOAT_MUL")
        return expr

    def process_line(self, line, current_line_num):
        line = line.strip()

        # Match nondet variables
        nondet_match = self.nondet_var_pattern.match(line)
        if nondet_match:
            order, var_name, frame_num, ssa_num, var_type = nondet_match.groups()
            converted_var = self.convert_variable(f"{var_name}@{frame_num}#{ssa_num}")
            expr = f"{converted_var} = {var_type}"
            self.expressions.append(
                ExpressionInfo(
                    expr,
                    current_line_num,
                    int(order),
                    converted_var,
                    self.current_function,
                )
            )
            self.last_line_numbers[converted_var] = int(current_line_num)
            return

        # Match guard statements
        guard_match = self.guard_pattern.match(line)
        if guard_match:
            order, ssa_num, expr = guard_match.groups()
            converted_var = self.convert_variable(f"\\guard#{ssa_num}")
            converted_expr = self.convert_expression(expr)
            self.expressions.append(
                ExpressionInfo(
                    f"{converted_var} = {converted_expr}",
                    current_line_num,
                    int(order),
                    converted_var,
                    self.current_function,
                )
            )
            self.last_line_numbers[converted_var] = int(current_line_num)
            return

        # Match expressions
        expression_match = self.expression_pattern.match(line)
        if expression_match:
            order, var_name, frame_num, ssa_num, expr = expression_match.groups()
            frame_num = frame_num if frame_num is not None else ""
            converted_var = self.convert_variable(f"{var_name}@{frame_num}#{ssa_num}")
            converted_expr = self.convert_expression(expr)
            self.expressions.append(
                ExpressionInfo(
                    f"{converted_var} = {converted_expr}",
                    current_line_num,
                    int(order),
                    converted_var,
                    self.current_function,
                )
            )
            self.last_line_numbers[converted_var] = int(current_line_num)
            return

        # Match assertions
        assertion_match = self.assertion_pattern.match(line)
        if assertion_match:
            order, assertion = assertion_match.groups()
            converted_assertion = self.convert_expression(assertion)
            self.expressions.append(
                ExpressionInfo(
                    f"ASSERT({converted_assertion})",
                    current_line_num,
                    int(order),
                    None,
                    self.current_function,
                )
            )
            self.last_line_numbers["ASSERT"] = int(current_line_num)

    def process_ir_content(self):
        current_line_num = None
        for line in self.ir_content.splitlines():
            line_comment_match = self.line_comment_pattern.search(line)
            function_comment_match = self.function_comment_pattern.search(line)
            if function_comment_match:
                self.current_function = function_comment_match.group(1)
            if line_comment_match:
                current_line_num = int(line_comment_match.group(1))
            else:
                self.process_line(line, current_line_num)

    def get_expressions(self):
        return self.expressions

    def get_last_line_numbers(self):
        return dict(self.last_line_numbers)


if __name__ == "__main__":
    # Sample IR content for demonstration
    ir_content = """
    Program constraints:
    // 15
    // 15
    ...
    // 5
    // 16 file program.c line 1 function candidate
    // 17 file program.c line 1 function candidate
    (10) x!0@1#2 == nondet_symbol<signed int>(symex::nondet0)
    // 18 file program.c line 1 function candidate
    // 19 file program.c line 1 function candidate
    // 20 file program.c line 1 function candidate
    (11) y!0@1#2 == nondet_symbol<signed int>(symex::nondet1)
    // 21 file program.c line 1 function candidate
    // 22 file program.c line 1
    // 22 file program.c line 1
    // 22 file program.c line 1
    (12) x!0@1#1 == x!0@1#2
    // 22 file program.c line 1
    (13) y!0@1#1 == y!0@1#2
    // 6 file program.c line 2 function candidate
    // 7 file program.c line 3 function candidate
    // 7 file program.c line 3 function candidate
    (14) \\guard#1 == x!0@1#1 >= 1
    // 8 file program.c line 4 function candidate
    (15) res!0@1#2 == x!0@1#1 + y!0@1#1 * 3
        guard: \\guard#1
    // 9 file program.c line 4 function candidate
    // 10 file program.c line 6 function candidate
    (16) res!0@1#3 == x!0@1#1 + y!0@1#1 * 4
        guard: !\\guard#1
    // 11 file program.c line 8 function candidate
    (17) res!0@1#4 == (\\guard#1 ? res!0@1#2 : res!0@1#3)
    // 11 file program.c line 8 function candidate
    (18) ASSERT(x!0@1#1 >= 1 ? x!0@1#1 + y!0@1#1 * 3 == res!0@1#4 : x!0@1#1 + y!0@1#1 * 4 == res!0@1#4)
    // 12 file program.c line 9 function candidate
    (sliced) candidate!0#1 == res!0@1#4
    // 14 file program.c line 10 function candidate
    // 22 file program.c line 1
    (sliced) return'!0#1 == candidate!0#1
    // 23 file program.c line 1
    // 26
    """

    ir_content_1 = """
    Program constraints:
    // 14
    // 14
    // 0 file <built-in-additions> line 8
    (1) SHARED_WRITE(__CPROVER_dead_object#1)
    // 0 file <built-in-additions> line 8
    (2) __CPROVER_dead_object#1 == NULL
    // 1 file <built-in-additions> line 7
    (3) SHARED_WRITE(__CPROVER_deallocated#1)
    // 1 file <built-in-additions> line 7
    (4) __CPROVER_deallocated#1 == NULL
    // 2 file <built-in-additions> line 12
    (5) SHARED_WRITE(__CPROVER_max_malloc_size#1)
    // 2 file <built-in-additions> line 12
    (6) __CPROVER_max_malloc_size#1 == 36028797018963968ul
    // 3 file <built-in-additions> line 9
    (7) SHARED_WRITE(__CPROVER_memory_leak#1)
    // 3 file <built-in-additions> line 9
    (8) __CPROVER_memory_leak#1 == NULL
    // 4 file <built-in-additions> line 16
    (9) __CPROVER_rounding_mode!0#1 == 0
    // 5
    // 15 file program.float.c line 1 function program
    // 16 file program.float.c line 1 function program
    (10) x!0@1#2 == nondet_symbol<float>(symex::nondet0)
    // 17 file program.float.c line 1 function program
    // 18 file program.float.c line 1 function program
    // 19 file program.float.c line 1 function program
    (11) y!0@1#2 == nondet_symbol<float>(symex::nondet1)
    // 20 file program.float.c line 1 function program
    // 21 file program.float.c line 1
    // 21 file program.float.c line 1
    // 21 file program.float.c line 1
    (12) x!0@1#1 == x!0@1#2
    // 21 file program.float.c line 1
    (13) y!0@1#1 == y!0@1#2
    // 6 file program.float.c line 2 function program
    // 6 file program.float.c line 2 function program
    (14) \\guard#1 == x!0@1#1 >= 1.0f
    // 7 file program.float.c line 3 function program
    (15) program!0#1 == FLOAT+(x!0@1#1, FLOAT*(y!0@1#1, 3.0f, 0), 0)
        guard: \\guard#1
    // 8 file program.float.c line 3 function program
    // 10 file program.float.c line 5 function program
    (16) program!0#2 == FLOAT+(x!0@1#1, FLOAT*(y!0@1#1, 4.0f, 0), 0)
        guard: !\\guard#1
    // 11 file program.float.c line 5 function program
    // 13 file program.float.c line 7 function program
    (17) program!0#3 == (\\guard#1 ? program!0#1 : program!0#2)
    // 13 file program.float.c line 7 function program
    // 21 file program.float.c line 1
    (18) return'!0#1 == program!0#3
    // 22 file program.float.c line 1
    // 25
    """

    # Create an instance of IRParser with the sample content
    parser = IRParser(ir_content)

    # Process the IR content
    parser.process_ir_content()

    # Get the expressions
    expressions = parser.get_expressions()

    # Print the expressions and their line numbers
    print("\nExtracted Expressions:")
    for expr, line_num in expressions:
        print(f"Line {line_num}: {expr}")

    # Get the last line numbers seen
    last_line_numbers = parser.get_last_line_numbers()

    # Print the dictionary of last line numbers seen
    print("\nLast line numbers seen:")
    for expr, line_num in last_line_numbers.items():
        print(f"{expr}: {line_num}")
