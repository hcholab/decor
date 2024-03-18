import collections
import itertools
import warnings
from joblib import Parallel, delayed  # noqa F401
import numpy as np
from sklearn.exceptions import ConvergenceWarning
import sympy
from sklearn.linear_model import (  # noqa F401
    ElasticNet,
    Ridge,
    Lasso,
    LinearRegression,
    SGDRegressor,
)
from sklearn.model_selection import GridSearchCV, train_test_split

from bitween import settings, miscs
from bitween.miscs import Symbolic
from bitween.z3utils import Z3

sympy.init_printing(use_unicode=False, wrap_line=False)

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def load_input_data(file_path):
    with open(file_path, "r") as file:
        input_data = file.read()
    return input_data


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
        for combo in itertools.combinations_with_replacement(terms, d):
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


def find_model(pivot, terms, data, test_size=0.2):
    X = data
    y = data[:, terms.index(pivot)]

    X_train, X_test, y_train, y_test = train_test_split(
        np.delete(data, terms.index(pivot), axis=1),
        y,
        test_size=test_size,
        random_state=42,
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    coefficients = model.coef_
    intercept = model.intercept_
    return pivot, {
        "model": model,
        "score": score,
        "coefficients": coefficients,
        "intercept": intercept,
        # "X_test": X_test,
        # "y_test": y_test,
        "X_test": X,  # Include the entire X for evaluating the equation
        "y_test": y,  # Include the entire y for evaluating the equation
    }


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
            # X_test,
            # y_test,
            X,  # Include the entire X for evaluating the equation
            y,  # Include the entire y for evaluating the equation
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
            "params": {"alpha": [1e-3, 1e-2, 1e-1, 1, 100, 1000]},
        },
        "Lasso": {
            "model": Lasso(random_state=42),
            "params": {"alpha": [1e-3, 1e-2, 1e-1, 1, 10, 100]},
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
        cv = settings.CROSS_VALIDATION
        for model_name, mp in model_params.items():
            clf = GridSearchCV(
                mp["model"], mp["params"], cv=cv, scoring="r2", n_jobs=-1
            )
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
            # "X_test": X_test,
            # "y_test": y_test,
            "X_test": X,  # NOTE: Include the entire X for evaluating the equation
            "y_test": y,  # NOTE: Include the entire y for evaluating the equation
        }

    return models


def infer_equations(
    models,
    extended_terms,
    extended_data,
    coeff_threshold=settings.COEFF_THRESHOLD,
    coeff_cutoff=settings.COEFF_CUTOFF,
    intercept_cutoff=settings.INTERCEPT_CUTOFF,
    delta=settings.DELTA,
):

    def infer_equation(pivot, model, extended_terms, extended_data, note):
        str = ""

        # NOTE: preparing an equation from the regression model
        if np.abs(model["intercept"]) >= intercept_cutoff:
            # str += f"Model for {term}: Intercept = {content['intercept']}!\n"
            return None

        rhs = sympy.Rational(0)
        coeff_terms = {}
        selected_terms = [pivot]  # Include LHS term
        terms = [item for item in extended_terms if item != pivot]

        # check all coefficients and if it is greater than 100, then skip it
        if np.any(np.abs(model["coefficients"]) >= coeff_cutoff):
            # str += f"Model for {term}: Large Coefficient!\n"
            return None

        for i, coefficient in enumerate(model["coefficients"]):
            if abs(coefficient) >= coeff_threshold:
                coeff = round(coefficient, 2)
                if coeff != 0:
                    rhs += sympy.Rational(coeff) * sympy.symbols(terms[i])
                    coeff_terms[terms[i]] = coeff
                    # Include term in selected list
                    selected_terms.append(terms[i])

        # Add the constant term (intercept)
        intercept = round(model["intercept"], 2)
        if intercept > coeff_threshold:
            rhs += sympy.Rational(intercept)

        equation = sympy.symbols(pivot) - rhs
        # equation = sp.simplify(equation)
        str += f"Model for {pivot}: {equation.evalf()} = 0, "

        X_test = model["X_test"]
        y_test = model["y_test"]

        # NOTE: Property Test: Evaluate the equation for each row in X_test
        rhs_values = np.zeros(y_test.shape[0])
        for i, row in enumerate(X_test):
            for t, coeff in coeff_terms.items():
                rhs_values[i] += coeff * row[extended_terms.index(t)]
            if intercept > coeff_threshold:
                rhs_values[i] += intercept

        me = np.mean(np.abs(rhs_values - y_test))
        str += f"(error: {round(me, 2)}), ({note}), "
        if me < delta:
            str += ">>>>>>>>>>>>>> good fit <<<<<<<<<<<<<<<<\n"
        else:
            str += "\n"

        if settings.MILP is not True and settings.REGRESSION_REFINEMENT is not True:
            return str, equation, me, None, None

        # NOTE: MILP Synthesis based on the regression model
        # Selecting respective columns from data
        selected_indices = [extended_terms.index(term) for term in selected_terms]
        selected_data = extended_data[:, selected_indices]

        print(f"Model for {pivot}: {equation.evalf()}")
        print(equation.evalf())
        print(selected_terms)
        print(selected_data)

        return (str, equation, me, selected_terms, selected_data)

    results = []
    for pivot, model in models.items():
        result = infer_equation(pivot, model, extended_terms, extended_data, "initial")
        if result is not None:
            results.append(result[0:3])
            term = result[3]
            data = result[4]

            # NOTE: start Regression Refinement
            if settings.REGRESSION_REFINEMENT and len(term) > 1:
                pivot_, model_ = find_model(pivot, term, data)
                result = infer_equation(pivot_, model_, term, data, "refined")
                if result is not None:
                    results.append(result[0:3])

    if settings.MILP is not True:
        return results


if __name__ == "__main__":  # noqa E123

    file_path = settings.FILE_PATH
    input_data = load_input_data(file_path)
    trace_data = parse_dig_vtrace_file(input_data)

    str = ""
    results = collections.defaultdict(list)
    for loc, data in trace_data.items():
        terms = data["terms"]
        data = data["data"]

        str += f"\nLocation: {loc}\n"
        str += f"Terms: {terms}\n"
        str += f"Shape: {data.shape}\n"

        for degree in range(1, settings.DEGREE + 1):
            str += f"\nDegree: {degree}\n"
            extended_terms, extended_data = process_trace(terms, data, degree)

            str += f"{extended_terms}\n"

            if settings.MULTIPLE_REGRESSION:
                # (Option 1) use cross validation to find the best model for each term
                models = find_best_model(extended_terms, extended_data)
            else:
                # (Option 2) use simple linear regression to find a model for each term
                models = find_models(extended_terms, extended_data)

            # Display the models and their equations
            for term, content in models.items():
                str += f"Model for {term}: Score = {content['score']}, "
                if "model_type" in content:
                    str += f"{content['model_type']}({content['params']})\n"
                else:
                    str += "Linear Regression\n"

            str += "\n"

            result = infer_equations(models, extended_terms, extended_data)
            results[loc].extend(result)
            for r in result:
                str += r[0]

    print(str)

    print("\nInferred Equalities:")
    for loc, result in results.items():
        print(f"\nTrace: {loc}")

        good_fit = set()
        for r in result:
            if r[2] < settings.DELTA:
                print(f"{r[1]} = 0 (error: {round(r[2], 3)})")
                good_fit.add(sympy.simplify(r[1]))

        print("\nReduced Equalities:")
        equations = Symbolic.refine(good_fit)

        for eq in equations:
            print(f"{eq} = 0")

        if settings.SLOW_SIMPLIFY:
            equations = Z3._simplify_slow(equations, [], loc)
            for r in equations:
                print(r)

        if settings.CONSISTENCY_CHECK:
            print("\nChecking Consistency of Equations:")

            try:
                print(f"1. Solve algebraically: {sympy.solve(equations)}")
            except NotImplementedError:
                print("1. Solve algebraically: Could not solve")

            print("2. Check satisfiability: ", end="")
            sat, r = Z3.check_sat(equations)
            print(f"{sat}, {r}")
