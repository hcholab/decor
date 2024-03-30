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

y = x**4 + 3 * x**3 + 5 * x**2 + 2 * x + 7

data = x[:, np.newaxis]
print(data)

model = model.fit(x[:, np.newaxis], y)

# Get the coefficients from the linear model
coefficients = model.named_steps["linear"].coef_

# Get the feature names from PolynomialFeatures
feature_names = model.named_steps["poly"].get_feature_names_out(input_features=["x"])

# Map the coefficients with their corresponding feature names
coeff_dict = dict(zip(feature_names, np.round(coefficients, 2)))
print(coeff_dict)
