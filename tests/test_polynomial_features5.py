from sklearn.ensemble import (  # noqa F401
    GradientBoostingClassifier,
    RandomForestRegressor,
)
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import (  # noqa F401
    RFECV,
    SelectFromModel,
    SelectKBest,
    VarianceThreshold,
    f_regression,
)
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor  # noqa F401
import numpy as np

# Define the model
model = Pipeline(
    [
        ("poly", PolynomialFeatures(degree=5)),
        ("linear", LinearRegression(fit_intercept=False)),
    ]
)

# Generate sample data
x = np.arange(150).reshape(-1, 1)
y = 6 * x**5 + 15 * x**4 + 10 * x**3 - 30 * x
z = np.arange(12, 162).reshape(-1, 1)
x = np.concatenate((x, z), axis=1)
print(x)
y = y.flatten()  # Flattening y to ensure it is 1D

# Fit the model to the data
model.fit(x, y)

# Transform the data
X_transformed = model.named_steps["poly"].transform(x)

# Initialize RFECV
# estimator = model.named_steps["linear"]
estimator = LinearRegression(fit_intercept=False)
# selector = RFECV(estimator, step=1, cv=5, scoring="neg_mean_squared_error")
selector = RFECV(
    estimator=estimator,
    step=1,
    cv=KFold(5),
    scoring="neg_mean_absolute_error",
)
# selector = VarianceThreshold()
# selector = SelectKBest(f_regression, k=5)
# Fit RFECV
X_new = selector.fit_transform(X_transformed, y)

# Print the optimal number of features
# print("Optimal number of features: %d" % selector.n_features_)

# Apply the feature selection to the data
# X_transformed_selected = selector.transform(X_transformed)

# print(f"selector ranking: {selector.ranking_}")

# Get selected feature names
feature_names = np.array(
    model.named_steps["poly"].get_feature_names_out(input_features=["x", "z"])
)
selected_features = feature_names[selector.get_support()]
print(f"Selected features: {selected_features}")

# Get coefficients (Note: These coefficients are from the full model, not the reduced one)
coefficients = model.named_steps["linear"].coef_

# Create a dictionary mapping feature names to coefficients for selected features
coeff_dict = dict(
    zip(selected_features, np.round(coefficients[selector.get_support()], 4))
)

# Print the dictionary
for key, value in coeff_dict.items():
    print(key, ":", value)

print()
coeff_dict = dict(zip(feature_names, np.round(coefficients, 4)))

for key, value in coeff_dict.items():
    print(key, ":", value)
