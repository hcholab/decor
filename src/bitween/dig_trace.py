import warnings
import numpy as np
from sklearn.exceptions import ConvergenceWarning
import sympy as sp
from itertools import combinations_with_replacement
from sklearn.linear_model import Ridge, Lasso, LinearRegression  # noqa F401
from sklearn.model_selection import GridSearchCV, train_test_split


def parse_dig_vtrace_file(input_data):
    # Splitting the input data into lines
    lines = input_data.strip().split("\n")

    # Dictionary to store the data and variable names for each trace type
    traces = {}

    # Processing each line
    for line in lines:
        parts = line.split("; ")
        trace_type = parts[0]
        values = parts[1:]

        # Handle header lines
        if "I " in values[0]:
            # Strip 'I ' from the names and store them as variable names
            traces[trace_type] = {"terms": [name[2:] for name in values], "data": []}
            continue

        # Check if the trace type is already initialized
        if trace_type not in traces:
            continue

        # Append the data to the respective list in the trace, converting to numeric types
        traces[trace_type]["data"].append(np.fromstring("; ".join(values), sep="; "))

    # Convert data lists to numpy arrays
    for trace in traces:
        traces[trace]["data"] = np.array(traces[trace]["data"])

    return traces


def generate_monomials(terms, degree):
    # Generate all combinations of terms up to the given degree
    monomials = []
    for d in range(1, degree + 1):
        for combo in combinations_with_replacement(terms, d):
            monomials.append("*".join(combo))
    return monomials


def calculate_monomial_data(terms, monomials, data):
    # Split each monomial and calculate its value for each row in the data
    monomial_values = np.ones((data.shape[0], len(monomials)))
    for i, monomial in enumerate(monomials):
        for term in monomial.split("*"):
            term_index = terms.index(term)
            monomial_values[:, i] *= data[:, term_index]
    return monomial_values


def process_trace(terms, data, degree):
    monomials = generate_monomials(terms, degree)
    extended_terms = terms + monomials[len(terms) :]
    monomial_data = calculate_monomial_data(terms, monomials, data)
    # extended_data = np.hstack((data, monomial_data))
    # append ones column for the constant term to the extended data and a constant term to the extended terms
    extended_terms.append("1")
    extended_data = np.hstack((monomial_data, np.ones((data.shape[0], 1))))
    return extended_terms, extended_data


# def find_models(extended_terms, extended_data):
#     X = extended_data[:, :-1]  # Use all terms except the target variable itself
#     models = {}

#     def fit_model(target_idx):
#         y = extended_data[:, target_idx]
#         # Exclude the target variable from the features
#         X_train, X_test, y_train, y_test = train_test_split(
#             np.delete(X, target_idx, axis=1), y, test_size=0.1, random_state=42
#         )

#         model = LinearRegression()
#         model.fit(X_train, y_train)

#         score = model.score(X_test, y_test)

#         # Insert 0 for the target variable's coefficient
#         coefficients = np.insert(model.coef_, target_idx, 0)
#         intercept = model.intercept_

#         return extended_terms[target_idx], model, score, coefficients, intercept

#     # Create a model for each term in extended_terms, excluding the constant '1'
#     results = Parallel(n_jobs=-1)(
#         delayed(fit_model)(i) for i in range(len(extended_terms) - 1)
#     )

#     for term, model, score, coefficients, intercept in results:
#         models[term] = {
#             "model": model,
#             "score": score,
#             "coefficients": coefficients,
#             "intercept": intercept,
#         }

#     return models


def find_best_model(extended_terms, extended_data):
    X = extended_data[:, :-1]  # Use all terms except the target variable itself
    models = {}

    # Define the models and parameters for grid search
    model_params = {
        "Linear Regression": {"model": LinearRegression(), "params": {}},
        # "Ridge": {
        #     "model": Ridge(random_state=42),
        #     "params": {"alpha": [1e-3, 1e-2, 1e-1, 1, 10, 100]},
        # },
        # "Lasso": {
        #     "model": Lasso(random_state=42),
        #     "params": {"alpha": [1e-3, 1e-2, 1e-1, 1, 10, 100]},
        # },
    }

    for i in range(len(extended_terms) - 1):
        y = extended_data[:, i]
        X_train, X_test, y_train, y_test = train_test_split(
            np.delete(X, i, axis=1), y, test_size=0.1, random_state=42
        )

        best_score = -np.inf
        best_model = None
        best_model_name = ""
        best_params = {}
        best_intercept = None
        best_coefficients = None

        for model_name, mp in model_params.items():
            clf = GridSearchCV(mp["model"], mp["params"], cv=5, scoring="r2", n_jobs=-1)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=ConvergenceWarning)
                clf.fit(X_train, y_train)
                if clf.best_score_ > best_score:
                    best_score = clf.best_score_
                    best_model = clf.best_estimator_
                    best_model_name = model_name
                    best_params = clf.best_params_
                    best_intercept = best_model.intercept_
                    best_coefficients = best_model.coef_

        models[extended_terms[i]] = {
            "model": best_model,
            "score": best_score,
            "model_type": best_model_name,
            "params": best_params,
            "intercept": best_intercept,
            "coefficients": best_coefficients,
        }

    return models, X_test, y_test


def display_equations(models, extended_terms, X_test, y_test, threshold=0.4):
    for term, content in models.items():
        if np.abs(content["intercept"]) >= 100:
            print(f"Model for {term}: Intercept = {content['intercept']}")
            continue

        # Construct the rhs of the equation
        rhs = 0
        rhs_terms_indices = {}
        for i, coefficient in enumerate(content["coefficients"]):
            if i != len(content["coefficients"]) - 1:  # Skip the constant term for now
                if abs(coefficient) >= threshold:
                    coeff = round(coefficient, 2)
                    if coeff != 0:
                        rhs += coeff * sp.symbols(extended_terms[i])
                        rhs_terms_indices[extended_terms[i]] = i

        # Add the constant term (intercept)
        intercept = round(content["intercept"], 2)
        if intercept:
            rhs += intercept

        # Display the equation
        equation = sp.Eq(sp.symbols(term), rhs)
        print(f"Model for {term}: {equation}")

        # Evaluate the equation for each row in X_test
        rhs_values = np.zeros(y_test.shape[0])
        for term_name, index in rhs_terms_indices.items():
            rhs_values += X_test[:, index] * content["coefficients"][index]
        rhs_values += intercept

        # Assuming y_test is for the current term only
        actual_values = y_test

        # Compute Mean Squared Error as a fitness score
        mse = np.mean((rhs_values - actual_values) ** 2)
        print(f"Mean Squared Error for {term}: {mse}\n")


def display_equations_1(models, extended_terms, threshold=0.4):
    for term, content in models.items():
        if np.abs(content["intercept"]) >= 100:
            print(f"Model for {term}: Intercept = {content['intercept']}")
            continue
        rhs = 0
        for i, coefficient in enumerate(content["coefficients"]):
            if i != len(content["coefficients"]) - 1:  # Skip the constant term for now
                if abs(coefficient) >= threshold:
                    coeff = round(coefficient, 2)
                    if coeff != 0:
                        rhs += coeff * sp.symbols(extended_terms[i])

        # Add the constant term (intercept)
        intercept = round(content["intercept"], 2)
        if intercept:
            rhs += intercept

        equation = sp.Eq(sp.symbols(term), rhs)
        print(f"Model for {term}: {equation}")


def load_input_data(file_path):
    with open(file_path, "r") as file:
        input_data = file.read()
    return input_data


if __name__ == "__main__":  # noqa E123
    # Example usage
    input_data = """
vtrace1; I X; I Y; I x; I y; I v
vtrace1; 298; 288; 150; 145; 258
vtrace1; 295; 15; 189; 10; -495
vtrace1; 274; 276; 174; 174; 974
vtrace1; 274; 289; 106; 106; 3484
vtrace1; 293; 14; 70; 3; -63
vtrace1; 274; 276; 212; 212; 1126
vtrace1; 16; 25; 4; 4; 106
vtrace1; 271; 12; 5; 0; -127
vtrace1; 289; 24; 2; 0; -145
vtrace2; I X; I Y; I x; I y; I v
vtrace2; 287; 13; 288; 13; -235
vtrace2; 2; 294; 3; 3; 2338
vtrace2; 1; 274; 2; 2; 1639
vtrace2; 4; 13; 5; 5; 112
vtrace2; 284; 8; 285; 8; -252
vtrace2; 7; 13; 8; 8; 115
vtrace2; 297; 9; 298; 9; -261
vtrace2; 19; 6; 20; 6; 5
vtrace2; 270; 29; 271; 29; -154
vtrace2; 3; 287; 4; 4; 2843
vtrace2; 3; 11; 4; 4; 83
vtrace2; 4; 10; 5; 5; 76
vtrace2; 295; 11; 296; 11; -251
"""

    file_path = "bresenham.dig.dyn.traces"  # Path to your file
    input_data = load_input_data(file_path)
    parsed_data = parse_dig_vtrace_file(input_data)
    # print(parsed_data)

    for trace, content in parsed_data.items():
        terms = content["terms"]
        data = content["data"]
        print(f"{trace}")
        print(f"{terms}")
        # print(f"{data}\n")

        extended_terms, extended_data = process_trace(terms, data, 2)

        print(f"{extended_terms}")
        # print(f"{extended_data}\n")

        models, X_test, y_test = find_best_model(extended_terms, extended_data)
        for term, content in models.items():
            print(f"Model for {term}: Score = {content['score']}", end=", ")
            print(f"Model type = {content['model_type']}, Params = {content['params']}")

        print("\n")

        # Exclude the original terms and constant term in the equation display
        display_equations(models, extended_terms, X_test, y_test, threshold=0.4)
