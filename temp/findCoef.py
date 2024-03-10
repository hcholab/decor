import random
from rsr_property_generation import utilities as ut
from rsr_property_generation import runLinReg as rlg
from rsr_property_generation import functionList as fl

if __name__ == "__main__":
    # functions = fl.functions

    # functions = [fl.sinTaylor]
    # functions = [fl.sinSimpleFunc]
    # functions = [fl.squareFunc]
    # functions = [fl.cotFunc]
    functions = [fl.cosSimpleFunc]

    # f(x+y)*f(x-y) = 2*f(x)*f(x)
    # (-f(x-y) + 2*f(x) + 2*f(y))*f(x-y) = 2*f(x)*f(x)

    minDegree = 1
    maxDegree = 3

    i = 100
    while i > 0:
        x = random.random() * 1000 - 500
        y = random.random() * 1000 - 500

        # f = fl.squareFunc
        f = fl.cosSimpleFunc

        # tl = f(x)*f(x+y)
        # tr = -1.0*f(y)*f(x+y) + 0.33*f(y)*f(x-y) + 0.67*f(y)*f(x) + -0.33*f(x)*f(x-y)  + -1.33

        # tl = f(x-y)*f(x-y) - 2*f(x)*f(x-y) - 2*f(y)*f(x-y) -f(x-y)*2*f(x) + 2*f(x)*2*f(x) + 2*f(y)*2*f(x) -f(x-y)*2*f(y) + 2*f(x)*2*f(y) + 2*f(y)*2*f(y) + 2*f(x-y)*f(x-y) - 4*f(x)*f(x-y) - 4*f(y)*f(x-y) + f(x-y)*f(x-y)
        # tl = f(x) * f(x)
        # tr = (
        #     2 * f(x) * f(y)
        #     - f(y) * f(y)
        #     - f(x - y) * f(x - y)
        #     + 2 * f(x) * f(x - y)
        #     + 2 * f(y) * f(x - y)
        # )

        tr = f(y)
        tl = (
            -2.0 * f(x - y)
            + 2.0 * f(y) * f(y) * f(x - y)
            + 1.0 * f(y) * f(y) * f(y)
            + 1.0 * f(y) * f(x) * f(x)
            + 1.0 * f(y) * f(x - y) * f(x - y)
            + 2.0 * f(x) * f(x) * f(x - y)
            + 2.0 * f(x - y) * f(x - y) * f(x - y)
            + -2.0 * f(y) * f(y) * f(x) * f(x - y)
            + -4.0 * f(y) * f(x) * f(x - y) * f(x - y)
        )

        if abs(tl - tr) > 0.001:
            print(tl - tr)
        i -= 1

    # exit()

    for f in functions:
        ut.printt(f.__name__, 2)
        for d in range(minDegree - 1, maxDegree):
            ut.printt(
                "checking degree " + str(d + 1) + " for function " + str(f.__name__), 1
            )
            # (successful, result) = rlg.run(f, d + 1, 0, ["f(x+y)"], 1000)
            # (successful, result) = rlg.run(f, d + 1, 0, ["f(x+y)", "f(y)*f(y)"], 200)
            (successful, result) = rlg.run(f, d + 1, 0, [], 1000)
            # (successfulm, resultm) = rlg.run(f, d+1, 0, ["f(x-y)"], 1000)
            # ut.printt(result+resultm, 2)
            # successful = run(f, d+1, ["f(x+y)"])

            # print("successful: " + str(successful))
            # if (len(successful) > 0):
            #     run(f, d+1, successful)

            ut.printt("\n\n------------------------------------------\n\n\n\n\n\n", 0)

    exit()
