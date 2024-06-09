import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generating the data
x1 = np.linspace(-5, 5, 100)
x1_transformed = np.vstack((x1**2, x1)).T
y_truth = (
    x1**2 + x1 - 1  # + np.random.normal(scale=0.5, size=x1.shape)
)  # Adding some noise

# Fitting linear regression on the transformed data
model = LinearRegression()
model.fit(x1_transformed, y_truth)
y_pred = model.predict(x1_transformed)

# Plotting the data and the linear regression fit in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Original data points
ax.scatter(
    x1_transformed[:, 0],
    x1_transformed[:, 1],
    y_truth,
    color="blue",
    label="Original data",
)

# Linear regression fit
ax.plot_trisurf(
    x1_transformed[:, 0],
    x1_transformed[:, 1],
    y_pred,
    color="red",
    alpha=0.5,
    label="Linear regression fit",
)

ax.set_xlabel(r"$x_1^2$")
ax.set_ylabel(r"$x_1$")
ax.set_zlabel(r"$y$")
ax.set_title("Linear Regression Fit on Transformed Data (x1^2, x1)")

plt.legend()
plt.show()
