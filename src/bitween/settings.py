# FILE_PATH = "benchmarks/bitween/dig/bresenham.dig.dyn.traces"
FILE_PATH = "benchmarks/bitween/dig/cohencu.dig.dyn.traces"
# FILE_PATH = "benchmarks/bitween/dig/cohendiv.dig.dyn.traces"
# FILE_PATH = "benchmarks/bitween/dig/dijkstra.dig.dyn.traces"
# FILE_PATH = "benchmarks/bitween/dig/egcd.dig.dyn.traces"

# FILE_PATH = "benchmarks/bitween/dig/poly3.dig.dyn.traces.csv"
# FILE_PATH = "benchmarks/bitween/dig/poly4.dig.dyn.traces.csv"
# FILE_PATH = "benchmarks/bitween/dig/poly5.dig.dyn.traces.csv"

LOGGER_LEVEL = 3

DEGREE = 2
DELTA = 0.2  # Property Test threshold

TYPE = "INT"  # INT or REAL

# NOTE: Multiple Regression Method
MULTIPLE_REGRESSION = False  # if True, then we use the multiple regression methods
CROSS_VALIDATION = 5

# NOTE: Regression Refinement Method
REGRESSION_REFINEMENT = True  # if True, then use the regression refinement algorithm

# NOTE: Equation inference parameters for Regression-based Methods
COEFF_THRESHOLD = 0.1  # remove coefficients that are smaller than this value
USE_CUTOFF = True  # if True, then we use the cutoffs
COEFF_CUTOFF = 30  # remove equalities that are larger than this value
INTERCEPT_CUTOFF = 50  # remove equalities that are larger than this value

# NOTE: MILP Method parameters
MILP = True  # if True, then we use the MILP solver after the regression-based methods
MILP_SOLVER = "GUROBI"  # PULP or GUROBI
OBJECTIVE_THRESHOLD = 1e-9
MILP_BOUND = 20
MILP_TIME_LIMIT = 3  # in seconds
PARALLEL_MILP = True  # if True, then we use the parallel MILP solver
FULL_MILP = False  # if True, then use MILP from all data points for each pivot


# NOTE: Equation inference parameters for Regression-based Methods
COEFF_THRESHOLD = 0.1  # remove coefficients that are smaller than this value
USE_CUTOFF = True  # if True, then we use the cutoffs
COEFF_CUTOFF = 30  # remove equalities that are larger than this value
INTERCEPT_CUTOFF = 50  # remove equalities that are larger than this value

# NOTE: Reductions
UGLY_FACTOR = 20  # remove equalities that have lots of terms and "large" coefficients

# NOTE: Z3
SOLVER_TIMEOUT = 10  # in seconds
SLOW_SIMPLIFY = True  # simplify results, e.g., removing weaker invariants
CONSISTENCY_CHECK = False  # if True, then we use the consistency check method
