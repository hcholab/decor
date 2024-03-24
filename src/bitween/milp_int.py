from gurobipy import GRB
import gurobipy as gp

import numpy as np
from sympy import sympify

from bitween.utilities import pp

INTEGRALITY_FOCUS = 1
# MIPFOCUS = 2
NUMERIC_FOCUS = 3
# OPTIMALITY_TOL = 1e-9
# SOS1 = False
ERROR_BOUND = 0.1  # 0.05

OPTIMAL = GRB.OPTIMAL


def milp_synthesis(  # noqa: C901
    data: np.ndarray,
    terms: list[str],
    pivot: str,  # pivot term
    blocked: str = None,  # blocked term
    bound=2,
    timeout=10,  # 10 seconds
) -> tuple[int, str | None, float | None, list[str]]:
    """
    Parameters
    ----------
    data : np.ndarray
        list of datapoints
    terms : list[str]
        list of term names
    pivot : str
        pivot term
    blocked : str, optional
        blocked term, by default None
    bound : int, optional
        bound, by default 2
    scale : int, optional
        scale, by default 1

    Returns
    -------
    status: the status of the optimization (e.g. GRB.OPTIMAL)
    expr: the synthesized property
    obj_val: the objective value
    """
    print("------------------------------------------")
    m = gp.Model("synthesis of random self-reducible properties")
    m.setParam("TimeLimit", timeout)
    m.setParam("IntegralityFocus", INTEGRALITY_FOCUS)
    # m.setParam("MIPFocus", MIPFOCUS)
    # m.setParam("OptimalityTol", OPTIMALITY_TOL)
    m.setParam("NumericFocus", NUMERIC_FOCUS)

    # For each term, create an integer decision variable and
    for i in range(len(terms)):
        m.addVar(vtype=GRB.INTEGER, name=f"term_{i}", lb=-bound, ub=bound)
        m.update()
        if terms[i] == pivot:  # e.g. "f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 1, name=f"term_{i}_ub")
            # m.getVarByName(f"term_{i}").setAttr("BranchPriority", 1000)
        if blocked is not None and terms[i] == blocked:  # e.g. "f(x-y)*f(x+y)"
            var = m.getVarByName(f"term_{i}")
            m.addConstr(var == 0, name=f"term_{i}_ub")

    # NOTE: add the last constant as a term
    m.addVar(vtype=GRB.INTEGER, name=f"term_{len(terms)}", lb=-bound, ub=bound)
    m.update()

    for i in range(len(data)):
        vals = []
        for j in range(len(data[i])):
            vals.append(data[i][j] * m.getVarByName(f"term_{j}"))

        # add the last constant as a term
        vals.append(m.getVarByName(f"term_{len(terms)}"))

        # create an expression for the sum of the datapoint times the decision variable.
        m.addConstr(gp.quicksum(vals) == 0, name=f"eq_{i}")

    # m.setObjective(gp.quicksum(abs_vars_name.values()), GRB.MINIMIZE)

    m.write("synthesis.lp")

    try:
        print("------------------------------------------")
        m.optimize()
    except gp.GurobiError as e:
        print("Error code " + str(e.errno) + ": " + str(e))
        exit()

    print("------------------------------------------")
    if m.Status == GRB.OPTIMAL:
        print("Optimal objective: %g" % m.ObjVal)
    elif m.Status == GRB.INF_OR_UNBD:
        print("Model is infeasible or unbounded")
        print("------------------------------------------")
        return m.Status, None, None, None
    elif m.Status == GRB.INFEASIBLE:
        print("Model is infeasible")
        print("------------------------------------------")
        return m.Status, None, None, None
    elif m.Status == GRB.UNBOUNDED:
        print("Model is unbounded")
        return m.Status, None, None, None
    else:
        print("Optimization ended with status %d" % m.Status)
        return m.Status, None, None, None

    expr = ""
    first_term = True
    terms.append("1")  # NOTE: add the last constant as a term

    term_costs = {}
    for v in m.getVars():
        # if v.X != 0:
        #     print('%s %g' % (v.VarName, v.X))
        if v.VarName.startswith("term_"):  # NOTE
            # find the length of the longest term interm_names
            max_len = max([len(x) for x in terms])
            cost = ""
            if v.X != 0:
                coeff = ""
                if v.X > 0 and not first_term:
                    coeff = " + "
                if v.X > 0 and first_term:
                    coeff = ""
                if v.X < 0:
                    coeff = " - "
                if v.X != 1 and v.X != -1:
                    coeff += f"{pp(abs(v.X))}*"
                term = terms[int(v.VarName[5:])]
                term_ = f"{coeff}{terms[int(v.VarName[5:])]}"
                cost = sympify(term_).count_ops()
                term_costs[term] = cost
                cost = f"cost: {cost}"
                expr += f"{coeff}{terms[int(v.VarName[5:])]}"
                first_term = False
            print(
                f"%8s | %{max_len}s = %3s"
                % (v.VarName, terms[int(v.VarName[5:])], pp(v.X))
                + f" | {cost}"
            )

    # for v in m.getVars():
    #     if v.VarName.startswith("error_"):  # NOTE
    #         print('%s %g' % (v.VarName, v.X))

    expr = expr.strip()
    print("------------------------------------------")
    print(f"Time: {round(m.runTime, 2)}s")
    print("Optimal objective: %g" % m.ObjVal)
    print("------------------------------------------", end=" ")
    m.printStats()
    print("------------------------------------------", end=" ")
    m.printQuality()
    print("------------------------------------------")
    print(f"milp property: {expr} = 0 ({m.ObjVal}) (block: {blocked}) (bound: {bound})")
    print("------------------------------------------")

    return (
        m.Status,
        expr,
        m.ObjVal,
        sorted(term_costs.keys(), key=lambda x: term_costs[x]),
    )
