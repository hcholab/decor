import collections
from dataclasses import dataclass
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
from bitween import milp, milp_pulp
from bitween.miscs import Symbolic
from bitween.z3utils import Z3

sympy.init_printing(use_unicode=False, wrap_line=False)

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


@dataclass(frozen=True)
class Equation:
    expr: sympy.Expr
    error: float
    pivot: str
    sample_size: int
    model_desc: str
    note: str


@dataclass(frozen=True)
class Model:
    model: object
    score: float
    model_type: str
    params: dict
    coefficients: np.ndarray
    intercept: float
    X_test: np.ndarray
    y_test: np.ndarray


def load_input_data(file_path):
    with open(file_path, "r") as file:
        input_data = file.read()
    return input_data


def parse_dig_vtrace_file(input_data) -> dict:
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
        # traces[trace]["data"].setflags(write=False)

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
    sample_size = X_train.shape[0]

    return pivot, {
        "model": model,
        "score": score,
        "model_type": "Linear",
        "params": "",  # NOTE: No parameters for simple linear regression
        "coefficients": coefficients,
        "intercept": intercept,
        "sample_size": sample_size,
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

    sample_size = int(extended_data.shape[0] * (1 - test_size))
    for term, model, score, coefficients, intercept, X_test, y_test in results:
        models[term] = {
            "model": model,
            "score": score,
            "model_type": "Linear",
            "params": "",  # NOTE: No parameters for simple linear regression
            "coefficients": coefficients,
            "intercept": intercept,
            "sample_size": sample_size,
            "X_test": X_test,
            "y_test": y_test,
        }

    return models


def find_best_model(extended_terms, extended_data, test_size=0.2):
    X_ = extended_data[:, :-1]  # Use all terms except the target variable itself

    # Define the models and parameters for grid search
    model_params = {
        "Linear": {"model": LinearRegression(), "params": {}},
        "Ridge": {
            "model": Ridge(random_state=42),
            "params": {"alpha": [1e-3, 1e-2, 1e-1, 100, 1000]},
        },
        "Lasso": {
            "model": Lasso(random_state=42),
            "params": {"alpha": [1e-3, 1e-2, 1e-1, 10, 100]},
        },
    }

    sample_size = extended_data.shape[0]

    if settings.REGRESSION_USE_SAMPLE_RATE and settings.REGRESSION_SAMPLE_RATE > 1:
        # select a random subset of the extended_data based on the number of terms * sample rate
        sample_size = int(len(extended_terms) * settings.REGRESSION_SAMPLE_RATE)
        threshold = settings.REGRESSION_SAMPLE_THRESHOLD
        if sample_size < threshold:
            if extended_data.shape[0] > threshold:
                sample_size = threshold
            else:  # use all data
                sample_size = extended_data.shape[0]

        if sample_size < extended_data.shape[0]:
            sample_indices = np.random.choice(
                extended_data.shape[0], sample_size, replace=False
            )
            extended_data = extended_data[sample_indices]
        else:
            sample_size = extended_data.shape[0]

    X = extended_data[:, :-1]  # Exclude the constant term

    def fit_model(i):
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
                warnings.simplefilter("ignore")
                clf.fit(X_train, y_train)
                if clf.best_score_ > best_score:
                    best_score = clf.best_score_
                    best_model = clf.best_estimator_
                    best_model_name = model_name
                    best_params = clf.best_params_
                    best_intercept = best_model.intercept_
                    best_coefficients = best_model.coef_

        return extended_terms[i], {
            "model": best_model,
            "score": best_score,
            "model_type": best_model_name,
            "params": best_params,
            "intercept": best_intercept,
            "coefficients": best_coefficients,
            "sample_size": sample_size,
            "X_test": X_,  # NOTE: Include the entire X for evaluating the eq.
            "y_test": X_[:, i],  # NOTE: Include the entire y for evaluating the eq.
        }

    results = Parallel(n_jobs=-1)(
        delayed(fit_model)(i) for i in range(len(extended_terms) - 1)
    )

    return {term: content for term, content in results}


def infer_equations(  # noqa F811
    models,
    extended_terms,
    extended_data,
    coeff_threshold=settings.COEFF_THRESHOLD,
    coeff_cutoff=settings.COEFF_CUTOFF,
    intercept_cutoff=settings.INTERCEPT_CUTOFF,
    delta=settings.DELTA,
    objective_threshold=settings.OBJECTIVE_THRESHOLD,
):

    def milp_synthesis_wrapper(pivot, selected_terms, selected_data, model_desc):
        str = ""
        optimal = None

        sample_size = selected_data.shape[0]
        if settings.MILP_USE_SAMPLE_RATE and settings.MILP_SAMPLE_RATE > 1:
            sample_size = int(len(selected_terms) * settings.MILP_SAMPLE_RATE)
            threshold = settings.MILP_SAMPLE_THRESHOLD
            if sample_size < threshold:
                if selected_data.shape[0] > threshold:
                    sample_size = threshold
                else:  # use all data
                    sample_size = selected_data.shape[0]

            if sample_size < selected_data.shape[0]:
                sample_indices = np.random.choice(
                    selected_data.shape[0], sample_size, replace=False
                )
                selected_data = selected_data[sample_indices]
            else:
                sample_size = selected_data.shape[0]

        if settings.MILP_SOLVER == "GUROBI":
            optimal = milp.OPTIMAL
            status, expr, obj, _ = milp.milp_synthesis(
                selected_data,
                selected_terms,
                pivot,
                bound=settings.MILP_BOUND,
                timeout=settings.MILP_TIME_LIMIT,
            )
        else:
            if settings.MILP_SOLVER != "PULP":
                log.warning(
                    f"Invalid MILP solver: {settings.MILP_SOLVER}, using PULP instead"
                )
            optimal = milp_pulp.OPTIMAL
            status, expr, obj, _ = milp_pulp.milp_synthesis(
                selected_data,
                selected_terms,
                pivot,
                bound=settings.MILP_BOUND,
                timeout=settings.MILP_TIME_LIMIT,
            )

        if status == optimal:
            if abs(obj) < objective_threshold:  # check if the objective is small enough
                equation = sympy.sympify(expr)
                str += f"MILP for {pivot}: {expr} = 0 (obj: {obj})"
                str += ">>>>>>>>>>>>>> MILP <<<<<<<<<<<<<<<<\n"
                me = obj
                return (
                    Equation(equation, me, pivot, sample_size, model_desc, str),
                    None,
                    None,
                )
            else:
                str += f"MILP for {pivot}: Objective too large: {obj}\n"
                return (
                    Equation(None, None, pivot, sample_size, model_desc, str),
                    None,
                    None,
                )
        else:
            str += f"MILP for {pivot}: No solution found\n"
            return Equation(None, None, pivot, sample_size, model_desc, str), None, None

    def infer_equation(pivot, model, extended_terms, extended_data, model_desc):
        str = ""
        sample_size = model["sample_size"]

        # NOTE: preparing an equation from the regression model
        if settings.USE_CUTOFF and np.abs(model["intercept"]) >= intercept_cutoff:
            # str += f"Model for {pivot}: Intercept = {model['intercept']}!\n"
            return Equation(None, None, pivot, sample_size, model_desc, str), None, None

        rhs = sympy.Rational(0)
        coeff_terms = {}
        selected_terms = [pivot]  # Include LHS term
        terms = [item for item in extended_terms if item != pivot]

        # check all coefficients and if it is greater than 100, then skip it
        if settings.USE_CUTOFF and np.any(
            np.abs(model["coefficients"]) >= coeff_cutoff
        ):
            # str += f"Model for {pivot}: Large Coefficient!\n"
            return Equation(None, None, pivot, sample_size, model_desc, str), None, None

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
        # equation = sympy.simplify(equation)
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
        str += f"(error: {round(me, 2)}), ({model_desc}), "
        if me < delta:
            str += ">>>>>>>>>>>>>> good fit <<<<<<<<<<<<<<<<\n"
        else:
            str += "\n"

        if settings.MILP is not True and settings.REGRESSION_REFINEMENT is not True:
            return (
                Equation(equation, me, pivot, sample_size, model_desc, str),
                None,
                None,
            )

        # NOTE: MILP Synthesis based on the regression model
        # Selecting respective columns from data
        selected_indices = [extended_terms.index(term) for term in selected_terms]
        selected_data = extended_data[:, selected_indices]

        print(f"\nModel for {pivot}: {equation.evalf()}")
        print(equation.evalf())
        print(selected_terms)
        # print(selected_data)

        return (
            Equation(equation, me, pivot, sample_size, model_desc, str),
            selected_terms,
            selected_data,
        )

    results = []
    milp_input = []
    for pivot, model in models.items():
        model_desc = f"{model['model_type']}({model['params']})"
        equation, term, data = infer_equation(
            pivot, model, extended_terms, extended_data, model_desc
        )
        if equation.expr is not None:
            results.append(equation)
            milp_input.append((pivot, term, data))
            if equation.error < delta:
                continue

            # NOTE: start Regression Refinement
            if settings.REGRESSION_REFINEMENT and len(term) > 1:
                pivot_, model_ = find_model(pivot, term, data)
                model_desc = f"{model_['model_type']}({model_['params']})+Refine"
                equation, _, _ = infer_equation(pivot_, model_, term, data, model_desc)
                if equation.expr is not None:
                    results.append(equation)

        if settings.MILP and settings.FULL_MILP != settings.FullMILP.NEVER:
            # remove the last element from the extended terms and data
            terms = extended_terms.copy()
            terms.pop()
            data = np.delete(extended_data, -1, axis=1)
            model_desc = f"{model['model_type']}({model['params']})+Full"
            equation, _, _ = milp_synthesis_wrapper(pivot, terms, data, model_desc)
            results.append(equation)

    # NOTE: MILP Synthesis based on the regression model
    if settings.MILP:
        # NOTE: Parallel MILP Synthesis based on the regression model
        solver = settings.MILP_SOLVER.lower()
        if settings.PARALLEL_MILP:
            model_desc = f"Milp({solver})"
            milp_results = Parallel(n_jobs=-1)(
                delayed(milp_synthesis_wrapper)(*mi, model_desc) for mi in milp_input
            )
            for equation, _, _ in milp_results:
                results.append(equation)

        else:
            model_desc = f"Milp({solver})"
            milp_results = [
                milp_synthesis_wrapper(*mi, model_desc) for mi in milp_input
            ]
            for equation, _, _ in milp_results:
                results.append(equation)

    # NOTE: Linear Equation Solver based on the regression model
    if settings.USE_LINSOLVE:
        # NOTE: Linear Solver
        lin_solve_results = Parallel(n_jobs=-1)(
            delayed(Symbolic.linear_solve)(*mi) for mi in milp_input
        )
        for expr, sample_size in lin_solve_results:
            equation = Equation(expr, 0, pivot, sample_size, "LinSolve", "")
            results.append(equation)

    # remove None values
    return [r for r in results if r is not None and r.error is not None]


def main():
    file_path = settings.FILE_PATH
    input_data = load_input_data(file_path)
    trace_data = parse_dig_vtrace_file(input_data)

    _str = ""
    results = collections.defaultdict(list)
    for loc, data in trace_data.items():
        terms = data["terms"]
        data = data["data"]

        _str += f"\nLocation: {loc}\n"
        _str += f"Terms: {terms}\n"
        _str += f"Shape: {data.shape}\n"

        for degree in range(1, settings.DEGREE + 1):
            _str += f"\nDegree: {degree}\n"
            extended_terms, extended_data = process_trace(terms, data, degree)
            trace_data[loc]["extended_terms"] = extended_terms

            _str += f"{extended_terms}\n"

            if settings.MULTIPLE_REGRESSION:
                # (Option 1) use cross validation to find the best model for each term
                models = find_best_model(extended_terms, extended_data)
            else:
                # (Option 2) use simple linear regression to find a model for each term
                models = find_models(extended_terms, extended_data)

            # Display the models and their equations
            for term, content in models.items():
                _str += f"Model for {term}: Score = {content['score']}, "
                _str += f"{content['model_type']}({content['params']})\n"

            _str += "\n"

            result = infer_equations(models, extended_terms, extended_data)
            results[loc].extend(result)
            for r in result:
                _str += r.note

    print(_str)

    # NOTE: Reporting--Display the inferred equalities
    print("\nInferred Equalities:")
    for loc, result in results.items():
        print(
            f"\nLocation: {loc}; Traces: {trace_data[loc]['data'].shape[0]}; Terms: {trace_data[loc]['terms']}"
        )
        p_width = 73
        good_fit = set()
        max_p = 4  # pivot
        max_m = 15  # model
        max_e = 30  # equation
        max_error = 3  # error
        max_s = 2  # sample size
        for eq in result:
            if eq.error < settings.DELTA:
                eql_s = str(eq.expr.evalf())
                max_m = max(max_m, len(eq.model_desc) + 1)
                max_e = max(max_e, len(eql_s) + 4)
                max_error = max(max_error, len(str(round(eq.error, 3))))
                max_p = max(max_p, len(eq.pivot))
                max_s = max(max_s, len(str(eq.sample_size)))
                if len(eql_s) > p_width:
                    max_e = p_width
        ruler = "-" * (max_p + max_m + max_e + max_error + max_s + 13)
        # print the header
        print(ruler)
        print(
            f"{'Source':<{max_m}}| {'Term':<{max_p}} | {'Invariant/Property':<{max_e}} | {'Err':<{max_error}} | {'n':<{max_s}} |"
        )
        print(ruler)
        for eq in result:
            if eq.error < settings.DELTA:
                s_eq = str(eq.expr.evalf()) + " = 0"
                if len(s_eq) > p_width:
                    s_eq = s_eq[: (p_width - 3)] + "..."
                print(
                    f"{eq.model_desc:<{max_m}}| {eq.pivot:<{max_p}} | {s_eq:<{max_e}} | {round(eq.error, 3):<{max_error}} | {eq.sample_size:<{max_s}} |"
                )
                good_fit.add(eq.expr)
        print(ruler)

        print("\nReduced Equalities:")
        equations = Symbolic.refine(good_fit)

        for eq in equations:
            print(f"{eq} = 0")

        if settings.SLOW_SIMPLIFY:
            equations = Z3._simplify_slow(equations, [], loc)
            for eq in equations:
                print(f"{eq} = 0")

        if settings.CONSISTENCY_CHECK:
            print("\nChecking Consistency of Equations:")

            try:
                print(f"1. Solve algebraically: {sympy.solve(equations)}")
            except NotImplementedError:
                print("1. Solve algebraically: Could not solve")

            print("2. Check satisfiability: ", end="")
            sat, r = Z3.check_sat(equations)
            print(f"{sat}, {r}")


if __name__ == "__main__":  # noqa E123
    main()
