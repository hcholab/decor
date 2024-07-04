import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))


from socrates.prog_synth.config import Config

config = Config()


import re


def convert_to_bracket_notation(expr):
    # match = re.search(r"let\s+\w+\s+(\(.+)\)", expr)
    # if match:
    # expr = match.group(1)
    return expr.replace("(", "{").replace(")", "}")
    # else:
    # return None


# Example usage
# expr1 = '(let expr1 (Mul (Num 2) (Add (Var "x") (Num 3))))'
# expr2 = '(let expr3 (Add (Var "h1") (Add (Var "x") (Var "x"))))'
expr1 = '(Add (Add (Var "x") (Var "x")) (Num 6))'  # expr = 2 * (x + 3)
# expr1 = '(Add (Var "h1") (Add (Var "x") (Var "x")))'  # expr = h1 + (x + x)
expr2 = '(Add (Add (Num 1) (Var "x")) (Var "x"))'  # expr = (1 + x) + x

bracket_notation1 = convert_to_bracket_notation(expr1).replace(" ", "")
bracket_notation2 = convert_to_bracket_notation(expr2).replace(" ", "")

print(bracket_notation1)
print(bracket_notation2)

# Run the command on the terminal
import subprocess

command = (
    config.project_dir
    + "playground/egraphs/./ted string "
    + bracket_notation1
    + " "
    + bracket_notation2
)
subprocess.run(command, shell=True)
