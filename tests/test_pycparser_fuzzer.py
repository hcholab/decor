import re
import sys
from pycparser import c_parser, c_generator, c_ast
import subprocess
import ctypes
from ctypes import CDLL
import random
import os
import time

# Example usage

# This should be the path to your C file
# file_path = "./benchmarks/bitween/dig/bresenham.c"
# func_name = "bresenham"  # This should be the name of the function you want to fuzz

file_path = "./benchmarks/bitween/dig/cohencu.c"
func_name = "cohencu"  # This should be the name of the function you want to fuzz

iterations = 30  # Number of times to call the function with random inputs

start_time = time.time()


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


# NOTE: 1. Preprocessing part


def preprocess_c_code(c_code):
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


c_code = read_c_file(file_path)

if c_code is None:
    print("Error reading the C file.")
    exit()

preprocessed_code, preprocessor_directives = preprocess_c_code(c_code)

# NOTE: 2. Parsing and instrumentation part

# Parse the code using pycparser
parser = c_parser.CParser()
ast = parser.parse(preprocessed_code.strip())

trace_headers = {}


class TransformFunc(c_ast.NodeVisitor):
    def visit_FuncDef(self, node):
        self.variables = {}
        self.params = []
        self.return_type = None  # Added to capture the function's return type

        if node.decl.name == func_name:
            # Extract the function's return type
            self.return_type = (
                node.decl.type.type.type.names[0]
                if isinstance(node.decl.type, c_ast.FuncDecl)
                else "int"
            )

            # Collect function parameter types
            params = node.decl.type.args.params
            for param in params:
                self.variables[param.name] = param.type.type.names[0]
                self.params.append((param.name, param.type.type.names[0]))

            # Collect local variable types from declarations
            for decl in node.body.block_items:
                if isinstance(decl, c_ast.Decl):
                    self.variables[decl.name] = decl.type.type.names[0]

            print(f"Function Name: {func_name}")
            print(f"Parameters: {self.params}")
            print(f"Return Type: {self.return_type}")
            print(f"Types: {self.variables}")

            # Traverse and modify the function body
            self.replace_vtrace_calls(node.body)

    def replace_vtrace_calls(self, node):
        if isinstance(node, c_ast.Compound):
            items_to_replace = []
            for item in node.block_items:
                if isinstance(item, c_ast.FuncCall) and item.name.name.startswith(
                    "vtrace"
                ):
                    # Create the correct format string based on variable types
                    args_str = f"{item.name.name}; "
                    args_str += "; ".join(
                        self.format_specifier(arg.name) for arg in item.args.exprs
                    )
                    trace_headers[f"{item.name.name}"] = (
                        f"{item.name.name}; "
                        + "; ".join([f"I {arg.name}" for arg in item.args.exprs])
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
                    # Create the fflush call
                    fflush_call = c_ast.FuncCall(
                        name=c_ast.ID(name="fflush"),
                        args=c_ast.ExprList(exprs=[c_ast.ID(name="stdout")]),
                    )

                    # Append the tuple of old item, new printf call, and new fflush call to items_to_replace
                    items_to_replace.append((item, new_printf_call, fflush_call))

            # Perform replacements outside of the original loop
            for old_item, new_printf_call, fflush_call in items_to_replace:
                index = node.block_items.index(old_item)
                node.block_items[index] = (
                    new_printf_call  # Replace the old vtrace call with new printf call
                )
                node.block_items.insert(
                    index + 1, fflush_call
                )  # Insert fflush right after the new printf call

        # Recursively process child nodes
        for child in node:
            self.replace_vtrace_calls(child)

    def format_specifier(self, variable_name):
        type_name = self.variables.get(variable_name, "int")
        if type_name == "double":
            return "%lf"
        elif type_name == "float":
            return "%f"
        elif type_name == "int":
            return "%d"
        return "%d"  # Default case, consider int if type not found


# Visit and process the function definition
transformer = TransformFunc()
transformer.visit(ast)

# Generate the modified C code
generator = c_generator.CGenerator()
final_code = generator.visit(ast)

# Add back the preprocessor directives
final_c_code_with_directives = "\n".join(preprocessor_directives) + "\n" + final_code
print(final_c_code_with_directives)

func_name_annotated = f"{func_name}_annotated.c"

with open(func_name_annotated, "w") as file:
    file.write(final_c_code_with_directives)

# NOTE: 3. Compilation part

# Compile the C file into a shared library (.so file)
shared_lib_name = f"lib{func_name}.so"
compile_command = f"gcc -shared -fPIC -o {shared_lib_name} {func_name_annotated}"

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

# Load the shared library
lib = CDLL(f"./lib{func_name}.so")

# Define the function prototype in ctypes
# Get the function by name
func = getattr(lib, func_name)

if transformer.return_type == "int":
    func.restype = ctypes.c_int
elif transformer.return_type == "float":
    func.restype = ctypes.c_float
elif transformer.return_type == "double":
    func.restype = ctypes.c_double

# convert transformers params to ctypes
param_types = []
for param in transformer.params:
    if param[1] == "int":
        param_types.append(ctypes.c_int)
    elif param[1] == "float":
        param_types.append(ctypes.c_float)
    elif param[1] == "double":
        param_types.append(ctypes.c_double)

# Define the types of the parameters
func.argtypes = param_types


def random_value(ctypes_type):
    """
    Generates a random value based on the ctypes type.

    Args:
        ctypes_type: The ctypes type for which to generate a value.

    Returns:
        A random value appropriate for the given type.
    """
    if ctypes_type == ctypes.c_int:
        return random.randint(0, 300)
    elif ctypes_type == ctypes.c_float:
        return ctypes.c_float(random.uniform(-100.0, 100.0))
    elif ctypes_type == ctypes.c_double:
        return ctypes.c_double(random.uniform(-100.0, 100.0))
    return 0


# Define the trace file name
trace_file_name = f"{func_name}.trace.csv"


def fuzz_function(func, param_types, iterations=10):
    """
    Fuzzes the given C function by calling it with random inputs and writes the output
    to a trace file named after the function, while keeping other outputs such as status
    messages and errors in the console.

    Args:
        func: The C function to be fuzzed.
        param_types: List of ctypes types for the function's parameters.
        func_name: Name of the function, used to name the trace file.
        iterations: Number of times the function should be called with random inputs.
    """
    original_stdout_fd = sys.stdout.fileno()  # usually 1 for stdout

    # Create a duplicate of the original stdout for restoring later
    saved_stdout_fd = os.dup(original_stdout_fd)

    try:
        with open(trace_file_name, "w+") as trace_file:
            for i in range(iterations):
                random_args = [random_value(ptype) for ptype in param_types]

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

            print(f"Trace file '{trace_file_name}' created.")
    except KeyboardInterrupt:
        print("Fuzzing interrupted by user.")
    finally:
        # Ensure stdout is restored even if interrupted
        os.dup2(saved_stdout_fd, original_stdout_fd)
        # Close the duplicated file descriptor
        os.close(saved_stdout_fd)


# Fuzz the function with random inputs
fuzz_function(func, param_types, iterations)


# NOTE: 5. Post-processing part


# Sort the trace file by trace markers
def sort_file_by_trace_marker(input_file_path, output_file_path=None):
    """
    Sorts the lines in a file based on the trace markers (e.g., vtrace1, vtrace2, etc.).
    Args:
        input_file_path (str): Path to the input file containing unsorted trace entries.
        output_file_path (str, optional): Path to the output file where sorted data will be written.
                                         If not specified, the input file will be overwritten.
    """
    # Use the input file path as the default output file path if none is provided
    if output_file_path is None:
        output_file_path = input_file_path

    with open(input_file_path, "r") as file:
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
    with open(output_file_path, "w") as file:
        for key in sorted_keys:
            file.write(trace_headers[key] + "\n")
            file.writelines(trace_dict[key])


# Sort the trace file by trace markers
sort_file_by_trace_marker(trace_file_name)

end_time = time.time()

print(f"Fuzzing time: {end_time - start_time:.2f} seconds.")
