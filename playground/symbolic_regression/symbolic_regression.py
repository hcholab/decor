import random
import numpy

if __name__ == "__main__":
    # Upload a .csv file where each row is of the form [x_0, x_1, ..., x_d, y].
    # Example for f(x0,x1)=x0+x1:
    a = numpy.asarray([[1, 1, 2], [-1, 1, 0], [2, 3, 5]])
    numpy.savetxt("data1.csv", a, delimiter=",")

    def f(x0, x1):
        return x0**2 + 4 * x1**2

    n = 100

    array = []

    for i in range(n):
        x = random.random()
        y = random.random()
        # generate a random uniform integer
        c = random.random()
        tuple = (x, y, c, f(x, y))
        array.append(tuple)

    numpy.savetxt("data.csv", array, delimiter=",")
