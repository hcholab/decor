# https://gplearn.readthedocs.io/en/stable/examples.html#example
import numpy as np
from sklearn.metrics import mean_squared_error
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

model = SymbolicRegressor(
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
    function_set=("add", "sub", "mul", "div"),
    n_jobs=-1,
)
model.fit(X_train, y_train)

print(model._program)

# 'add' : addition, arity=2.
# 'sub' : subtraction, arity=2.
# 'mul' : multiplication, arity=2.
# 'div' : protected division where a denominator near-zero returns 1., arity=2.
# 'sqrt' : protected square root where the absolute value of the argument is used, arity=1.
# 'log' : protected log where the absolute value of the argument is used and a near-zero argument returns 0., arity=1.
# 'abs' : absolute value, arity=1.
# 'neg' : negative, arity=1.
# 'inv' : protected inverse where a near-zero argument returns 0., arity=1.
# 'max' : maximum, arity=2.
# 'min' : minimum, arity=2.
# 'sin' : sine (radians), arity=1.
# 'cos' : cosine (radians), arity=1.
# 'tan' : tangent (radians), arity=1.
locals = {
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "mul": lambda x, y: x * y,
    "div": lambda x, y: x / y,
    "sqrt": lambda x: sympy.sqrt(x),
    "log": lambda x: sympy.log(x),
    "abs": lambda x: sympy.Abs(x),
    "neg": lambda x: -x,
    "inv": lambda x: 1 / x,
    "max": lambda x, y: sympy.Max(x, y),
    "min": lambda x, y: sympy.Min(x, y),
    "sin": lambda x: sympy.sin(x),
    "cos": lambda x: sympy.cos(x),
    "tan": lambda x: sympy.tan(x),
    "pow": lambda x, y: x**y,
}
print(model)

print(simplify(sympify(str(model._program), locals=locals).expand()))

mse = mean_squared_error(y_test, model.predict(X_test))
print("MSE:", mse)
