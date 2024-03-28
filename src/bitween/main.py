import collections
import math
from dataclasses import dataclass
import itertools
import warnings
from joblib import Parallel, delayed  # noqa F401
import numpy as np
from sklearn.exceptions import ConvergenceWarning
import sympy
import csv
from sklearn.linear_model import (  # noqa F401
    ElasticNet,
    Ridge,
    Lasso,
    LinearRegression,
    SGDRegressor,
)
from sklearn.model_selection import GridSearchCV, train_test_split

from bitween import settings, miscs
from bitween import milp_gurobi, milp_pulp
from bitween.miscs import Symbolic
from bitween.sampler import Domain, Distribution, sample
from bitween.z3utils import Z3

sympy.init_printing(use_unicode=False, wrap_line=False)

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)

TABLE_WIDTH = 70


@dataclass(frozen=True)
class Equation:
    expr: sympy.Expr
    error: float
    pivot: str
    sample_size: int
    model_desc: str
    dimension: int
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
        parts = line.split(";")
        parts = [part.strip() for part in parts]
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


def process_trace(terms: list[str], data, degree):
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
            "params": {"alpha": [1e-4, 1e-3, 1e-2, 1e-1, 100, 1000]},
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

    # return {term: content for term, content in results}
    models = {}
    for term, content in results:
        if content["model"] is None:
            log.debug(f"Model for {term}: No model found")
            continue
        models[term] = content
    return models


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

    # NOTE: Property Test for MILP-based Synthesis
    def property_test(term_coefs: dict[str, float]) -> float:
        # Evaluate the equation for each row in entire data
        error = 0.0
        for row in extended_data:
            lhs = 0
            for term, coef in term_coefs.items():
                lhs += coef * row[extended_terms.index(term)]
            error += abs(lhs)
        return error / extended_data.shape[0]

    # NOTE: MILP-based Synthesis
    def milp_synthesis_wrapper(
        pivot: str,
        selected_terms: list[str],
        selected_data: np.ndarray,
        model_desc: str,
        blocked: str,
    ):
        str_ = ""
        optimal = None

        dims = len(selected_terms)
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
            optimal = milp_gurobi.OPTIMAL
            status, expr, obj, term_coefs, _ = milp_gurobi.milp_synthesis(
                selected_data,
                selected_terms,
                pivot,
                bound=settings.MILP_BOUND,
                timeout=settings.MILP_TIME_LIMIT,
                blocked=blocked,
            )
        else:
            if settings.MILP_SOLVER != "PULP":
                log.warning(
                    f"Invalid MILP solver: {settings.MILP_SOLVER}, using PULP instead"
                )
            optimal = milp_pulp.OPTIMAL
            status, expr, obj, term_coefs, _ = milp_pulp.milp_synthesis(
                selected_data,
                selected_terms,
                pivot,
                bound=settings.MILP_BOUND,
                timeout=settings.MILP_TIME_LIMIT,
                blocked=blocked,
            )

        if status == optimal:
            if abs(obj) < objective_threshold:  # check if the objective is small enough
                equation = sympy.sympify(expr)

                s_eq = str(equation.evalf())
                if len(s_eq) > TABLE_WIDTH:
                    s_eq = s_eq[:TABLE_WIDTH] + " ..."
                    s_eq = f"{s_eq + ' = 0':<{TABLE_WIDTH+4}} "
                else:
                    s_eq = f"{s_eq + ' = 0':<{TABLE_WIDTH+8}} "

                # NOTE: Property Test: Evaluate the equation for each row in entire data
                error = property_test(term_coefs)

                s_err = f"err: {round(error, 2):<5.2f}"
                s_obj = f"obj: {round(obj, 2):.2f}"
                str_ += s_eq + f"({s_err}); ({model_desc}); ({s_obj}); [{pivot}] **\n"

                return (
                    Equation(
                        equation, error, pivot, sample_size, model_desc, dims, str_
                    ),
                    None,
                    None,
                )
            else:
                str_ += f"MILP for {pivot}: Objective too large: {obj}\n"
                return (
                    Equation(None, None, pivot, sample_size, model_desc, dims, str_),
                    None,
                    None,
                )
        else:
            str_ += f"MILP for {pivot}: No solution found\n"
            return (
                Equation(None, None, pivot, sample_size, model_desc, dims, str_),
                None,
                None,
            )

    def infer_equation(pivot, model, extended_terms, extended_data, model_desc):
        str_ = ""
        sample_size = model["sample_size"]
        dims = len(extended_terms)

        # NOTE: preparing an equation from the regression model
        if settings.USE_CUTOFF and np.abs(model["intercept"]) >= intercept_cutoff:
            # str += f"Model for {pivot}: Intercept = {model['intercept']}!\n"
            return (
                Equation(None, None, pivot, sample_size, model_desc, dims, str_),
                None,
                None,
            )

        rhs = 0
        coeff_terms = {}
        selected_terms = [pivot]  # Include LHS term
        terms = [item for item in extended_terms if item != pivot]

        # check all coefficients and if it is greater than 100, then skip it
        if settings.USE_CUTOFF and np.any(
            np.abs(model["coefficients"]) >= coeff_cutoff
        ):
            # str += f"Model for {pivot}: Large Coefficient!\n"
            return (
                Equation(None, None, pivot, sample_size, model_desc, dims, str_),
                None,
                None,
            )

        for i, coefficient in enumerate(model["coefficients"]):
            if abs(coefficient) >= coeff_threshold:
                coeff = round(coefficient, 2)  # TODO be careful with rounding
                if coeff != 0:
                    rhs += sympy.Rational(coeff) * sympy.Symbol(terms[i])
                    coeff_terms[terms[i]] = coeff
                    # Include term in selected list
                    selected_terms.append(terms[i])

        # Add the constant term (intercept)
        intercept = round(model["intercept"], 2)  # TODO be careful with rounding
        if intercept > coeff_threshold:
            rhs += sympy.Rational(intercept)

        equation = sympy.Symbol(pivot) - rhs
        # equation = sympy.simplify(equation)
        s_eq = str(equation.evalf())
        if len(s_eq) > TABLE_WIDTH:
            s_eq = s_eq[:TABLE_WIDTH] + " ..."
            s_eq = f"{s_eq + ' = 0':<{TABLE_WIDTH+4}} "
        else:
            s_eq = f"{s_eq + ' = 0':<{TABLE_WIDTH+8}} "

        str_ += s_eq

        print(f"\nModel for {pivot}: {s_eq}")
        print(s_eq)

        # NOTE: Property Test: Evaluate the equation for each row in X_test
        X_test = model["X_test"]
        y_test = model["y_test"]

        rhs_values = np.zeros(y_test.shape[0])
        for i, row in enumerate(X_test):
            for t, coeff in coeff_terms.items():
                rhs_values[i] += coeff * row[extended_terms.index(t)]
            if intercept > coeff_threshold:
                rhs_values[i] += intercept

        me = np.mean(np.abs(rhs_values - y_test))
        str_ += f"(err: {round(me, 2):<5.2f}): ({model_desc}); [{pivot}]"
        if me < delta:
            str_ += "***\n"
        else:
            str_ += "\n"

        if settings.MILP is not True and settings.REGRESSION_REFINEMENT is not True:
            return (
                Equation(equation, me, pivot, sample_size, model_desc, dims, str_),
                None,
                None,
            )

        # NOTE: MILP Synthesis based on the regression model
        # Selecting respective columns from data
        selected_indices = [extended_terms.index(term) for term in selected_terms]
        selected_data = extended_data[:, selected_indices]

        print(selected_terms)
        # print(selected_data)

        return (
            Equation(equation, me, pivot, sample_size, model_desc, dims, str_),
            selected_terms,
            selected_data,
        )

    # NOTE: Inference starts here
    results = []
    milp_input = []
    term_frequencies = collections.Counter()
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

    # collect term frequencies from inferred equations (results)
    for equation in results:
        if not equation.model_desc.startswith("Milp"):
            term_frequencies.update([str(s) for s in equation.expr.free_symbols])
    print(f"Term Frequencies: {term_frequencies}\n")

    # NOTE: MILP Synthesis based on the regression model
    if settings.MILP:
        # NOTE: Parallel MILP Synthesis based on the regression model
        solver = settings.MILP_SOLVER.lower()
        blocked = None  # NOTE: No blocked term for now
        if settings.PARALLEL_MILP:
            model_desc = f"Milp({solver})"
            milp_results = Parallel(n_jobs=-1)(
                delayed(milp_synthesis_wrapper)(*mi, model_desc, blocked)
                for mi in milp_input
            )
            for equation, _, _ in milp_results:
                results.append(equation)

        else:
            model_desc = f"Milp({solver})"
            milp_results = [
                milp_synthesis_wrapper(*mi, model_desc, blocked) for mi in milp_input
            ]
            for equation, _, _ in milp_results:
                results.append(equation)

    # NOTE: Run a milp over the most frequent terms, pivot all terms
    if settings.MILP and settings.MILP_FREQ_REFINE and len(term_frequencies) > 5:
        terms = []  # there is no "1" in term_frequencies
        # keep the relative order of the terms
        for term in extended_terms:
            if term in term_frequencies:
                terms.append(term)
        selected_indices = [extended_terms.index(term) for term in terms]
        selected_data = extended_data[:, selected_indices]
        model_desc = f"Milp({settings.MILP_SOLVER.lower()})+Freqs"
        inputs = []
        for pivot in terms:
            inputs.append((pivot, terms, selected_data, model_desc))

        blocked = None  # NOTE: No blocked term for now
        milp_results = Parallel(n_jobs=-1)(
            delayed(milp_synthesis_wrapper)(*mi, blocked) for mi in inputs
        )
        for equation, _, _ in milp_results:
            results.append(equation)

    # NOTE: EAGER MILP over Full Model that includes all terms
    if settings.MILP and settings.FULL_MILP != settings.FullMILP.NEVER:
        if (
            settings.FULL_MILP == settings.FullMILP.AUTO
            and extended_data.shape[0] < settings.FULL_MILP_THRESHOLD
        ) or settings.FULL_MILP == settings.FullMILP.ALWAYS:
            model_desc = f"Milp({solver})+Full"

            milp_input = []
            for pivot in extended_terms[:-1]:
                terms = extended_terms.copy()
                terms.pop()
                data = np.delete(extended_data, -1, axis=1)
                milp_input.append((pivot, terms, data, model_desc))

            blocked = None  # NOTE: No blocked term for now
            milp_results = Parallel(n_jobs=-1)(
                delayed(milp_synthesis_wrapper)(*mi, blocked) for mi in milp_input
            )
            for equation, _, _ in milp_results:
                results.append(equation)

    # NOTE: Linear Equation Solver based on the regression model
    if settings.USE_LINSOLVE:
        # NOTE: Linear Solver

        milp_input = []
        for pivot in extended_terms[:-1]:
            terms = extended_terms.copy()
            data = extended_data.copy()
            milp_input.append((pivot, terms, data))

        lin_solve_results = Parallel(n_jobs=-1)(
            delayed(Symbolic.linear_solve)(*mi) for mi in milp_input
        )
        dims = len(extended_terms)
        for expr, sample_size in lin_solve_results:
            if expr is not None and expr != 0:
                equation = Equation(expr, 0, pivot, sample_size, "LinSolve", dims, "")
            results.append(equation)

    # remove None values
    return [
        r for r in results if r is not None and r.error is not None
    ], term_frequencies


def main(file_path: str = None):
    if file_path is None:
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

            _str += f"{extended_terms}; size: {len(extended_terms)}\n"

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

            result, term_freq = infer_equations(models, extended_terms, extended_data)
            _str += f"Term Frequencies: {term_freq}; Size: {len(term_freq)}\n\n"
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
        p_width = settings.PROPERTY_TABLE_WIDTH
        good_fit = set()
        max_p = 4  # pivot
        max_m = 15  # model
        max_e = 30  # equation
        max_error = 3  # error
        max_s = 2  # sample size
        init_d = str(len(trace_data[loc]["extended_terms"]))  # initial dimension
        max_d = len(init_d)  # dimension
        for eq in result:
            if eq.error < settings.DELTA:
                # NOTE: a dirty hack to simplify the equation
                eql_s = str(sympy.sympify(str(sympy.nsimplify(eq.expr.evalf()))))
                max_m = max(max_m, len(eq.model_desc) + 1)
                max_e = max(max_e, len(eql_s) + 4)
                max_error = max(max_error, len(str(round(eq.error, 3))))
                max_p = max(max_p, len(eq.pivot))
                max_s = max(max_s, len(str(eq.sample_size)))
                max_d = max(max_d, len(str(eq.dimension)))
                if len(eql_s) > p_width:
                    max_e = p_width
        ruler = "-" * (max_p + max_m + max_d + max_e + max_error + max_s + 16)
        # print the header
        print(ruler)
        print(
            f"{'Source':<{max_m}}| {'Term':^{max_p}} | {init_d:<{max_d}} | {'Invariant/Property':<{max_e}} | {'Err':<{max_error}} | {'n':^{max_s}} |"
        )
        print(ruler)
        for eq in result:
            if eq.error < settings.DELTA:
                # NOTE: a dirty hack to simplify the equation
                s_eq = (
                    str(sympy.sympify(str(sympy.nsimplify(eq.expr.evalf())))) + " = 0"
                )
                if len(s_eq) > p_width:
                    s_eq = s_eq[: (p_width - 3)] + "..."
                print(
                    f"{eq.model_desc:<{max_m}}| {eq.pivot:^{max_p}} | {eq.dimension:<{max_d}} | {s_eq:<{max_e}} | {round(eq.error, 3):<{max_error}} | {eq.sample_size:^{max_s}} |"
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


def get_vars(template: list[str]):
    vars = set()
    for t in template:
        expr = sympy.sympify(t)
        vars.update(expr.free_symbols)
    return vars


def generate_input_data(
    domain: Domain,  # domain of the samples
    distribution: Distribution,  # distribution of the samples
    exprs: list[str],  # function calls to function basis
    template: list[str],  # template for function basis
    *functions,
    max_degree: int = 2,  # maximum degree
    n: int = 30,  # number of samples
    delta: float = 0.1,  # error threshold
):

    settings.DEGREE = max_degree
    settings.DELTA = delta

    # get a dictionary of functions
    functions = {func.__name__: func for func in functions}
    # get the list of variables
    variables = get_vars(template)

    evals = [["vtrace1"] + [f"I {term}" for term in template]]
    i = 0
    while i < n:
        variables = sample(domain, distribution, list(variables))
        eval_row = ["vtrace1"]
        try:
            for expr in exprs:
                eval_row.append(
                    eval(
                        expr,
                        functions | variables,
                        {
                            "sqrt": math.sqrt,
                            "abs": abs,
                            "sin": math.sin,
                            "cos": math.cos,
                            "tan": math.tan,
                            "tanh": math.tanh,
                            "sinh": math.sinh,
                            "cosh": math.cosh,
                            "exp": math.exp,
                            "log": math.log,
                            "sign": np.sign,
                            "pi": math.pi,
                            "arcsin": math.asin,
                            "asin": math.asin,
                            "arccos": math.acos,
                            "acos": math.acos,
                            "arctan": math.atan,
                            "atan": math.atan,
                            "arctan2": math.atan2,
                            "atan2": math.atan2,
                        },
                    )
                )
            evals.append(eval_row)
        except ZeroDivisionError as e:
            print(f"ZeroDivisionError: {e}, {variables}")
            continue
        i += 1

    # Write the data to a CSV file
    with open("trace.csv", mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(evals)

    main("trace.csv")


def test_sin():

    def F(x, terms=40):
        """sinTaylor"""
        result = 0.0

        for n in range(terms):
            numerator = (-1) ** n
            denominator = 1

            for i in range(1, 2 * n + 2):
                denominator *= i

            term = numerator * (x ** (2 * n + 1)) / denominator
            result += term

        return result

    generate_input_data(
        Domain.Real,
        Distribution.Small,
        ["F(x+y)", "F(x-y)", "F(x)", "F(y)"],  # how to call functions
        ["f(x+y)", "f(x-y)", "f(x)", "f(y)"],  # function basis aka the template
        F,
        max_degree=2,
        n=150,
    )


if __name__ == "__main__":  # noqa E123
    main()
