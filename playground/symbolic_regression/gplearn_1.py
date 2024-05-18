# https://gplearn.readthedocs.io/en/stable/examples.html#example
import numpy as np
import sympy
from sympy import sympify, simplify
import matplotlib.pyplot as plt
from sklearn.dummy import check_random_state
from gplearn.genetic import SymbolicRegressor

x0 = np.arange(-1, 1, 1 / 10.0)
x1 = np.arange(-1, 1, 1 / 10.0)
x0, x1 = np.meshgrid(x0, x1)
y_truth = x0**2 - x1**2 + x1 - 1

ax = plt.figure().add_subplot(projection="3d")
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
surf = ax.plot_surface(x0, x1, y_truth, rstride=1, cstride=1, color="green", alpha=0.5)
# plt.show()

rng = check_random_state(0)

# Training samples
X_train = rng.uniform(-1, 1, 100).reshape(50, 2)
y_train = X_train[:, 0] ** 2 - X_train[:, 1] ** 2 + X_train[:, 1] - 1

# Testing samples
X_test = rng.uniform(-1, 1, 100).reshape(50, 2)
y_test = X_test[:, 0] ** 2 - X_test[:, 1] ** 2 + X_test[:, 1] - 1

est_gp = SymbolicRegressor(
    population_size=5000,
    generations=20,
    stopping_criteria=0.01,
    p_crossover=0.7,
    p_subtree_mutation=0.1,
    p_hoist_mutation=0.05,
    p_point_mutation=0.1,
    max_samples=0.9,
    verbose=1,
    parsimony_coefficient=0.01,
    random_state=0,
    feature_names=["x0", "x1"],
)
est_gp.fit(X_train, y_train)

print(est_gp._program)

locals = {
    "sub": lambda x, y: x - y,
    "div": lambda x, y: x / y,
    "mul": lambda x, y: x * y,
    "add": lambda x, y: x + y,
    "neg": lambda x: -x,
    "pow": lambda x, y: x**y,
    "cos": lambda x: sympy.cos(x),
    "sin": lambda x: sympy.sin(x),
}

print(simplify(sympify(str(est_gp._program), locals=locals).expand()))
