import random
import functionList as fl

i = 100
while i > 0:
    x = random.random() * 1000 - 500
    y = random.random() * 1000 - 500

    f = fl.squareFunc

    # tl = f(x)*f(x+y)
    # tr = -1.0*f(y)*f(x+y) + 0.33*f(y)*f(x-y) + 0.67*f(y)*f(x) + -0.33*f(x)*f(x-y)  + -1.33

    tl = +0.5 * f(x + y) + 0.5 * f(x - y) + -1.0 * f(x)
    tr = 1

    if abs(tl - tr) > 0.001:
        print(tl - tr)
    i -= 1
