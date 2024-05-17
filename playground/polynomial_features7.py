from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SequentialFeatureSelector
import numpy as np

# Define the initial model with polynomial features and linear regression
model = Pipeline(
    [
        ("poly", PolynomialFeatures(degree=5)),
        ("linear", LinearRegression(fit_intercept=False)),
    ]
)

# Generate sample data
x = np.arange(100).reshape(-1, 1)
y = 6 * x**5 + 15 * x**4 + 10 * x**3 - 30 * x
z = np.arange(12, 112).reshape(-1, 1)
x = np.concatenate((x, z), axis=1)
y = y.flatten()  # Flattening y to ensure it is 1D


# split the data into train and test
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Fit the initial model to the data
model.fit(x_train, y_train)

# Transform the data with polynomial features
X_transformed = model.named_steps["poly"].transform(x_train)
# print dimensions of X_transformed
print(X_transformed.shape)

# Define the feature selector with a linear regression estimator
estimator = LinearRegression(fit_intercept=False)
selector = SequentialFeatureSelector(estimator, n_features_to_select=7, cv=5, n_jobs=-1)
selector.fit(X_transformed, y_train)

# Transform the data to select features
X_selected = selector.transform(X_transformed)

# Get selected feature names
feature_names = model.named_steps["poly"].get_feature_names_out(
    input_features=["x", "z"]
)
selected_features = feature_names[selector.get_support()]

# Fit a linear regression model on the selected features only
final_model = LinearRegression(fit_intercept=False)
final_model.fit(X_selected, y_train)

selected_features_coefficients = final_model.coef_
# Create a dictionary mapping selected feature names to coefficients
coeff_dict = dict(zip(selected_features, np.round(selected_features_coefficients, 4)))
# print the score of the final model
print(f"Score of the final model: {final_model.score(X_selected, y_train)}")

# Print the dictionary
for key, value in coeff_dict.items():
    print(f"{key}: {value}")

print("Test the model on unseen data")
# Transform the test data using the same polynomial transformation applied to the training data
X_test_transformed = model.named_steps["poly"].transform(x_test)

# Apply the same feature selection to the test data
X_test_selected = selector.transform(X_test_transformed)

# Predict the outcomes for the test data
y_pred = final_model.predict(X_test_selected)

# Calculate the mean squared error using the actual and predicted values
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error on Test Data: {mse}")
