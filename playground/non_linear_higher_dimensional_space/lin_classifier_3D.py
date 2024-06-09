import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Generate the data
np.random.seed(0)
x = np.linspace(0, 10, 100)
y = np.sqrt(x) + np.random.normal(scale=0.5, size=x.shape)  # Adding some noise
labels = (y**2 >= x).astype(int)  # Generate labels based on y^2 >= x

# Transform the data into a higher-dimensional space
x_transformed = np.vstack((x, y, y**2)).T

# Train a linear classifier
classifier = LogisticRegression()
classifier.fit(x_transformed, labels)

# Create a meshgrid for visualization
x0, x1 = np.meshgrid(np.linspace(0, 10, 100), np.linspace(0, 4, 100))
x2 = x1**2
X_grid = np.c_[x0.ravel(), x1.ravel(), x2.ravel()]

# Predict the labels for the meshgrid
y_pred = classifier.predict(X_grid).reshape(x0.shape)

# Plotting the data and the decision boundary in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Scatter plot of the original data points
ax.scatter(x, y, y**2, c=labels, cmap="bwr", edgecolor="k", label="Data points")

# Plot the decision boundary
ax.plot_surface(x0, x1, x2, facecolors=plt.cm.bwr(y_pred), alpha=0.3)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$y^2$")
ax.set_title("Linear Classifier in Transformed Space (x, y, y^2)")

plt.show()
