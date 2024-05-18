"""
===================================
Polynomial and Spline interpolation
===================================

This example demonstrates how to approximate a function with polynomials up to
degree ``degree`` by using ridge regression. We show two different ways given
``n_samples`` of 1d points ``x_i``:

- :class:`~sklearn.preprocessing.PolynomialFeatures` generates all monomials
  up to ``degree``. This gives us the so called Vandermonde matrix with
  ``n_samples`` rows and ``degree + 1`` columns::

    [[1, x_0, x_0 ** 2, x_0 ** 3, ..., x_0 ** degree],
     [1, x_1, x_1 ** 2, x_1 ** 3, ..., x_1 ** degree],
     ...]

  Intuitively, this matrix can be interpreted as a matrix of pseudo features
  (the points raised to some power). The matrix is akin to (but different from)
  the matrix induced by a polynomial kernel.

- :class:`~sklearn.preprocessing.SplineTransformer` generates B-spline basis
  functions. A basis function of a B-spline is a piece-wise polynomial function
  of degree ``degree`` that is non-zero only between ``degree+1`` consecutive
  knots. Given ``n_knots`` number of knots, this results in matrix of
  ``n_samples`` rows and ``n_knots + degree - 1`` columns::

    [[basis_1(x_0), basis_2(x_0), ...],
     [basis_1(x_1), basis_2(x_1), ...],
     ...]

This example shows that these two transformers are well suited to model
non-linear effects with a linear model, using a pipeline to add non-linear
features. Kernel methods extend this idea and can induce very high (even
infinite) dimensional feature spaces.

"""

# Author: Mathieu Blondel
#         Jake Vanderplas
#         Christian Lorentzen
#         Malte Londschien
# License: BSD 3 clause

import matplotlib.pyplot as plt
import numpy as np

# import seaborn as sns

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, SplineTransformer
from sklearn.metrics import mean_squared_error, r2_score
from kan import KAN
import torch

plt.rcParams.update({"font.size": 9})  # Set global font size to 10

# Configuration to use LaTeX, set font family and include extra packages
plt.rcParams["text.usetex"] = True
# plt.rcParams["font.family"] = "serif"
# plt.rcParams["font.serif"] = ["Computer Modern Roman"]
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

# plt.rcParams["axes.prop_cycle"] = plt.cycler(
#     color=plt.cm.viridis(np.linspace(0, 1, 10))
# )

# Set the palette to deep, a predefined palette in seaborn
# sns.set_palette("deep")

# Set Seaborn style and color palette
# sns.set_theme(context="paper", style="ticks", palette="pastel")


# We start by defining a function that we intend to approximate and prepare
# plotting it.


def f(x):
    """Function to be approximated by polynomial interpolation."""
    return x * np.sin(x)


# whole range we want to plot
x_plot = np.linspace(-1, 11, 100)

# To make it interesting, we only give a small subset of points to train on.

x_train = np.linspace(0, 10, 100)
rng = np.random.RandomState(0)
x_train = np.sort(rng.choice(x_train, size=20, replace=False))
y_train = f(x_train)

# Add 5 test points
x_test = np.linspace(0, 10, 5)
y_test = f(x_test)

sin_x = np.sin(x_train)
cos_x = np.cos(x_train)
x_train_bw = np.column_stack((x_train, sin_x, cos_x))

# create 2D-array versions of these arrays to feed to transformers
X_train = x_train[:, np.newaxis]
X_plot = x_plot[:, np.newaxis]
X_test = x_test[:, np.newaxis]

X_train_bw = x_train_bw
X_plot_bw = np.column_stack((x_plot, np.sin(x_plot), np.cos(x_plot)))
X_test_bw = np.column_stack((x_test, np.sin(x_test), np.cos(x_test)))


# Now we are ready to create polynomial features and splines, fit on the
# training points and show how well they interpolate.

lw = 2
fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(14, 8))
# Setting up the color cycle
colors = ["black", "teal", "yellowgreen", "gold", "darkorange", "tomato", "skyblue"]

# Ground truth and training points
for i in range(2):
    for j in range(2):
        axes[i][j].plot(
            x_plot,
            f(x_plot),
            linewidth=lw + 0.5,
            label=r"ground truth: $f(x) = x \sin(x)$",
            color="black",
        )
        axes[i][j].scatter(x_train, y_train, label="training points", color="black")
        axes[i][j].scatter(
            x_test,
            y_test,
            label="test points",
            edgecolors="red",
            facecolors="none",
            linewidth=1.5,
        )
        axes[i][j].axvline(
            x=0, linestyle="--", color="gray", lw=1, label="extrapolation limits"
        )
        axes[i][j].axvline(x=10, linestyle="--", color="gray", lw=1)

# 1st. plot function

# polynomial features
for degree in [1, 2, 3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), Ridge(alpha=1e-3))
    model.fit(X_train, y_train)
    feature_names = model.named_steps["polynomialfeatures"].get_feature_names_out(
        input_features=["x"]
    )
    print(feature_names)
    coefficients = model.named_steps["ridge"].coef_
    print(coefficients)
    y_plot = model.predict(X_plot)
    # mse = mean_squared_error(y_train, model.predict(X_train))
    mse = mean_squared_error(
        np.hstack([y_train, y_test]),
        np.hstack([model.predict(X_train), model.predict(X_test)]),
    )
    axes[0][0].plot(
        x_plot,
        y_plot,
        label=f"Polynomial Interpolation -- degree {degree} with "
        + r"$1, x$ -- "
        + f"MSE: {mse:.2f}",
    )

axes[0][0].set_title("Polynomial Interpolation")

# B-spline with 4 + 3 - 1 = 6 basis functions
# model = make_pipeline(SplineTransformer(n_knots=4, degree=3), Ridge(alpha=1e-3))
# model.fit(X_train, y_train)
# feature_names = model.named_steps["splinetransformer"].get_feature_names_out(
#     input_features=["x"]
# )
# print(feature_names)
# coefficients = model.named_steps["ridge"].coef_
# print(coefficients)

# y_plot = model.predict(X_plot)
# mse = mean_squared_error(y_train, model.predict(X_train))
# axes[0][0].plot(x_plot, y_plot, label=f"B-spline -- MSE: {mse:.2f}")


# 2nd. plot function

# BW's polynomial features including sin(x)
for degree in [1, 2, 3, 4, 5]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train_bw, y_train)
    feature_names = model.named_steps["polynomialfeatures"].get_feature_names_out(
        input_features=["x", "sin(x)", "cos(x)"]
    )
    print(feature_names)
    coefficients = model.named_steps["linearregression"].coef_
    print(coefficients)
    y_plot = model.predict(X_plot_bw)
    # mse = mean_squared_error(y_train, model.predict(X_train_bw))
    mse = mean_squared_error(
        np.hstack([y_train, y_test]),
        np.hstack([model.predict(X_train_bw), model.predict(X_test_bw)]),
    )
    axes[0][1].plot(
        x_plot,
        y_plot,
        label=f"Bitween's Inference -- degree {degree} with "
        + r"$1, x, \sin(x), \cos(x)$ -- "
        + f"MSE: {mse:.2f}",
    )

axes[0][1].set_title("Bitween's Inference")

# 3rd. plot function

# B-spline model
model = make_pipeline(SplineTransformer(n_knots=4, degree=3), Ridge(alpha=1e-3))
model.fit(X_train, y_train)
y_plot = model.predict(X_plot)
# mse = mean_squared_error(y_train, model.predict(X_train))
mse = mean_squared_error(
    np.hstack([y_train, y_test]),
    np.hstack([model.predict(X_train), model.predict(X_test)]),
)
axes[1][0].plot(
    x_plot,
    y_plot,
    label=f"B-spline Interpolation with Ridge regressor -- MSE: {mse:.2f}",
    color="yellowgreen",
)

# MLP Regressor
mlp_regressor = MLPRegressor(
    random_state=1, max_iter=10000, activation="tanh", solver="adam"
)
mlp_regressor.fit(X_train, y_train)
y_mlp = mlp_regressor.predict(X_plot)
# mlp_mse = mean_squared_error(y_train, mlp_regressor.predict(X_train))
mlp_mse = mean_squared_error(
    np.hstack([y_train, y_test]),
    np.hstack([mlp_regressor.predict(X_train), mlp_regressor.predict(X_test)]),
)
axes[1][0].plot(
    x_plot,
    y_mlp,
    label=f"Multi-layer Perceptron regressor (Neural Network) -- MSE: {mlp_mse:.2f}",
    color="blue",
)

# BW's polynomial features including sin(x)
for degree in [2, 3, 4]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train_bw, y_train)
    feature_names = model.named_steps["polynomialfeatures"].get_feature_names_out(
        input_features=["x", "sin(x)", "cos(x)"]
    )
    print(feature_names)
    coefficients = model.named_steps["linearregression"].coef_
    print(coefficients)
    y_plot = model.predict(X_plot_bw)
    mse = mean_squared_error(y_train, model.predict(X_train_bw))
    axes[1][0].plot(
        x_plot,
        y_plot,
        label=f"Bitween's Inference -- degree {degree} with "
        + r"$1, x, \sin(x), \cos(x)$ -- "
        + f"MSE: {mse:.2f}",
    )

axes[1][0].set_title("Spline Interpolation and MLP Regressor vs. Bitween's Inference")

# 4th plot function

# KAN Regressor
# Convert data to tensors for KAN
X_train_tensor = torch.tensor(x_train[:, None], dtype=torch.float32)  # Ensuring it's 2D
y_train_tensor = torch.tensor(y_train[:, None], dtype=torch.float32)  # 2D target tensor
X_plot_tensor = torch.tensor(x_plot[:, None], dtype=torch.float32)

X_test_tensor = torch.tensor(np.hstack([x_train, x_test])[:, None], dtype=torch.float32)
y_test_tensor = torch.tensor(
    f(np.hstack([x_train, x_test]))[:, None], dtype=torch.float32
)

# Creating hypothetical test labels (usually should be real test data)
y_test_tensor = torch.tensor(
    f(np.hstack([x_train, x_test]))[:, None], dtype=torch.float32
)

# Create dataset dictionary expected by KAN
my_ds = {
    "train_input": X_train_tensor,
    "train_label": y_train_tensor,
    "test_input": X_test_tensor,
    "test_label": y_test_tensor,  # Adding test labels
}

# Initialize and train KAN
kan_model = KAN(width=[1, 5, 1], grid=5, k=3, seed=0)
kan_model.train(my_ds, opt="LBFGS", steps=100, lamb=0.01, lamb_entropy=10.0)

# Get predictions from KAN
KAN_preds = kan_model(X_plot_tensor).detach().numpy()
# Calculate MSE for KAN
kan_mse = mean_squared_error(
    y_test_tensor.detach().numpy(), kan_model(X_test_tensor).detach().numpy()
)
print(f"KAN MSE: {kan_mse:.2f}")
kan_r2 = r2_score(
    y_test_tensor.detach().numpy(), kan_model(X_test_tensor).detach().numpy()
)
# Plotting KAN results
axes[1][1].plot(
    x_plot,
    KAN_preds,
    color="purple",
    label="KAN [1,5,1], LBFGS -- with symbolic library: "
    + r"$x, \sin(x)$ -- "
    + f"MSE: {kan_mse:.2f}",
)


# BW's polynomial features including sin(x)
for degree in [2, 3, 4]:
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X_train_bw, y_train)
    feature_names = model.named_steps["polynomialfeatures"].get_feature_names_out(
        input_features=["x", "sin(x)", "cos(x)"]
    )
    print(feature_names)
    coefficients = model.named_steps["linearregression"].coef_
    print(coefficients)
    y_plot = model.predict(X_plot_bw)
    mse = mean_squared_error(y_train, model.predict(X_train_bw))
    axes[1][1].plot(
        x_plot,
        y_plot,
        label=f"Bitween's Inference -- degree {degree} with "
        + r"$1, x, \sin(x), \cos(x)$ -- "
        + f"MSE: {mse:.2f}",
    )

axes[1][1].set_title("KAN Regressor vs. Bitween's Inference")

# Set legends and labels
for i in range(2):
    for j in range(2):
        axes[i][j].legend(loc="lower center")
        axes[i][j].set_ylim(-20, 10)

plt.tight_layout()
# Save the figure
plt.savefig("./figures/regression_methods.pdf")  # Saves as PNG file


# # kan_model.plot()
# kan_model = kan_model.prune()
# kan_model.train(my_ds, opt="LBFGS", steps=50)
# # kan_model.plot()
# lib = ["x", "x^2", "x^3", "sin"]  # Note that "cos" is not defined
# kan_model.auto_symbolic(lib=lib)
# kan_model.train(my_ds, opt="LBFGS", steps=50)
# print(kan_model.symbolic_formula()[0][0])
# # kan_model.plot()
plt.show()

exit()
# This shows nicely that higher degree polynomials can fit the data better. But
# at the same time, too high powers can show unwanted oscillatory behaviour
# and are particularly dangerous for extrapolation beyond the range of fitted
# data. This is an advantage of B-splines. They usually fit the data as well as
# polynomials and show very nice and smooth behaviour. They have also good
# options to control the extrapolation, which defaults to continue with a
# constant. Note that most often, you would rather increase the number of knots
# but keep ``degree=3``.
#
# In order to give more insights into the generated feature bases, we plot all
# columns of both transformers separately.

fig, axes = plt.subplots(ncols=2, figsize=(16, 5))
pft = PolynomialFeatures(degree=3).fit(X_train)
axes[0].plot(x_plot, pft.transform(X_plot))
axes[0].legend(axes[0].lines, [f"degree {n}" for n in range(4)])
axes[0].set_title("PolynomialFeatures")

splt = SplineTransformer(n_knots=4, degree=3).fit(X_train)
axes[1].plot(x_plot, splt.transform(X_plot))
axes[1].legend(axes[1].lines, [f"spline {n}" for n in range(6)])
axes[1].set_title("SplineTransformer")

# plot knots of spline
knots = splt.bsplines_[0].t
axes[1].vlines(knots[3:-3], ymin=0, ymax=0.8, linestyles="dashed")
plt.show()

# In the left plot, we recognize the lines corresponding to simple monomials
# from ``x**0`` to ``x**3``. In the right figure, we see the six B-spline
# basis functions of ``degree=3`` and also the four knot positions that were
# chosen during ``fit``. Note that there are ``degree`` number of additional
# knots each to the left and to the right of the fitted interval. These are
# there for technical reasons, so we refrain from showing them. Every basis
# function has local support and is continued as a constant beyond the fitted
# range. This extrapolating behaviour could be changed by the argument
# ``extrapolation``.

# Periodic Splines
# ----------------
# In the previous example we saw the limitations of polynomials and splines for
# extrapolation beyond the range of the training observations. In some
# settings, e.g. with seasonal effects, we expect a periodic continuation of
# the underlying signal. Such effects can be modelled using periodic splines,
# which have equal function value and equal derivatives at the first and last
# knot. In the following case we show how periodic splines provide a better fit
# both within and outside of the range of training data given the additional
# information of periodicity. The splines period is the distance between
# the first and last knot, which we specify manually.
#
# Periodic splines can also be useful for naturally periodic features (such as
# day of the year), as the smoothness at the boundary knots prevents a jump in
# the transformed values (e.g. from Dec 31st to Jan 1st). For such naturally
# periodic features or more generally features where the period is known, it is
# advised to explicitly pass this information to the `SplineTransformer` by
# setting the knots manually.


def g(x):
    """Function to be approximated by periodic spline interpolation."""
    return np.sin(x) - 0.7 * np.cos(x * 3)


y_train = g(x_train)

# Extend the test data into the future:
x_plot_ext = np.linspace(-1, 21, 200)
X_plot_ext = x_plot_ext[:, np.newaxis]

lw = 2
fig, ax = plt.subplots()
ax.set_prop_cycle(color=["black", "tomato", "teal"])
ax.plot(x_plot_ext, g(x_plot_ext), linewidth=lw, label="ground truth")
ax.scatter(x_train, y_train, label="training points")

for transformer, label in [
    (SplineTransformer(degree=3, n_knots=10), "spline"),
    (
        SplineTransformer(
            degree=3,
            knots=np.linspace(0, 2 * np.pi, 10)[:, None],
            extrapolation="periodic",
        ),
        "periodic spline",
    ),
]:
    model = make_pipeline(transformer, Ridge(alpha=1e-3))
    model.fit(X_train, y_train)
    y_plot_ext = model.predict(X_plot_ext)
    ax.plot(x_plot_ext, y_plot_ext, label=label)

ax.legend()
fig.show()

# We again plot the underlying splines.
fig, ax = plt.subplots()
knots = np.linspace(0, 2 * np.pi, 4)
splt = SplineTransformer(knots=knots[:, None], degree=3, extrapolation="periodic").fit(
    X_train
)
ax.plot(x_plot_ext, splt.transform(X_plot_ext))
ax.legend(ax.lines, [f"spline {n}" for n in range(3)])
plt.show()
