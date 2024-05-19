# https://astroautomata.com/PySR/
import numpy as np  # noqa F401
from pysr import PySRRegressor
from sklearn.dummy import check_random_state
from sklearn.metrics import mean_squared_error
from sympy import simplify
from multiprocessing import cpu_count


rng = check_random_state(0)
# Training samples
X_train = rng.uniform(-1, 1, 100).reshape(50, 2)
y_train = X_train[:, 0] ** 2 - X_train[:, 1] ** 2 + X_train[:, 1] - 1

X_test = rng.uniform(-1, 1, 100).reshape(50, 2)
y_test = X_test[:, 0] ** 2 - X_test[:, 1] ** 2 + X_test[:, 1] - 1

model = PySRRegressor(
    niterations=100,  # < Increase me for better results
    binary_operators=["+", "*", "-"],
    # unary_operators=[
    #     "cos",
    #     "exp",
    #     "sin",
    #     "sqrt",
    #     "inv(x) = 1/x",
    #     # ^ Custom operator (julia syntax)
    # ],
    populations=max(15, cpu_count() * 2),
    timeout_in_seconds=2 * 60,
    # extra_sympy_mappings={"inv": lambda x: 1 / x},
    # ^ Define operator for SymPy as well
    # elementwise_loss="loss(prediction, target) = (prediction - target)^2",
    # ^ Custom loss function (julia syntax)
    select_k_features=10,
    # ^ Train on only the 4 most important features
)

# est = PySRRegressor(
#     niterations=1_000_000_000,
#     ncyclesperiteration=2_500,
#     population_size=100,
#     populations=max(15, cpu_count() * 2),
#     # budget 10 minutes for compile time,
#     # ensuring we can finish within 2 hours:
#     timeout_in_seconds=2 * 60 * 60 - 10 * 60,
#     maxsize=40,
#     maxdepth=20,
#     binary_operators=["+", "-", "*", "/"],
#     unary_operators=["sin", "exp", "log", "sqrt"],
#     constraints={
#         **dict(
#             sin=9,
#             exp=9,
#             log=9,
#             sqrt=9,
#         ),
#         **{"/": (-1, 9)},
#     },
#     nested_constraints=dict(
#         sin=dict(
#             sin=0,
#             exp=1,
#             log=1,
#             sqrt=1,
#         ),
#         exp=dict(
#             exp=0,
#             log=0,
#         ),
#         log=dict(
#             exp=0,
#             log=0,
#         ),
#         sqrt=dict(
#             sqrt=0,
#         ),
#     ),
#     # prefer multiprocessing:
#     procs=cpu_count(),
#     multithreading=False,
#     batching=True,
#     batch_size=50,
#     turbo=True,
#     weight_optimize=0.001,
#     adaptive_parsimony_scaling=1_000.0,
#     parsimony=0.0,
# )

model.fit(X_train, y_train)

print(model)

print(simplify(model.sympy().expand()))
print(model.feature_names_in_)
mse = mean_squared_error(y_test, model.predict(X_test))
