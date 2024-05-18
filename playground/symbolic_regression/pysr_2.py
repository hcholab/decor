# https://astroautomata.com/PySR/
import numpy as np  # noqa F401
from pysr import PySRRegressor
from sklearn.dummy import check_random_state
from sympy import simplify


rng = check_random_state(0)
# Training samples
X_train = rng.uniform(-1, 1, 100).reshape(50, 2)
y_train = X_train[:, 0] ** 2 - X_train[:, 1] ** 2 + X_train[:, 1] - 1

model = PySRRegressor(
    niterations=40,  # < Increase me for better results
    binary_operators=["+", "*", "-"],
    # unary_operators=[
    #     "cos",
    #     "exp",
    #     "sin",
    #     "inv(x) = 1/x",
    #     # ^ Custom operator (julia syntax)
    # ],
    extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
    # select_k_features=10,
    # ^ Train on only the 4 most important features
)

model.fit(X_train, y_train)

print(model)

print(simplify(model.sympy().expand()))
