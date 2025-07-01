#!/usr/bin/env python3
import numpy as np
import sympy as sp
from sympy.calculus.util import continuous_domain

from bitween.main import process_trace, find_model, infer_equations
from bitween.config import Config

# ----------------------------------------------------------------------------
# Declare SymPy symbols and the function as a SymPy expression
x, a = sp.symbols("x a", real=True)
f_sym = sp.log(1+x)                # ← change this line to your desired f(x)

# 1a) Automatically get a NumPy‐callable version
f_callable = sp.lambdify(x, f_sym, "numpy")

# ----------------------------------------------------------------------------
# Compute continuous domains for x and for a
dom_x = continuous_domain(f_sym,            x, sp.S.Reals)
# domain for a by substituting x→a
dom_a = continuous_domain(f_sym.subs(x, a), a, sp.S.Reals)

# Enforce x - a ∈ dom_x by sampling a < x - lb_x
lb_x = dom_x.start if dom_x.start != -sp.oo else 0
#                                  ^ for log, lb_x = 0

# Turn symbolic intervals into numeric bounds [ε, M]
ε, M = 1e-6, 10.0

def get_bounds(interval):
    low = float(interval.start) + ε if interval.start != -sp.oo else ε
    high = float(interval.end) - ε if interval.end    !=  sp.oo else M
    return low, high

low_x,  high_x  = get_bounds(dom_x)
low_a,  high_a  = get_bounds(dom_a)

# Sample (x,a) so that x∈dom_x, a∈dom_a, and x - a ∈ dom_x
def sample_xy(N: int):
    xs, as_ = [], []
    while len(xs) < N:
        xv = np.random.uniform(low_x, high_x)
        # enforce a < x - lb_x
        ub_a_eff = min(high_a, xv - float(lb_x) - ε)
        if ub_a_eff <= low_a:
            continue
        av = np.random.uniform(low_a, ub_a_eff)
        xs.append(xv)
        as_.append(av)
    return np.array(xs), np.array(as_)

def discover_relation(f, a_vals, x_vals):
    cfg = Config()
    cfg.degree                = 5
    cfg.epsilon               = 1e-3
    cfg.milp_enabled          = False #We don't have a license for this
    cfg.regression_refinement = True

    xs, a_arr = np.asarray(x_vals), np.asarray(a_vals)
    f_vals  = f(xs)
    f_minus = f(xs - a_arr)
    f_a     = f(a_arr)

    mask = np.isfinite(f_vals) & np.isfinite(f_minus) & np.isfinite(f_a)
    xs, a_arr = xs[mask], a_arr[mask]
    f_vals, f_minus, f_a = f_vals[mask], f_minus[mask], f_a[mask]

    data = np.column_stack([f_minus, f_a, f_vals])
    terms = ["f_x_minus_a", "f_a", "f_x"]
    ext_terms, ext_data = process_trace(terms, data, cfg.degree)

    model_dict = {p: find_model(p, ext_terms, ext_data) for p in ext_terms}
    equations, _ = infer_equations(model_dict, ext_terms, ext_data)

    f_x, f_a_sym, f_x_minus_a = sp.symbols("f_x f_a f_x_minus_a")
    for eq in equations:
        if eq.error >= cfg.epsilon:
            continue
        expr = sp.sympify(str(eq.expr), locals={
            "f_x":         f_x,
            "f_a":         f_a_sym,
            "f_x_minus_a": f_x_minus_a
        })
        expr = sp.simplify(expr)
        sols = sp.solve(expr, f_x)
        for sol in sols:
            if sol == f_x or sol.has(f_x):
                continue
            f_num = sp.lambdify((f_x_minus_a, f_a_sym), sol, "numpy")
            pred  = f_num(f_minus, f_a)
            if np.allclose(pred, f_vals, atol=cfg.epsilon, rtol=0):
                return sp.Eq(f_x, sp.ratsimp(sol))
    return None

if __name__ == "__main__":
    N = 200
    x_vals, a_vals = sample_xy(N)
    relation = discover_relation(f_callable, a_vals, x_vals)
    print("Discovered:", relation)