import ctypes
import math
import os
import random

pwd = os.path.dirname(os.path.abspath(__file__))
so_file = pwd + "/test_tracing.so"

functions = ctypes.CDLL(so_file)

test = functions.test
test.argtypes = [ctypes.c_int, ctypes.c_int]
test.restype = ctypes.c_int


print("Running tests...")
print(f"test(5, 6) = {test(5, 6)}")


def tan_py(x):
    return math.tan(x)


n = 30
for i in range(n):
    # x = random.random() * 10 - 5
    # y = random.random() * 10 - 5
    x = random.randint(-10, 10)
    y = random.randint(-10, 10)
    if x >= 1 or y >= 1:
        continue
    print(f"test({x}, {y}) = {test(x, y)}")
    print("------------------------------------------")
