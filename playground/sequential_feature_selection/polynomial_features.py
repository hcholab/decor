import numpy as np
from sklearn.preprocessing import PolynomialFeatures

# Assign names to the input features
feature_names = ["f(x)", "f(y)"]

# Your original data
X = np.arange(6).reshape(3, 2)
print("Original Data:\n", X)

# Initialize and fit PolynomialFeatures
poly = PolynomialFeatures(3)
X_poly = poly.fit_transform(X)

# Get the feature names for the polynomial features
poly_feature_names = poly.get_feature_names_out(input_features=feature_names)
print("Polynomial Features: ", poly_feature_names)
print("Transformed Polynomial Data:\n", X_poly)

# Initialize and fit PolynomialFeatures for interaction-only terms
poly_interaction = PolynomialFeatures(interaction_only=True)
X_interaction = poly_interaction.fit_transform(X)

# Get the feature names for interaction-only features
interaction_feature_names = poly_interaction.get_feature_names_out(
    input_features=feature_names
)
print("Interaction Features: ", interaction_feature_names)
print("Transformed Interaction Only Data:\n", X_interaction)
