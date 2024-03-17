LOGGER_LEVEL = 3

DEGREE = 2

DELTA = 0.2  # Property Test threshold

# NOTE: Multiple Regression Method
MULTIPLE_REGRESSION = False  # if True, then we use the multiple regression methods
CROSS_VALIDATION = 5

# NOTE: Regression Refinement Method
REGRESSION_REFINEMENT = False  # if True, then use the regression refinement algorithm

# NOTE: MILP Method parameters
MILP = False  # if True, then we use the MILP solver after the regression-based methods
OBJECTIVE_THRESHOLD = 1e-9
MILP_BOUND = 12

# NOTE: Equation inference parameters for Regression-based Methods
COEFF_THRESHOLD = 0.3  # remove coefficients that are smaller than this value
COEFF_CUTOFF = 30  # remove equalities that are larger than this value
INTERCEPT_CUTOFF = 50  # remove equalities that are larger than this value

# NOTE: Reductions
UGLY_FACTOR = 20  # remove equalities that have lots of terms and "large" coefficients
