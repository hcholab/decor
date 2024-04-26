import re
import sys
from pycparser import c_parser, c_generator, c_ast
import subprocess
import ctypes
from ctypes import CDLL
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
                    elif item.name.name == "vassume":
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
                return float(value)
        elif isinstance(expr, c_ast.UnaryOp) and expr.op == "-":
            # Handle negation
            type = expr.expr.type
            value = expr.expr.value
            if type == "int":
                return int(value)
            elif type == "float" or type == "double":
                return float(value)
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


def random_value(ctypes_type, distr=None):
    """
    Generates a random value based on the ctypes type.
    """
    if ctypes_type == ctypes.c_int:
        if distr:
            return random.randint(int(distr[0]), int(distr[1]))
        return random.randint(0, 300)
    elif ctypes_type == ctypes.c_float:
        if distr:
            return ctypes.c_float(random.uniform(float(distr[0]), float(distr[1])))
        return ctypes.c_float(random.uniform(-2.0, 2.0))
    elif ctypes_type == ctypes.c_double:
        if distr:
            return ctypes.c_double(random.uniform(float(distr[0]), float(distr[1])))
        return ctypes.c_double(random.uniform(-2.0, 2.0))
    return 0


def load_shared_library_func(
    folder_path: str, func_name: str, return_type: str, params: list[tuple[str, str]]
):
    """
    Loads the shared library and defines the function prototype using ctypes.

    Args:
        func_name (str): Name of the function to be loaded.
        return_type (str): Return type of the function.
        params (list): List of tuples containing parameter names and types.
    """
    # Load the shared library
    lib = CDLL(f"{folder_path}/{func_name}.so")

    # Define the function prototype in ctypes
    func = getattr(lib, func_name)

    if return_type == "int":
        func.restype = ctypes.c_int
    elif return_type == "float":
        func.restype = ctypes.c_float
    elif return_type == "double":
        func.restype = ctypes.c_double

    # Convert the parameter types to ctypes
    param_types = []
    for param in params:
        if param[1] == "int":
            param_types.append(ctypes.c_int)
        elif param[1] == "float":
            param_types.append(ctypes.c_float)
        elif param[1] == "double":
            param_types.append(ctypes.c_double)

    # Define the types of the parameters
    func.argtypes = param_types

    return func


def fuzz_function(
    func, trace_path, iterations=30, params=list[str], distr=dict[str:list]
):
    """
    Fuzzes the given C function by calling it with random inputs and writes the output
    to a trace file named after the function, while keeping other outputs such as status
    messages and errors in the console.
    """

    original_stdout_fd = sys.stdout.fileno()  # usually 1 for stdout

    # Create a duplicate of the original stdout for restoring later
    saved_stdout_fd = os.dup(original_stdout_fd)

    try:
        with open(trace_path, "w+") as trace_file:
            for i in range(iterations):
                random_args = [
                    random_value(ptype, distr.get(params[i], None))
                    for i, ptype in enumerate(func.argtypes)
                ]

                # Flush any library-level buffers before redirection
                sys.stdout.flush()

                # Redirect stdout to our trace file
                os.dup2(trace_file.fileno(), original_stdout_fd)

                try:
                    # Perform the function call with stdout redirected
                    result = func(*random_args)
                except Exception as e:
                    # Write errors directly to the trace file if function fails
                    print(
                        f"Error calling {func.__name__} with args ({', '.join(map(str, random_args))}): {str(e)}",
                        file=trace_file,
                    )
                finally:
                    # Restore stdout immediately after the function call
                    os.dup2(saved_stdout_fd, original_stdout_fd)

                # Output the call status to console
                print(
                    f"Called {func.__name__}({', '.join(map(str, random_args))}) -> {result}"
                )

            print(f"Trace file '{trace_path}' created.")
    except KeyboardInterrupt:
        print("Fuzzing interrupted by user.")
    finally:
        # Ensure stdout is restored even if interrupted
        os.dup2(saved_stdout_fd, original_stdout_fd)
        # Close the duplicated file descriptor
        os.close(saved_stdout_fd)


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

    # NOTE: 0. Load the C code to be fuzzed
    start_time = time.time()

    c_code = read_c_file(file_path)

    if c_code is None:
        print("Error reading the C file.")
        exit()

    # NOTE: 1. Preprocessing part

    # Preprocess the C code and extract preprocessor directives
    # CParser does not handle preprocessor directives, so we need to extract and add them back later
    preprocessed_code, preprocessor_directives = preprocess_c_code(c_code)

    # NOTE: 2. Parsing and instrumentation part

    # Parse the code using pycparser
    parser = c_parser.CParser()
    ast = parser.parse(preprocessed_code.strip())
    # Visit and process the function definition
    transformer = TransformFunc(func_name)
    transformer.visit(ast)

    # Generate the modified C code
    generator = c_generator.CGenerator()
    final_code = generator.visit(ast)

    # Add back the preprocessor directives
    final_c_code_with_directives = (
        "\n".join(preprocessor_directives) + "\n" + final_code
    )
    print(final_c_code_with_directives)

    func_name_instrumented = f"{folder_path}/{func_name}.instrumented.c"

    with open(func_name_instrumented, "w") as file:
        file.write(final_c_code_with_directives)

    # NOTE: 3. Compilation part

    # Compile the C file into a shared library (.so file)
    shared_lib_name = f"{func_name}.so"
    compile_command = (
        f"gcc -shared -fPIC -o {folder_path}/{shared_lib_name} {func_name_instrumented}"
    )

    try:
        # Execute the compile command
        compilation_result = subprocess.run(
            compile_command, shell=True, check=True, text=True, stderr=subprocess.PIPE
        )
        print("Compilation successful. Shared library created:", shared_lib_name)
    except subprocess.CalledProcessError as e:
        # Handle errors in compilation
        print("Compilation failed:")
        print(e.stderr)

    # NOTE: 4. Fuzzing part

    # Load the shared library function
    func = load_shared_library_func(
        folder_path, func_name, transformer.return_type, transformer.params
    )

    trace_path = f"{folder_path}/{func_name}.trace.csv"

    print(f"Fuzzing {func_name} function with {iterations} random inputs...")
    print(f"Params: {transformer.params}")
    if transformer.distr:
        print(f"Distributions: {transformer.distr}")

    # Fuzz the function with random inputs
    fuzz_function(
        func,
        trace_path,
        iterations,
        [p[0] for p in transformer.params],
        transformer.distr,
    )

    # NOTE: 5. Post-processing part

    # Sort the trace file by trace markers
    sort_file_by_trace_marker(trace_path, transformer.trace_headers)

    print(f"Fuzzing time: {time.time() - start_time:.2f} seconds.")


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

    # file_path = "./benchmarks/bitween/dig/poly3_1.c"
    # func_name = "poly3_1"

    # file_path = "./benchmarks/bitween/dig/poly3.c"
    # func_name = "poly3"

    # file_path = "./benchmarks/bitween/dig/poly4.c"
    # func_name = "poly4"

    # file_path = "./benchmarks/bitween/dig/poly5.c"
    # func_name = "poly5"

    # file_path = "./benchmarks/bitween/dig/prod4br.c"
    # func_name = "prod4br"

    # file_path = "./benchmarks/bitween/dig/prodbin.c"
    # func_name = "prodbin"

    # file_path = "./benchmarks/bitween/dig/ps1.c"
    # func_name = "ps1"

    # file_path = "./benchmarks/bitween/dig/ps2.c"
    # func_name = "ps2"

    # file_path = "./benchmarks/bitween/dig/ps3.c"
    # func_name = "ps3"

    # file_path = "./benchmarks/bitween/dig/ps4.c"
    # func_name = "ps4"

    # file_path = "./benchmarks/bitween/dig/ps5.c"
    # func_name = "ps5"

    # file_path = "./benchmarks/bitween/dig/ps6.c"
    # func_name = "ps6"

    # file_path = "./benchmarks/bitween/dig/sqrt1.c"
    # func_name = "sqrt1"

    # file_path = "./benchmarks/bitween/fpcore/salsa.c"
    # func_name = "Odometry"
    # func_name = "PID"
    # func_name = "Runge_Kutta_4"
    # func_name = "Lead_lag_System"
    # func_name = "Trapeze"
    # func_name = "rocket_trajectory"  # NOTE: be careful with this one
    # func_name = "Jacobis_Method" # NOTE: be careful with this one
    # func_name = "Newton_Raphsons_Method"
    # func_name = "Eigenvalue_Computation"  # NOTE: be careful with this one
    # func_name = "Iterative_Gram_Schmidt_Method"

    # file_path = "./benchmarks/bitween/fpcore/rosa.c"
    # func_name = "doppler1"

    iterations = 30  # Number of times to call the function with random inputs

    fuzz_and_trace(file_path, func_name, iterations)
