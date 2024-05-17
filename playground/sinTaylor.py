import functionList as fl
import math
import random

m = 30

for n in range(1000):
    r = random.random() * 2 * m - m
    d = fl.sinTaylor(r) - math.sin(r)
    print(d)
    if d > 0.001:
        print(
            f"for the value {r} the error is {d}, since taylor gives {fl.sinTaylor(r)} and library gives {math.sin(r)}"
        )
        print("fff")
