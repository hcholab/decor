import ctypes
import os

pwd = os.path.dirname(os.path.abspath(__file__))
so_file = pwd + "/input_programs/quake.so"

functions = ctypes.CDLL(so_file)

invsqrt = functions.invsqrt
invsqrt.argtypes = [ctypes.c_float]
invsqrt.restype = ctypes.c_float

print("Running tests...")
print(f"square(1/4) = {invsqrt(1/4)}")
