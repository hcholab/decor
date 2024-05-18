from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import numpy as np

model = Pipeline(
    [
        ("poly", PolynomialFeatures(degree=4)),
        ("linear", LinearRegression(fit_intercept=False)),
    ]
)
# fit to an order-3 polynomial data
x = np.arange(5)
print(x)


# Fit the model to an order-3 polynomial data
x = np.arange(5).reshape(-1, 1)
# Reshape x to a 2D array for compatibility with fit method
y = x**4 + 3 * x**3 + 5 * x**2 + 2 * x + 7
print(y)
y = y.flatten()  # Flattening y to ensure it is 1D
model.fit(x, y)

X_transformed = model.named_steps["poly"].transform(x)
print(X_transformed)

# Get the feature names
feature_names = model.named_steps["poly"].get_feature_names_out(input_features=["x"])

# Get the coefficients
coefficients = model.named_steps["linear"].coef_

# Create a dictionary mapping feature names to coefficients
coeff_dict = dict(zip(feature_names, coefficients))

# Print the dictionary
print(coeff_dict)
