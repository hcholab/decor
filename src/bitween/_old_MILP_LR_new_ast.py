from itertools import product
import math  # noqa F401
from gurobipy import GRB
import gurobipy as gp
import csv
import time

from sklearn.feature_selection import (  # noqa F401
    SelectKBest,
    f_regression,
    mutual_info_regression,
)
from sklearn.metrics import mean_absolute_error  # noqa F401
from sklearn.model_selection import train_test_split  # noqa F401
import numpy as np

from sympy import (  # noqa F401
    Expr,
    Symbol,
    cosh,
    sinh,
    symbols,
    Function,
    tan,
    tanh,
    sin,
    cos,
    simplify,
    lambdify,
    sympify,
    exp,
    latex,
    sqrt,
    Abs,
    log,
    sign,
    pi,
)

from sklearn.linear_model import Lasso, LinearRegression  # noqa F401

from sampler import Domain, Distribution, sample
from terms import canonicalize
from utilities import pp
from verifier import property_test, verify


def is_complex_number(num):
    if isinstance(num, Expr):
        _, imag_part = num.as_real_imag()
        return imag_part != 0
    return num.imag != 0


# Function to generate all expressions up to a given depth
def generate_all_expressions(leaf_terms, symbolic_functions, depth):
    if depth == 0:
        return [sympify(term) for term in leaf_terms]

    prev_level_exprs = generate_all_expressions(
        leaf_terms, symbolic_functions, depth - 1
    )
    all_exprs = set(prev_level_exprs)

    for func in symbolic_functions:
        if not isinstance(func, Expr):
            func = sympify(func)
        arg_count = len(func.free_symbols)
        for args in product(prev_level_exprs, repeat=arg_count):
            all_exprs.add(func.subs(zip(func.free_symbols, args)))

    return list(all_exprs)


if __name__ == "__main__":  # noqa E123
    degree = None
    importantVarName = "?"
    block = None
    domain = Domain.Real
    distribution = Distribution.Small
    BOUND = 2
    N = 50

    ERROR_BOUND = 0.3  # 0.05

    x, y, z, r, s, t = symbols("x y z r s t")
    f = Function("f")
    g = Function("g")
    h = Function("h")
    u = Function("u")
    v = Function("v")
    w = Function("w")
    F = Function("F")
    G = Function("G")
    H = Function("H")
    U = Function("U")
    V = Function("V")
    W = Function("W")

    def g():
        return 1

    def h():
        return 1

    def u():
        return 1

    def var():
        return 1

    def w():
        return 1

    # start timer
    start = time.time()

    # clear the file
    with open("data.csv", mode="w", newline="") as file:
        file.write("")  # Write an empty string to clear the file

    with open("data.csv", mode="a", newline="\n") as file:
        writer = csv.writer(file)

        important = None

        # to_be_removed_from_model = []
        complex_term_to_be_removed = set()

        degree = 1
        importantVarName = "P(x, y)"
        # importantVarName = "f(g(x), g(h(x, y)))"
        # importantVarName = "g(h(f(x, x), f(x, y))"
        BOUND = 1

        termNames_ = generate_all_expressions(
            leaf_terms=["x", "y"],
            symbolic_functions=["g(x)", "f(x,y)", "h(x,y)", "P(x,y)"],
            depth=2,
        )

        def g(x):
            return sqrt(x)

        def f(x, y):
            return x * y

        def h(x, y):
            return x + y

        def P(x, y):
            return sqrt(x**2 + x * y)

        implementation_map = {"f": f, "g": g, "h": h, "P": P}
        # implementation_map = {"f": f, "g": g, "h": h}

        variablesNames = set()
        for expr in termNames_:
            for var in expr.free_symbols:
                variablesNames.add(str(var))

        # convert all termnames to strings
        termNames_ = [str(term) for term in termNames_]
        termNames_.append("g(h(f(x, x), f(x, y)))")
        termNames_.append("1")

        for t in termNames_:
            print(t)

        k = N
        while k > 0:
            termNames = termNames_
            variables = sample(domain, distribution, variablesNames)

            if variables["x"] < 0:
                continue
            if variables["y"] < 0:
                continue
            if variables["x"] ** 2 + variables["x"] * variables["y"] < 0:
                continue
            if variables["y"] ** 2 + variables["y"] * variables["x"] < 0:
                continue
            if variables["x"] ** 2 + variables["x"] * variables["x"] < 0:
                continue
            if variables["y"] ** 2 + variables["y"] * variables["y"] < 0:
                continue

            print(k, ":", variables)

            terms = []
            for expr in termNames:
                try:
                    terms.append(
                        eval(
                            str(expr),
                            implementation_map | variables,
                            {
                                "sqrt": sqrt,
                                "Abs": Abs,
                                "sin": sin,
                                "cos": cos,
                                "tan": tan,
                                "tanh": tanh,
                                "sinh": sinh,
                                "cosh": cosh,
                                "exp": exp,
                                "log": log,
                                "sign": sign,
                                "pi": pi,
                            },
                        )
                    )
                except ZeroDivisionError as e:
                    print(f"ZeroDivisionError: {e}, {variables}")
                    continue

            terms.append(1)

            # NOTE: g( h( f(x,x), f(x,y) ) = f( g(x), g( h(x,y) ))

            # add the index of a term that results in a complex solution to the to_be_removed_from_model list
            # there is no complex valued terms in the model, check if there is any nan or inf
            # if so continue to select a new set of terms with fress random values.
            # no_complex = True
            # for i in range(len(terms)):
            #     if not terms[i].is_integer and not terms[i].is_real:
            #         to_be_removed_from_model.append(i)
            #         no_complex = False
            # if no_complex:
            #     if any(math.isnan(x) and math.isinf(x) for x in terms):
            #         continue

            # if there is a complex number in the samples, print the value and term
            # for i in range(len(terms)):
            #     if not terms[i].is_integer and not terms[i].is_real:
            #         print(f"{termNames[i]}: {terms[i]}")

            # if there is at least one term that makes the expression complex, remove
            # that column from terms and termNames. Remember this for the rest of the
            # iterations
            for i, term in enumerate(terms):
                if is_complex_number(term):
                    complex_term_to_be_removed.add(i)

            # remove these terms from the model
            terms = [
                term
                for i, term in enumerate(terms)
                if i not in complex_term_to_be_removed
            ]

            termNames = [
                termName
                for i, termName in enumerate(termNames)
                if i not in complex_term_to_be_removed
            ]

            # putting important term to the end
            important = termNames.index(importantVarName)
            terms = terms[:important] + terms[important + 1 :] + [terms[important]]
            termNames = (
                termNames[:important]
                + termNames[important + 1 :]
                + [termNames[important]]
            )

            # removing constant
            constant = termNames.index("1")
            terms = terms[:constant] + terms[constant + 1 :]
            termNames = termNames[:constant] + termNames[constant + 1 :]

            # if k == N:
            #     k = len(terms) + 10

            k -= 1

            writer.writerow(terms)

    # print("")
    # print(terms)
    # print to_be_removed_from_model termNames and terms if any
    # if len(to_be_removed_from_model) > 0:
    #     print("to_be_removed_from_model:")
    #     for index in to_be_removed_from_model:
    #         print(f"{termNames[index]}: {terms[i]}")

    print(termNames)

    # Load the CSV file into a numpy array
    data = np.genfromtxt("data.csv", delimiter=",")

    # Split the data into X and y
    X = data[:, :-1]  # Select all columns except the last one
    y = data[:, -1]  # Select the last column

    features = []
    r_squared = []
    print("------------------------------------------")
    lr_prop = ""
    lr_expr = ""
    intercept_included = True
    n = 0
    for n in range(10):
        prev_X = X
        prev_termNames = termNames
        to_be_removed_from_model = []
        to_be_likely_removed_from_model = []
        try:
            # Create a linear regression model and fit it to the data
            model = LinearRegression(copy_X=True, fit_intercept=intercept_included).fit(
                X, y
            )
            # Print the coefficients of the regression line
            # print(f"Coefficients: {model.coef_}")
            # print(f"Intercept: {model.intercept_}")
            print(f"Features: {model.n_features_in_}")
            features.append(model.n_features_in_)

            print("------------------------------------------")
            max_len = max([len(x) for x in termNames])
            # print all the coefficients and their corresponding variables
            for i in range(len(model.coef_)):
                print(f"%{max_len}s = %2s" % (termNames[i], (round(model.coef_[i], 5))))
            # print the intercept
            if intercept_included:
                print(f"%{max_len}s = %2s" % ("1", model.intercept_))
            print("------------------------------------------")
            # print R^2 score
            print(f"R^2 score: {model.score(X, y)}")
            r_squared.append(model.score(X, y))

            # printing the solution
            lr_prop = importantVarName + " = "
            lr_expr = "-" + importantVarName + " "
            res = 0
            for i in range(len(model.coef_)):
                res += model.coef_[i] * terms[i]
                if abs(model.coef_[i]) > BOUND:
                    to_be_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.05 and len(termNames) < 10:
                    rounded = round(model.coef_[i], 2)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.4 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.01 and len(termNames) < 40:
                    rounded = round(model.coef_[i], 2)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.3 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                elif abs(model.coef_[i]) > 0.001:
                    rounded = round(model.coef_[i], 3)
                    if rounded == round(model.coef_[i]):
                        rounded = int(rounded)
                    lr_prop += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    lr_expr += "+ " + str(rounded) + "*" + str(termNames[i]) + " "
                    if abs(model.coef_[i]) < 0.1 and n > 0:
                        to_be_likely_removed_from_model.append(i)
                else:
                    to_be_removed_from_model.append(i)

            if intercept_included and abs(round(model.intercept_, 2)) > 0.01:
                lr_prop += " + " + str(round(model.intercept_, 2))
                lr_expr += " + " + str(round(model.intercept_, 2))
                intercept_included = False

            print("------------------------------------------")
            print(lr_prop)
            print(f"error: {res}")

        except ValueError as e:
            print(f"ValueError: {e}")
        if (
            len(to_be_removed_from_model) == 0
            and len(to_be_likely_removed_from_model) == 0
        ):
            print("------------------------------------------")
            print("no more terms to remove!!!")
            break
        else:
            X = np.delete(
                X, to_be_removed_from_model + to_be_likely_removed_from_model, 1
            )
            termNames = np.delete(
                termNames, to_be_removed_from_model + to_be_likely_removed_from_model
            )

        # if n > 0 and r_squared[n] < r_squared[n - 1]:
        #     print("r_square decreased!")
        #     break

    # print("------------------------------------------")
    # proved = verify(canonicalize(lr_expr), f, g, h)
    # print("------------------------------------------")
    # functions = [f, g, h, u, v, w]
    # passed = property_test(
    #     lr_expr,
    #     *functions,
    #     domain=domain,
    #     distribution=distribution,
    #     epsilon=1e-13,
    #     n=30,
    # )

    # exit()
    #######################################
    print("------------------------------------------")

    # X = data
    # append the y values to the X matrix
    X = np.append(X, np.array([y]).T, axis=1)

    # traverse the data columnwise. If the average is less than 1e-6, set SCALE to 1e5.
    # If the average is greater than 1e6, set SCALE to 1e-5.
    SCALE = 1  # scaling factor for a pulse value
    for i in range(len(X[0])):
        avg = 0
        for j in range(len(X)):
            avg += X[j][i]
        avg /= len(X)
        if avg < 1e-7:
            SCALE = 1e5
        if avg > 1e7:
            SCALE = 1e-5

    print(f"SCALE: {SCALE:e}")

    # find the minimum and maximum values of X
    minX = 0
    maxX = 0
    for i in range(len(X)):
        for j in range(len(X[i])):
            if X[i][j] < minX:
                minX = X[i][j]
            if X[i][j] > maxX:
                maxX = X[i][j]

    INTEGRALITY_FOCUS = 1
    # MIPFOCUS = 2
    NUMERIC_FOCUS = 3
    # OPTIMALITY_TOL = 1e-9
    # SOS1 = False
    # ERROR_BOUND = 0.1  # 0.05
    ROUND = None
    SCALE = 1

    m = gp.Model("synthesis of random self-reducible properties")
    m.setParam("TimeLimit", 3)
    m.setParam("IntegralityFocus", INTEGRALITY_FOCUS)
    # m.setParam("MIPFocus", MIPFOCUS)
    # m.setParam("OptimalityTol", OPTIMALITY_TOL)
    m.setParam("NumericFocus", NUMERIC_FOCUS)

    # For each term, create an integer decision variable and
    for i in range(len(termNames)):
        m.addVar(vtype=GRB.INTEGER, name=f"term_{i}", lb=-BOUND, ub=BOUND)
        m.update()
        if termNames[i] == importantVarName:  # e.g. "f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 1, name=f"term_{i}_ub")
            # m.getVarByName(f"term_{i}").setAttr("BranchPriority", 1000)
        if block is not None and termNames[i] == block:  # e.g. "f(x-y)*f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 0, name=f"term_{i}_ub")

    # NOTE: add the last constant as a term
    m.addVar(vtype=GRB.INTEGER, name=f"term_{len(termNames)}", lb=-BOUND, ub=BOUND)
    m.update()

    # m.addConstr(gp.quicksum(m.getVars()) >= -20, name="sum_terms")
    # m.addConstr(gp.quicksum(m.getVars()) <= -15, name="sum_terms")

    abs_vars_name = {}
    abs_vars_expr = {}
    for i in range(len(X)):
        # create a continous error variable.
        var_error = m.addVar(
            vtype=GRB.CONTINUOUS, name=f"error_{i}", lb=-ERROR_BOUND, ub=ERROR_BOUND
        )
        abs_vars_name[f"error_{i}"] = var_error
        vals = []
        for j in range(len(X[i])):
            # TODO: round the value of X[i][j] to ? decimal places
            if ROUND is None:
                vals.append(X[i][j] * SCALE * m.getVarByName(f"term_{j}"))
            else:
                vals.append(round(X[i][j], ROUND) * SCALE * m.getVarByName(f"term_{j}"))
            # vals.append(X[i][j] * m.getVarByName(f"term_{j}"))

        # add the last constant as a term
        vals.append(m.getVarByName(f"term_{len(termNames)}"))

        # create an expression for the sum of the datapoint times the decision variable.
        sum_terms = gp.quicksum(vals)
        abs_vars_expr[f"error_{i}"] = sum_terms
        m.addConstr(sum_terms == var_error, name=f"error_{i}_ub")
        # m.addConstr(sum_terms <= ERROR_BOUND, name=f"error_{i}_ub")
        # m.addConstr(sum_terms >= -ERROR_BOUND, name=f"error_{i}_lb")

    # convexify the absolute value function in the objective function
    # NOTE: set objective function
    for name in abs_vars_name.keys():
        var = abs_vars_name[name]
        lr_expr = abs_vars_expr[name]
        # m.addConstr(expr <= var, name=f"sum_{name}_ub")
        # m.addConstr(-expr <= var, name=f"sum_{name}_lb")

    # TODO:
    # m.addConstr(gp.quicksum(abs_vars_name.values()) <= 1e4, name="obj_ub")

    m.setObjective(gp.quicksum(abs_vars_name.values()), GRB.MINIMIZE)

    m.write("synthesis.lp")

    try:
        print("------------------------------------------")
        m.optimize()
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))

    print("------------------------------------------")
    ordered_gates = {}
    if m.Status == GRB.OPTIMAL:
        print("Optimal objective: %g" % m.ObjVal)
    elif m.Status == GRB.INF_OR_UNBD:
        print("Model is infeasible or unbounded")
        exit(0)
    elif m.Status == GRB.INFEASIBLE:
        print("Model is infeasible")
        print("------------------------------------------")
        print(
            f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
        )
        print("------------------------------------------")
        print(f"scale: {SCALE:e}")
        print("------------------------------------------")
        exit(0)
    elif m.Status == GRB.UNBOUNDED:
        print("Model is unbounded")
        exit(0)
    else:
        print("Optimization ended with status %d" % m.Status)
        print("------------------------------------------")
        print(
            f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
        )
        print("------------------------------------------")
        exit(0)

    milp_expr = ""
    first_term = True

    # NOTE: add the last constant as a term
    termNames = np.append(termNames, "1")

    for var in m.getVars():
        # if v.X != 0:
        #     print('%s %g' % (v.VarName, v.X))
        if var.VarName.startswith("term_"):  # NOTE
            # find the length of the longest term in termNames
            max_len = max([len(x) for x in termNames])
            print(
                f"%8s | %{max_len}s = %2s"
                % (var.VarName, termNames[int(var.VarName[5:])], pp(var.X))
            )
            if var.X != 0:
                coeff = ""
                if var.X > 0 and not first_term:
                    coeff = " + "
                if var.X > 0 and first_term:
                    coeff = ""
                if var.X < 0:
                    coeff = " - "
                if var.X != 1 and var.X != -1:
                    coeff += f"{pp(abs(var.X))}*"
                milp_expr += f"{coeff}{termNames[int(var.VarName[5:])]}"
                first_term = False

    # for v in m.getVars():
    #     if v.VarName.startswith("error_"):  # NOTE
    #         print('%s %g' % (v.VarName, v.X))

    milp_expr = milp_expr.strip()
    print("------------------------------------------")
    print(f"Time: {round(m.runTime, 2)}s")
    print("Optimal objective: %g" % m.ObjVal)
    print("------------------------------------------", end=" ")
    m.printStats()
    print("------------------------------------------", end=" ")
    m.printQuality()
    print("------------------------------------------")
    print(
        f"  LR property: {lr_prop} (features: {features}) (R^2: {np.round(r_squared, 3)})"
    )
    print("------------------------------------------")
    print(
        f"MILP property: {milp_expr} = 0 ({m.ObjVal}) (block: {block}) (bound: {BOUND})"
    )
    print("------------------------------------------")
    print(f"scale: {SCALE:e}")

    print("------------------------------------------")
    if milp_expr == "":
        print("no terms in the property!")
        exit(0)
    proved = verify(milp_expr, f, g, h)
    print("------------------------------------------")
    functions = [f, g, h, u, v, w]
    passed = property_test(
        milp_expr,
        *functions,
        domain=domain,
        distribution=distribution,
        epsilon=0.1,
        n=30,
    )
    print("------------------------------------------")
    print(f"{canonicalize(milp_expr)} = 0")
    print("------------------------------------------")
    # print the elapsed time
    print(f"Time: {round(m.runTime, 2)}s")
    print("------------------------------------------")
