import numpy as np
import matplotlib.pyplot as plt
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error

# Generate some polynomial data
np.random.seed(0)
X = np.sort(5 * np.random.rand(100, 1), axis=0)
# y = 1 - 2 * X + X**2 + np.random.normal(0, 1, X.shape)
y = 1 - 2 * X + X**2

# Fit Kernel Ridge Regression model with a polynomial kernel
model = KernelRidge(kernel="polynomial", degree=2, alpha=1.0)
model.fit(X, y)

# Predict on the training data
y_pred = model.predict(X)

# Calculate the mean squared error
mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error: {mse}")

# print coefficients
for i in range(len(model.dual_coef_[0])):
    print(f"alpha_{i} = {model.dual_coef_[0][i]}")

print(f"coefficients = {model.dual_coef_}")


# Plot the results
plt.scatter(X, y, color="red", label="Data")
plt.plot(X, y_pred, color="blue", label="KRR Prediction")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Kernel Ridge Regression with Polynomial Kernel")
plt.legend()
plt.show()
