from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SequentialFeatureSelector
import numpy as np


def pp(x):
    """
    Pretty print a number.
    """
    return np.format_float_positional(x, trim="-")


# Generate sample data
x = np.arange(150).reshape(-1, 1)
y = 6 * x**5 + 15 * x**4 + 10 * x**3 - 30 * x
# add correlated but irrelevant feature
z = np.arange(12, 162).reshape(-1, 1)
x = np.concatenate((x, z), axis=1)
y = y.flatten()

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42
)
print(f"x_train shape: {x_train.shape}")

# Define the range of features to select
current = np.inf
best_model = None
for n_features in range(1, 8):  # Will go from 7 to 4
    print(f"\nEvaluating model with {n_features} features selected:")

    # Define the feature selector with the current number of features
    selector = SequentialFeatureSelector(
        LinearRegression(fit_intercept=False),
        n_features_to_select=n_features,
        cv=3,
        # n_jobs=-1,
    )

    # Define the pipeline with the current feature selector
    model = Pipeline(
        [
            ("poly", PolynomialFeatures(degree=5)),
            ("selector", selector),
            ("linear", LinearRegression(fit_intercept=False)),
        ]
    )

    # Fit the pipeline to the training data
    model.fit(x_train, y_train)

    # Get the selected features and their coefficients
    selected_features = model.named_steps["poly"].get_feature_names_out(
        input_features=["x", "z"]
    )[model.named_steps["selector"].get_support()]
    coefficients = model.named_steps["linear"].coef_

    print("Selected features:", selected_features)

    # Construct the polynomial equation string
    equation = "y = "
    for feature, coeff in zip(selected_features, coefficients):
        coeff = round(coeff, 1)
        if feature == "1" and coeff != 0:
            equation += f"{coeff} + "
        elif coeff != 0:
            equation += f"{coeff}*{feature} + "
    equation = equation.rstrip(" + ")  # remove the last plus sign
    print(f"Equation: {equation}")

    # Predict and evaluate the model on the test set
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error on Test Data: {pp(mse)}")

    r2 = model.score(x_test, y_test)
    r2_ = r2_score(y_test, y_pred)
    print(f"Model R^2 Score on Test Data: {pp(r2_)}")
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error on Test Data: {pp(mae)}")

    if mae < current:
        current = mae
        best_model = model

    if mse < 1e-10:
        break

# Print the final model
print()
# Get the final selected features and their coefficients
selected_features = best_model.named_steps["poly"].get_feature_names_out(
    input_features=["x", "z"]
)[best_model.named_steps["selector"].get_support()]
coefficients = best_model.named_steps["linear"].coef_

print("Selected features:", selected_features, "(best model)")

# Construct the polynomial equation string
equation = "y = "
for feature, coeff in zip(selected_features, coefficients):
    coeff = round(coeff, 1)
    if feature == "1" and coeff != 0:
        equation += f"{coeff} + "
    elif coeff != 0:
        equation += f"{coeff}*{feature} + "
equation = equation.rstrip(" + ")  # remove the last plus sign
print(f"Equation: {equation}")
