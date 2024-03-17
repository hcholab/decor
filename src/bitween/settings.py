LOGGER_LEVEL = 3

DEGREE = 2

MULTIPLE_REGRESSION = False
CROSS_VALIDATION = 5

MILP = False  # use MILP solver
OBJECTIVE_THRESHOLD = 1e-9
MILP_BOUND = 12


UGLY_FACTOR = 20  # remove equalities that have lots of terms and "large" coefficients
# coeff_threshold
COEFF_THRESHOLD = 0.3  # remove coefficients that are smaller than this value
COEFF_CUTOFF = 30  # remove equalities that are larger than this value
INTERCEPT_CUTOFF = 50  # remove equalities that are larger than this value
# MILP: don't include objective if it's greater than this value
DELTA = 0.2  # Property Test threshold
