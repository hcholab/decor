import re
from pycparser import c_parser, c_generator, c_ast
import subprocess
import ctypes
from ctypes import CDLL
import random


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


# Example usage
file_path = "bresenham.c"  # This should be the path to your C file
func_name = "bresenham"  # This should be the name of the function you want to fuzz

c_code = read_c_file(file_path)

# Extract and preserve preprocessor directives
preprocessor_directives = re.findall(r"^\s*#.*$", c_code, flags=re.MULTILINE)
# Remove directives and vtrace function definitions from the code
preprocessed_code = re.sub(
    r"^\s*#.*$|^void vtrace[0-9]+\(.*\)\s*\{\s*\}", "", c_code, flags=re.MULTILINE
)

# Parse the code using pycparser
parser = c_parser.CParser()
ast = parser.parse(preprocessed_code.strip())


class TransformFunc(c_ast.NodeVisitor):
    def visit_FuncDef(self, node):
        self.variables = {}
        self.params = {}
        self.return_type = None  # Added to capture the function's return type

        if node.decl.name == func_name:
            # Extract the function's return type
            self.return_type = (
                node.decl.type.type.names[0]
                if isinstance(node.decl.type, c_ast.FuncDecl)
                else "int"
            )

            # Collect function parameter types
            params = node.decl.type.args.params
            for param in params:
                self.variables[param.name] = param.type.type.names[0]
                self.params[param.name] = param.type.type.names[0]

            # Collect local variable types from declarations
            for decl in node.body.block_items:
                if isinstance(decl, c_ast.Decl):
                    self.variables[decl.name] = decl.type.type.names[0]

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
                    args_str = ", ".join(
                        self.format_specifier(arg.name) for arg in item.args.exprs
                    )
                    args = ", ".join([f"{arg.name}" for arg in item.args.exprs])
                    new_func_call = c_ast.FuncCall(
                        name=c_ast.ID(name="printf"),
                        args=c_ast.ExprList(
                            exprs=[
                                c_ast.Constant(type="string", value=f'"{args_str}\\n"'),
                                *item.args.exprs,
                            ]
                        ),
                    )
                    items_to_replace.append((item, new_func_call))
            for old_item, new_item in items_to_replace:
                index = node.block_items.index(old_item)
                node.block_items[index] = new_item
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


# Load the shared library
lib = CDLL(f"./lib{func_name}.so")

# Define the function prototype in ctypes
func = lib.bresenham
func.restype = ctypes.c_int

# Define the types of the parameters
param_types = {"X": ctypes.c_int, "Y": ctypes.c_double}
func.argtypes = [param_types["X"], param_types["Y"]]


# Function to generate random values based on type
def random_value(ctypes_type):
    if ctypes_type == ctypes.c_int:
        return random.randint(-1000, 1000)
    elif ctypes_type == ctypes.c_float:
        return ctypes.c_float(random.uniform(-1000.0, 1000.0))
    elif ctypes_type == ctypes.c_double:
        return ctypes.c_double(random.uniform(-1000.0, 1000.0))
    return 0


# Fuzzing the function
num_tests = 10
for _ in range(num_tests):
    random_X = random_value(ctypes.c_int)
    random_Y = random_value(ctypes.c_double)
    result = func(random_X, random_Y)
    print(f"Called {func_name}(X={random_X}, Y={random_Y}) = {result}")
