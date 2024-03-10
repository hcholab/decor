import ctypes
import math
import os
import random

pwd = os.path.dirname(os.path.abspath(__file__))
so_file = pwd + "/input_programs/functions.so"

functions = ctypes.CDLL(so_file)

square = functions.square
square.argtypes = [ctypes.c_int]
square.restype = ctypes.c_int

add = functions.add
add.argtypes = [ctypes.c_int, ctypes.c_int]
add.restype = ctypes.c_int

tan = functions.tan
tan.argtypes = [ctypes.c_double]
tan.restype = ctypes.c_double

tanf = functions.tanf
tanf.argtypes = [ctypes.c_float]
tanf.restype = ctypes.c_float

sin = functions.sin
sin.argtypes = [ctypes.c_double]
sin.restype = ctypes.c_double

sinf = functions.sinf
sinf.argtypes = [ctypes.c_float]
sinf.restype = ctypes.c_float

print("Running tests...")
print(f"square(5) = {square(5)}")
print(f"add(5, 6) = {add(5, 6)}")
print(f"tan(0.785398163) = {tan(0.785398163)}")
print(f"tanf(0.785398163) = {tanf(0.785398163)}")
print(f"sin(5) = {sin(5)}")
print(f"sinf(5) = {sinf(5)}")


def tan_py(x):
    return math.tan(x)


n = 5
for i in range(n):
    x = random.random() * 10 - 5
    print(f"tan   ({x}) = {tan(x)}")
    print(f"tan_py({x}) = {tan_py(x)}")
    print(f"tanf  ({x}) = {tanf(x)}")
    print("------------------------------------------")
