import re
from pycparser import c_parser, c_generator, c_ast
import subprocess
import random
import os
import time


def read_c_file(file_path):
    try:
        with open(file_path, "r") as file:
            c_code = file.read()
        return c_code
    except FileNotFoundError:
        print("Error: The file does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def preprocess_c_code(c_code):
    """
    Preprocesses the C code by removing comments, vtrace function definitions, and adding stdio.h if not included.
    """
    # Extract preprocessor directives and store them
    preprocessor_directives = re.findall(r"^\s*#.*$", c_code, flags=re.MULTILINE)
    # Check if stdio.h is included
    stdio_included = any(
        "#include <stdio.h>" in directive for directive in preprocessor_directives
    )
    # Add stdio.h if not included
    if not stdio_included:
        preprocessor_directives.append("#include <stdio.h>")

    assert_included = any(
        "#include <assert.h>" in directive for directive in preprocessor_directives
    )
    # Add assert.h if not included
    if not assert_included:
        preprocessor_directives.append("#include <assert.h>")

    # Remove directives and vtrace function definitions from the code
    preprocessed_code = re.sub(
        r"^\s*#.*$|^void vtrace[0-9]+\(.*\)\s*\{\s*\}", "", c_code, flags=re.MULTILINE
    )

    # Pattern to match single-line and multi-line comments
    comments_pattern = r"//.*?$|/\*.*?\*/"
    # Pattern to remove specific function definitions
    functions_pattern = r"^void vtrace[0-9]+\s*\(.*\)\s*\{.*?\}"

    # Remove comments
    preprocessed_code = re.sub(
        comments_pattern, "", preprocessed_code, flags=re.DOTALL | re.MULTILINE
    )
    # Remove vtrace function definitions
    preprocessed_code = re.sub(
        functions_pattern, "", preprocessed_code, flags=re.MULTILINE | re.DOTALL
    )

    return preprocessed_code.strip(), preprocessor_directives


class TransformFunc(c_ast.NodeVisitor):
    """
    A class to transform a C function by replacing vtrace calls with printf calls and handling vassume calls.
    """

    def __init__(self, func_name):
        self.func_name = func_name
        self.trace_headers = {}
        # Added to capture the entry function's signature
        self.params = []
        self.return_type = None  # Added to capture the function's return type
        self.distr = {}  # Dictionary to store distribution intervals

    def visit_FuncDef(self, node):
        self.curr_params = []
        self.curr_variables = {}
        self.curr_return_type = None

        # Extract the function's return type
        self.curr_return_type = (
            node.decl.type.type.type.names[0]
            if isinstance(node.decl.type, c_ast.FuncDecl)
            else "int"
        )
        if node.decl.name == self.func_name:
            self.return_type = self.curr_return_type

        # Collect function parameter types
        params = node.decl.type.args.params
        for param in params:
            type_name = param.type.type.names[0]
            self.curr_variables[param.name] = type_name
            self.curr_params.append((param.name, type_name))
            if node.decl.name == self.func_name:
                self.params.append((param.name, type_name))

        # if block_items is None, the function is defined but not implemented
        if node.body.block_items is None:
            return

        # Collect local variable types from declarations
        for decl in node.body.block_items:
            if isinstance(decl, c_ast.Decl):
                self.curr_variables[decl.name] = decl.type.type.names[0]

        print(f"Function Name: {node.decl.name}")
        print(f"Parameters: {self.curr_params}")
        print(f"Return Type: {self.curr_return_type}")
        print(f"Types: {self.curr_variables}")

        # Traverse and modify the function body
        self.replace_vtrace_calls(node.body)

    def replace_vtrace_calls(self, node):
        if isinstance(node, c_ast.Compound):
            items_to_replace = []
            for item in node.block_items:
                if isinstance(item, c_ast.FuncCall):
                    if item.name.name.startswith("vtrace"):
                        new_printf_call, fflush_call = self.handle_vtrace_call(item)
                        items_to_replace.append((item, (new_printf_call, fflush_call)))
                    elif item.name.name == "vassume" or item.name.name == "assume":
                        new_if_statement = self.handle_vassume_call(item)
                        items_to_replace.append((item, new_if_statement))
                    elif item.name.name == "vdistr":
                        self.handle_vdistr_call(item)
                        items_to_replace.append((item, None))

            for old_item, new_item in items_to_replace:
                index = node.block_items.index(old_item)
                if isinstance(new_item, tuple):  # This is from vtrace handling
                    node.block_items[index] = new_item[0]  # Replace with printf call
                    node.block_items.insert(index + 1, new_item[1])  # Insert fflush
                else:  # This is from vassume and vdistr handling
                    if new_item is not None:
                        node.block_items[index] = new_item  # Replace with if statement
                    else:
                        node.block_items.remove(old_item)

        # Recursively process child nodes
        for child in node:
            self.replace_vtrace_calls(child)

    def handle_vtrace_call(self, item):
        args_str = f"{item.name.name}; " + "; ".join(
            self.format_specifier(arg.name) for arg in item.args.exprs
        )
        self.trace_headers[f"{item.name.name}"] = f"{item.name.name}; " + "; ".join(
            [f"I {arg.name}" for arg in item.args.exprs]
        )
        new_printf_call = c_ast.FuncCall(
            name=c_ast.ID(name="printf"),
            args=c_ast.ExprList(
                exprs=[
                    c_ast.Constant(type="string", value=f'"{args_str}\\n"'),
                    *item.args.exprs,
                ]
            ),
        )
        fflush_call = c_ast.FuncCall(
            name=c_ast.ID(name="fflush"),
            args=c_ast.ExprList(exprs=[c_ast.ID(name="stdout")]),
        )
        return new_printf_call, fflush_call

    def handle_vassume_call(self, item):
        # Negate the condition and create an if statement
        negated_condition = c_ast.UnaryOp(op="!", expr=item.args.exprs[0])
        return_statement = c_ast.Return(expr=c_ast.Constant(type="int", value="0"))
        if_statement = c_ast.If(
            cond=negated_condition,
            iftrue=c_ast.Compound(block_items=[return_statement]),
            iffalse=None,
        )
        return if_statement

    def handle_vdistr_call(self, item):
        # Assuming the vdistr call looks like vdistr(var, min, max)
        if len(item.args.exprs) == 3:
            var_name = item.args.exprs[0].name
            min_val = self.extract_value(item.args.exprs[1])
            max_val = self.extract_value(item.args.exprs[2])
            if var_name not in [param[0] for param in self.params]:
                print(f"Variable {var_name} not found in function parameters.")
                return
            self.distr[var_name] = [min_val, max_val]  # Store the distribution interval
        else:
            print("Invalid vdistr call:", item)

    def extract_value(self, expr):
        # This method extracts the value from the expression,
        # whether it is a direct constant or a negated value.
        if isinstance(expr, c_ast.Constant):
            type = expr.type
            value = expr.value
            if type == "int":
                return int(value)
            elif type == "float" or type == "double":
                return float(value.strip("f"))
        elif isinstance(expr, c_ast.UnaryOp) and expr.op == "-":
            # Handle negation
            type = expr.expr.type
            value = expr.expr.value
            if type == "int":
                return -1 * int(value)
            elif type == "float" or type == "double":
                return -1 * float(value.strip("f"))
        else:
            raise ValueError(f"Unsupported expression type for bounds: {type(expr)}")

    def format_specifier(self, variable_name):
        type_name = self.curr_variables.get(variable_name, "int")
        if type_name == "double":
            return "%lf"
        elif type_name == "float":
            return "%f"
        elif type_name == "int":
            return "%d"
        return "%d"  # Default case, consider int if type not found


def create_test_driver(func_name, params, return_type):
    """
    Generates a main function to test the given C function with command-line arguments.
    """
    # String template for the main function
    main_function = "int main(int argc, char** argv) {\n"
    main_function += f"    if (argc != {len(params) + 1}) {{\n"
    main_function += '        printf("Usage: %s '
    for param_name, param_type in params:
        main_function += f"<{param_name}:{param_type}> "
    main_function += '\\n", argv[0]);\n        return 1;\n    }\n\n'
    for i, (param_name, param_type) in enumerate(params, start=1):
        conversion_function = "atoi" if param_type == "int" else "atof"
        main_function += (
            f"    {param_type} {param_name} = {conversion_function}(argv[{i}]);\n"
        )
    param_names = ", ".join([name for name, _ in params])
    if return_type != "void":
        main_function += f"    {return_type} result = {func_name}({param_names});\n"
        print_statement = (
            'printf("%d\\n", result);'
            if return_type == "int"
            else 'printf("%f\\n", result);'
        )
        main_function += f"    {print_statement}\n"
    else:
        main_function += f"    {func_name}({param_names});\n"
    main_function += "    return 0;\n}\n"
    return main_function


def compile_code(source_file):
    # Assuming gcc is installed and available in the path
    executable = source_file.replace(".fuzzer.c", ".fuzzer")
    compilation_command = ["gcc", source_file, "-o", executable]
    try:
        subprocess.run(compilation_command, check=True)
        print(f"Compilation successful: {executable} created.")
        return executable
    except subprocess.CalledProcessError:
        print("Compilation failed.")
        return None


def random_value(param_type, distr=None):
    """
    Generates a random value based on the parameter type.
    """
    if param_type == "int":
        if distr:
            return random.randint(int(distr[0]), int(distr[1]))
        return random.randint(0, 300)
    elif param_type == "float":
        if distr:
            return random.uniform(float(distr[0]), float(distr[1]))
        return random.uniform(-2.0, 2.0)
    elif param_type == "double":
        if distr:
            return random.uniform(float(distr[0]), float(distr[1]))
        return random.uniform(-2.0, 2.0)
    return 0


def fuzz_function_to_collect_traces(
    executable, trace_path, iterations, params, distributions
):
    """
    Fuzzes the given C function by calling it with random inputs and writes the output
    to a trace file named after the function, while keeping other outputs such as status
    messages and errors in the console.
    """

    # extract the file name from the path
    file_name = os.path.basename(executable)
    file_name = os.path.splitext(file_name)[0]

    with open(trace_path, "w+") as trace_file:
        results = []
        for _ in range(iterations):
            # Generate test inputs based on the specified distributions or simply random within a range
            test_inputs = []
            for param in params:
                param_name = param[0]
                param_type = param[1]
                test_inputs.append(
                    str(random_value(param_type, distributions[param_name]))
                )

            # Convert list to command-line arguments
            input_str = " ".join(test_inputs)

            # Run the executable with the generated inputs
            result = subprocess.run(
                [executable] + test_inputs, capture_output=True, text=True
            )

            # Store the result along with the input data
            results.append((input_str, result.stdout, result.stderr, result.returncode))

        # Analyze the results
        for input_data, output, error, return_code in results:
            if return_code != 0:
                print(
                    f"Run Failed | Input: {input_data} | Error Message: {error.strip()}"
                )
            else:
                out = ""
                # Process each line in the output
                for line in output.splitlines():
                    if line.startswith("vtrace"):
                        trace_file.write(
                            line + "\n"
                        )  # Write trace lines to the trace file
                    else:
                        out += line + "; "

                # extract the trace markers from the output (starts with 'vtraceN;')
                print(f"{file_name}({input_data}): {out}")

        print(f"Trace file written to: {trace_path}")


# Sort the trace file by trace markers
def sort_file_by_trace_marker(trace_path, trace_headers):
    """
    Sorts the lines in a file based on the trace markers (e.g., vtrace1, vtrace2, etc.).
    """
    with open(trace_path, "r") as file:
        lines = file.readlines()

    # Create a dictionary to hold lines based on their trace marker
    trace_dict = {}
    for line in lines:
        # Assume line format starts with 'vtraceN;' where N is a number
        marker = line.split(";")[0]
        if marker in trace_dict:
            trace_dict[marker].append(line)
        else:
            trace_dict[marker] = [line]

    # Sort dictionary keys to ensure vtrace1, vtrace2,... order
    sorted_keys = sorted(trace_dict.keys(), key=lambda x: (x[:-1], int(x[-1])))

    # Write sorted lines back to file
    with open(trace_path, "w") as file:
        for key in sorted_keys:
            file.write(trace_headers[key] + "\n")
            file.writelines(trace_dict[key])


def fuzz_and_trace(file_path: str, func_name: str, iterations: int):
    """
    Fuzzes the given C function by calling it with random inputs and writes the output as a trace file.
    """

    # remove the .c extension from the file_path
    folder_path = os.path.dirname(file_path)

    # NOTE: Load the C code to be fuzzed
    start_time = time.time()

    c_code = read_c_file(file_path)

    if c_code is None:
        print("Error reading the C file.")
        exit()

    # NOTE: Preprocessing part

    # Preprocess the C code and extract preprocessor directives
    # CParser does not handle preprocessor directives, so we need to extract and add them back later
    preprocessed_code, preprocessor_directives = preprocess_c_code(c_code)

    # NOTE: Parsing and instrumentation part

    # Parse the code using pycparser
    parser = c_parser.CParser()
    ast = parser.parse(preprocessed_code.strip())
    # Visit and process the function definition
    transformer = TransformFunc(func_name)
    transformer.visit(ast)

    # Generate the modified C code
    generator = c_generator.CGenerator()
    modified_code = generator.visit(ast)

    # NOTE: Instrument Test Driver

    # Generate the new main function
    params = transformer.params
    return_type = transformer.return_type
    main_code = create_test_driver(func_name, params, return_type)

    # Combine modified code with the new main function
    modified_code = modified_code + "\n" + main_code

    # Add back the preprocessor directives
    final_code = "\n".join(preprocessor_directives) + "\n" + modified_code
    print(final_code)

    # write the final code to a file
    test_driver_file = f"{folder_path}/{func_name}.fuzzer.c"
    with open(test_driver_file, "w") as file:
        file.write(final_code)

    # NOTE: Compilation part

    # construct the executable
    executable = compile_code(test_driver_file)

    # NOTE: Fuzzing part

    print(f"Fuzzing {func_name} function with {iterations} random inputs...")
    print(f"Params: {transformer.params}")
    if transformer.distr:
        print(f"Distributions: {transformer.distr}")

    trace_path = f"{folder_path}/{func_name}.trace.csv"

    # Fuzz the function with random inputs
    fuzz_function_to_collect_traces(
        executable, trace_path, iterations, transformer.params, transformer.distr
    )

    # NOTE: Post-processing part

    # Sort the trace file by trace markers
    sort_file_by_trace_marker(trace_path, transformer.trace_headers)

    print(f"Fuzzing time: {time.time() - start_time:.2f} seconds.")

    return trace_path


if __name__ == "__main__":
    # Example usage

    # This should be the path to your C file
    file_path = "./benchmarks/bitween/dig/bresenham.c"
    func_name = "bresenham"  # This should be the name of the function you want to fuzz

    # file_path = "./benchmarks/bitween/dig/cohencu.c"
    # func_name = "cohencu"

    # file_path = "./benchmarks/bitween/dig/cohendiv.c"
    # func_name = "cohendiv"

    # file_path = "./benchmarks/bitween/dig/dijkstra.c"
    # func_name = "dijkstra"

    # file_path = "./benchmarks/bitween/dig/divbin.c"
    # func_name = "divbin"

    # file_path = "./benchmarks/bitween/dig/egcd.c"
    # func_name = "egcd"

    # file_path = "./benchmarks/bitween/dig/egcd2.c"
    # func_name = "egcd2"

    # file_path = "./benchmarks/bitween/dig/egcd3.c"
    # func_name = "egcd3"

    # file_path = "./benchmarks/bitween/dig/fermat1.c"
    # func_name = "fermat1"

    # file_path = "./benchmarks/bitween/dig/fermat2.c"
    # func_name = "fermat2"

    # file_path = "./benchmarks/bitween/dig/freire1_int.c"
    # func_name = "freire1_int"

    # file_path = "./benchmarks/bitween/dig/freire1.c"
    # func_name = "freire1"

    # file_path = "./benchmarks/bitween/dig/freire2.c"
    # func_name = "freire2"

    # file_path = "./benchmarks/bitween/dig/geo1.c"
    # func_name = "geo1"

    # file_path = "./benchmarks/bitween/dig/geo2.c"
    # func_name = "geo2"

    # file_path = "./benchmarks/bitween/dig/geo3.c"
    # func_name = "geo3"

    # file_path = "./benchmarks/bitween/dig/hard.c"
    # func_name = "hard"

    # file_path = "./benchmarks/bitween/dig/knuth.c"
    # func_name = "knuth"

    # file_path = "./benchmarks/bitween/dig/lcm1.c"
    # func_name = "lcm1"

    # file_path = "./benchmarks/bitween/dig/lcm2.c"
    # func_name = "lcm2"

    # file_path = "./benchmarks/bitween/dig/mannadiv.c"
    # func_name = "mannadiv"

    # file_path = "./benchmarks/bitween/fpcore/rosa.c"
    # func_name = "doppler1"

    # file_path = "./benchmarks/bitween/fpcore/salsa.c"
    # func_name = "Odometry"
    # func_name = "PID"
    # func_name = "Runge_Kutta_4"

    iterations = 30  # Number of times to call the function with random inputs

    fuzz_and_trace(file_path, func_name, iterations)
