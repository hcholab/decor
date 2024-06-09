import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Generate random sample points for x and y as integers
np.random.seed(0)
x = np.random.randint(1, 2500, 100)
y = np.random.randint(1, 50, 100)

# Calculate the features y^2 and x^2
y_squared = y**2
x_squared = x**2

# Generate labels based on y^2 < x
labels = (y_squared < x).astype(int)

# Transform the data into the higher-dimensional space (x, y^2, x^2, y)
X_transformed = np.vstack((x, y_squared, x_squared, y)).T

# Train the first linear classifier with increased max_iter
# classifier = LogisticRegression(max_iter=1000)
classifier = LogisticRegression(max_iter=1000, fit_intercept=False)
classifier.fit(X_transformed, labels)

# Train the second linear classifier using only (x, y^2) with increased max_iter
X_transformed_simple = np.vstack((x, y_squared)).T
# classifier_simple = LogisticRegression(max_iter=1000)
classifier_simple = LogisticRegression(max_iter=1000, fit_intercept=False)
classifier_simple.fit(X_transformed_simple, labels)

# Print coefficients and intercept
print("Coefficients of full model:", classifier.coef_)
print("Intercept of full model:", classifier.intercept_)
print("Coefficients of simple model:", classifier_simple.coef_)
print("Intercept of simple model:", classifier_simple.intercept_)

# Create a meshgrid for visualization
x_min, x_max = x.min() - 1, x.max() + 1
y_min, y_max = y_squared.min() - 1, y_squared.max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

# Predict the labels for the meshgrid for both classifiers
Z_full = classifier.predict(
    np.c_[xx.ravel(), yy.ravel(), xx.ravel() ** 2, yy.ravel() ** 0.5]
).reshape(xx.shape)
Z_simple = classifier_simple.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

# Plotting the data and the decision boundaries in 2D
plt.figure(figsize=(12, 6))

# Plot the full model
plt.subplot(1, 2, 1)
plt.contourf(xx, yy, Z_full, alpha=0.3, cmap="bwr")
plt.scatter(x, y_squared, c=labels, cmap="bwr", edgecolor="k")

# Plot the points with different markers for the full model
for i in range(len(labels)):
    if labels[i] == 1:
        plt.scatter(
            x[i],
            y_squared[i],
            color="blue",
            marker="o",
            edgecolor="k",
            label="y^2 < x" if i == 0 else "",
        )
    else:
        plt.scatter(
            x[i],
            y_squared[i],
            color="red",
            marker="x",
            label="y^2 >= x" if i == 0 else "",
        )

plt.xlabel(r"$x$")
plt.ylabel(r"$y^2$")
plt.title("Full Model (x, y^2, x^2, y)")
plt.legend(loc="upper right")

# Plot the simple model
plt.subplot(1, 2, 2)
plt.contourf(xx, yy, Z_simple, alpha=0.3, cmap="bwr")
plt.scatter(x, y_squared, c=labels, cmap="bwr", edgecolor="k")

# Plot the points with different markers for the simple model
for i in range(len(labels)):
    if labels[i] == 1:
        plt.scatter(
            x[i],
            y_squared[i],
            color="blue",
            marker="o",
            edgecolor="k",
            label="y^2 < x" if i == 0 else "",
        )
    else:
        plt.scatter(
            x[i],
            y_squared[i],
            color="red",
            marker="x",
            label="y^2 >= x" if i == 0 else "",
        )

# Adding text with coefficients and intercept for the full model
textstr_full = "\n".join(
    (
        r"$\mathbf{Full\ Model\ Coefficients:}$",
        r"$x = %.2f$" % (classifier.coef_[0][0],),
        r"$y^2 = %.2f$" % (classifier.coef_[0][1],),
        r"$x^2 = %.2f$" % (classifier.coef_[0][2],),
        r"$y = %.2f$" % (classifier.coef_[0][3],),
        r"$b = %.2f$" % (classifier.intercept_[0],),
    )
)

# Adding text with coefficients and intercept for the simple model
textstr_simple = "\n".join(
    (
        r"$\mathbf{Simple\ Model\ Coefficients:}$",
        r"$x = %.2f$" % (classifier_simple.coef_[0][0],),
        r"$y^2 = %.2f$" % (classifier_simple.coef_[0][1],),
        r"$b = %.2f$" % (classifier_simple.intercept_[0],),
    )
)

plt.xlabel(r"$x$")
plt.ylabel(r"$y^2$")
plt.title("Simple Model (x, y^2)")
plt.legend(loc="upper right")

# Displaying the text box with coefficients and intercept for both models
props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

plt.subplot(1, 2, 1)
plt.text(
    0.05,
    0.95,
    textstr_full,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=props,
)

plt.subplot(1, 2, 2)
plt.text(
    0.05,
    0.95,
    textstr_simple,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=props,
)

plt.show()
