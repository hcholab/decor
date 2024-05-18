import numpy as np
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.pipeline import Pipeline
from joblib import Parallel, delayed

# Example data
X = np.random.rand(100, 5)  # Feature matrix with 5 features
y = np.random.rand(100, 3)  # Target matrix with 3 different targets

# Dictionary of models and their parameter grids
models = {
    "Linear": {
        "model": LinearRegression(),
        "params": {"regressor__fit_intercept": [True, False]},
    },
    "Ridge": {
        "model": Ridge(random_state=42),
        "params": {"regressor__alpha": [1e-3, 1e-2, 1e-1, 100, 1000]},
    },
    "Lasso": {
        "model": Lasso(random_state=42),
        "params": {"regressor__alpha": [1e-4, 1e-3, 1e-2, 1e-1, 100, 1000]},
    },
}


# Function to perform GridSearchCV on a single target with a given model
def perform_grid_search(X, y, target_index, model_name, model, params):
    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y[:, target_index], test_size=0.2, random_state=42
    )

    # Setting up the pipeline
    pipeline = Pipeline([("regressor", model)])

    # GridSearchCV
    grid_search = GridSearchCV(pipeline, params, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    return (
        model_name,
        target_index,
        grid_search.best_estimator_,
        grid_search.best_params_,
    )


# Parallel execution for each model and target column
results = [
    Parallel(n_jobs=-1)(
        delayed(perform_grid_search)(
            X, y, i, model_name, model_info["model"], model_info["params"]
        )
        for model_name, model_info in models.items()
    )
    for i in range(y.shape[1])
]

# Processing results
for target_results in results:
    for model_name, target_index, model, params in target_results:
        print(f"Results for target column {target_index} with {model_name}:")
        print(f"Best model: {model}")
        print(f"Best parameters: {params}\n")
