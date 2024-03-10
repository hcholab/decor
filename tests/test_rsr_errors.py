import math
import random
import statistics
import matplotlib.pyplot as plt


# property 1: f(x+y) = 2 f(x)*f(y) - f(x-y)
# property 2: f(x+y) = - f(x-y) + 2*f(y)*f(x) + 2*f(y)*f(y) + 2*f(x)*f(x) - 2*f(x-y)*f(x+y) - 2
def f(x):
    return math.cos(x)


values = []

z = random.random() * 100 - 50
z = -16.772695616821373

i = 10
while i > 0:
    x = z + random.random() * 1e-10
    y = z - x

    print(f"z = {z}, x = {x}, y = {y}")

    values.append((x, y))

    i -= 1

errors_1 = []
errors_2 = []

# compare the errors with a suitable metric
values.sort(key=lambda x: x[0] + x[1])

# result vectors
sc_1s = []
sc_2s = []
funcs = []
z_s = []
for x, y in values:
    z_s.append(f(z))
    funcs.append(f(x + y))
    self_corrector_1 = 2 * f(x) * f(y) - f(x - y)
    self_corrector_2 = (
        -f(x - y)
        + 2 * f(y) * f(x)
        + 2 * f(y) * f(y)
        + 2 * f(x) * f(x)
        - 2 * f(x - y) * f(x + y)
        - 2
    )
    sc_1s.append(self_corrector_1)
    sc_2s.append(self_corrector_2)

sc_1s.sort()
sc_2s.sort()
# print the median of result vectors
print(
    f"f(z) = {f(z)}; sc_1 = {statistics.median(sc_1s)}; sc_2 = {statistics.median(sc_2s)}"
)

exit()
plt.plot(z_s, "yo-", label="f(z)")
plt.plot(funcs, "ro-", label="f(x+(z-x))")
plt.plot(sc_1s, "bo-", label="self-corrector-1")
plt.plot(sc_2s, "go-", label="self-corrector-2")
plt.legend()
plt.show()
