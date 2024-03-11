import warnings
from joblib import Parallel, delayed  # noqa F401
import numpy as np
from sklearn.ensemble import RandomForestRegressor  # noqa F401
from sklearn.exceptions import ConvergenceWarning
from sklearn.svm import SVR  # noqa F401
from sklearn.tree import DecisionTreeRegressor  # noqa F401
import sympy as sp
from itertools import combinations_with_replacement
from sklearn.linear_model import (  # noqa F401
    ElasticNet,
    Ridge,
    Lasso,
    LinearRegression,
    SGDRegressor,
)
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
    # append ones column for the constant term to the extended data and a constant term to the extended terms
    extended_terms.append("1")
    extended_data = np.hstack((monomial_data, np.ones((data.shape[0], 1))))
    return extended_terms, extended_data


def find_models(extended_terms, extended_data, test_size=0.2):
    X = extended_data[:, :-1]  # Exclude the constant term
    models = {}

    def fit_model(target_idx):
        y = extended_data[:, target_idx]
        # Exclude the target variable from the features
        X_train, X_test, y_train, y_test = train_test_split(
            np.delete(X, target_idx, axis=1), y, test_size=test_size, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        score = model.score(X_test, y_test)

        # Insert 0 for the target variable's coefficient
        coefficients = model.coef_
        intercept = model.intercept_

        return (
            extended_terms[target_idx],
            model,
            score,
            coefficients,
            intercept,
            X_test,
            y_test,
        )

    # Create a model for each term in extended_terms, excluding the constant '1'
    results = Parallel(n_jobs=-1)(
        delayed(fit_model)(i) for i in range(len(extended_terms) - 1)
    )

    for term, model, score, coefficients, intercept, X_test, y_test in results:
        models[term] = {
            "model": model,
            "score": score,
            "coefficients": coefficients,
            "intercept": intercept,
            "X_test": X_test,
            "y_test": y_test,
        }

    return models


def find_best_model(extended_terms, extended_data, test_size=0.2):
    X = extended_data[:, :-1]  # Use all terms except the target variable itself
    models = {}

    # Define the models and parameters for grid search
    model_params = {
        "Linear Regression": {"model": LinearRegression(), "params": {}},
        "Ridge": {
            "model": Ridge(random_state=42),
            "params": {"alpha": [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]},
        },
        "Lasso": {
            "model": Lasso(random_state=42),
            "params": {"alpha": [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100]},
        },
    }

    for i in range(len(extended_terms) - 1):
        y = extended_data[:, i]
        X_train, X_test, y_train, y_test = train_test_split(
            np.delete(X, i, axis=1), y, test_size=test_size, random_state=42
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
            "X_test": X_test,
            "y_test": y_test,
        }

    return models


def infer_equation(models, extended_terms, threshold=0.4, coeff_cutoff=50, delta=0.2):
    str = ""
    for term, content in models.items():
        if np.abs(content["intercept"]) >= 100:
            # str += f"Model for {term}: Intercept = {content['intercept']}!\n"
            continue

        rhs = 0
        coeff_terms = {}

        # check all coefficients and if it is greater than 100, then skip it
        if np.any(np.abs(content["coefficients"]) >= coeff_cutoff):
            # str += f"Model for {term}: Large Coefficient!\n"
            continue

        for i, coefficient in enumerate(content["coefficients"]):
            if i != len(content["coefficients"]) - 1:  # Skip the constant term for now
                if abs(coefficient) >= threshold:
                    coeff = round(coefficient, 2)
                    if coeff != 0:
                        rhs += coeff * sp.symbols(extended_terms[i])
                        coeff_terms[extended_terms[i]] = coeff

        # Add the constant term (intercept)
        intercept = round(content["intercept"], 2)
        if intercept > threshold:
            rhs += intercept

        equation = sp.Eq(sp.symbols(term), rhs)
        # equation = sp.simplify(equation)
        str += f"Model for {term}: {equation}, "

        X_test = content["X_test"]
        y_test = content["y_test"]

        # Evaluate the equation for each row in X_test
        rhs_values = np.zeros(y_test.shape[0])
        for i, row in enumerate(X_test):
            for t, coeff in coeff_terms.items():
                rhs_values[i] += coeff * row[extended_terms.index(t)]
            if intercept > threshold:
                rhs_values[i] += intercept

        me = np.mean(np.abs(rhs_values - y_test))
        str += f"(error: {me}), "
        if me < delta:
            str += ">>>>>>>>>>>>>> good fit <<<<<<<<<<<<<<<<\n"
        else:
            str += "\n"

    return str


def load_input_data(file_path):
    with open(file_path, "r") as file:
        input_data = file.read()
    return input_data


if __name__ == "__main__":  # noqa E123

    file_path = "benchmarks/bitween/dig/bresenham.dig.dyn.traces"  # Path to your file
    # file_path = "benchmarks/bitween/dig/cohencu.dig.dyn.traces"  # Path to your file
    # file_path = "benchmarks/bitween/dig/cohendiv.dig.dyn.traces"  # Path to your file
    # file_path = "benchmarks/bitween/dig/dijkstra.dig.dyn.traces"  # Path to your file
    input_data = load_input_data(file_path)
    parsed_data = parse_dig_vtrace_file(input_data)

    str = ""
    for trace, content in parsed_data.items():
        terms = content["terms"]
        data = content["data"]

        str += f"\n{trace}\n"
        str += f"{terms}\n"

        extended_terms, extended_data = process_trace(terms, data, 2)

        str += f"{extended_terms}\n"

        # models = find_best_model(extended_terms, extended_data)
        models = find_models(extended_terms, extended_data)
        for term, content in models.items():
            str += f"Model for {term}: Score = {content['score']}, "
            if "model_type" in content:
                str += f"{content['model_type']}({content['params']})\n"
            else:
                str += "Linear Regression\n"

        str += "\n"

        # Exclude the original terms and constant term in the equation display
        str += infer_equation(models, extended_terms)

    print(str)
