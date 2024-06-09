import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Generate random sample points for x and y as integers
np.random.seed(0)
x = np.random.randint(1, 100, 100)
y = np.random.randint(1, 10, 100)

# Calculate the features y^2 and x^2
y_squared = y**2
x_squared = x**2

# Generate labels based on y^2 < x
labels = (y_squared - x < 0).astype(int)

# Transform the data into the higher-dimensional space (x, y^2, x^2, y)
X_transformed = np.vstack((x, y_squared, x_squared, y)).T

# Train a linear classifier
classifier = LogisticRegression(fit_intercept=False)
classifier.fit(X_transformed, labels)

# Print coefficients and intercept
print("Coefficients:", classifier.coef_)
print("Intercept:", classifier.intercept_)
print("Coefficients and intercept in original space:")
print("x =", classifier.coef_[0][0])
print("y^2 =", classifier.coef_[0][1])
print("x^2 =", classifier.coef_[0][2])
print("y =", classifier.coef_[0][3])

# Create a meshgrid for visualization
x_min, x_max = x.min() - 1, x.max() + 1
y_min, y_max = y_squared.min() - 1, y_squared.max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

# Predict the labels for the meshgrid
Z = classifier.predict(
    np.c_[xx.ravel(), yy.ravel(), xx.ravel() ** 2, yy.ravel() ** 0.5]
).reshape(xx.shape)

# Plotting the data and the decision boundary in 2D
plt.figure(figsize=(8, 6))
plt.contourf(xx, yy, Z, alpha=0.3, cmap="bwr")

# Plot the points with different markers
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
            edgecolor="k",
            label="y^2 >= x" if i == 0 else "",
        )

# Adding text with coefficients and intercept
textstr = "\n".join(
    (
        r"$\mathbf{Classifier\ Coefficients:}$",
        r"$x = %.2f$" % (classifier.coef_[0][0],),
        r"$y^2 = %.2f$" % (classifier.coef_[0][1],),
        r"$x^2 = %.2f$" % (classifier.coef_[0][2],),
        r"$y = %.2f$" % (classifier.coef_[0][3],),
        r"$b = %.2f$" % (classifier.intercept_[0],),
    )
)

plt.xlabel(r"$x$")
plt.ylabel(r"$y^2$")
plt.title("Linear Classifier in Transformed Space (x, y^2)")
plt.legend(loc="upper right")

# Displaying the text box with coefficients and intercept
props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
plt.text(
    0.05,
    0.95,
    textstr,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=props,
)

plt.show()
