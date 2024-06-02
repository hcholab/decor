# Bitween 

HERE GOES THE DESCRIPTION

## Installation

You can install `bitween` via pip from [PyPI](https://pypi.org/project/bitween/):

NOTE: This package is not yet available on PyPI. You can install it from the source code.

```bash
$ pip install bitween 
```

## Usage

From the command line, on the root of the project, you can run the following command:

```bash
python src/bitween/run.py -f benchmarks/bitween/dig/cohendiv.c -m cohendiv -n 15 --correctness verification
```

```bash
python src/bitween/run.py -h                                                                               

```
usage: bitween -f <file_path> -n <func_name> [options]

Run analysis based on provided configurations.

options:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file_path FILE_PATH
                        Path to the input file.
  -m FUNC_NAME, --func_name FUNC_NAME
                        Name of the function to analyze.
  -d DEGREE, --degree DEGREE
                        Degree of the polynomial (default: 2).
  -n N                  Number of samples to collect (default: 20).
  --correctness {verification,fuzzing}
                        Check or verify correctness of inferred invariants.
  --epsilon EPSILON     Tolerance for squared error (default: 0.001).
  --delta DELTA         Delta value (default: 0.2).
  --precision PRECISION
                        Precision for floating-point numbers (default: 2).
  --method {MULTIPLE_REGRESSION,SIMPLE_REGRESSION,FORWARD_SELECTION,EAGER_MILP,PYSR,GPLEARN,KAN}
                        Initial method for analysis (default: MULTIPLE_REGRESSION).
  --cross_validation CROSS_VALIDATION
                        Number of cross validations (default: 3).
  --regression_score {NEG_MEAN_SQUARED_ERROR,R2}
                        Regression score method (default: r2).
  --coeff_threshold COEFF_THRESHOLD
                        Coefficient threshold (default: 0.01).
  --use_cutoff USE_CUTOFF
                        Whether to use cutoff (default: True).
  --coeff_cutoff COEFF_CUTOFF
                        Coefficient cutoff value (default: 30).
  --intercept_cutoff INTERCEPT_CUTOFF
                        Intercept cutoff value (default: 50).
  --ugly_factor UGLY_FACTOR
                        Ugly factor for reductions (default: 20).
  --milp {PULP,GUROBI,GLPK}
                        MILP solver to use (default: None).

For more information, visit the documentation.
```

You can also use the .ini file to provide the configurations:

```toml
[general]
degree = 2
epsilon = 0.001 # Tolerance for squared error
delta = 0.2 
precision = 2 # Precision for the floating-point numbers
method = MULTIPLE_REGRESSION  # MULTIPLE_REGRESSION, SIMPLE_REGRESSION, FORWARD_SELECTION, EAGER_MILP, PYSR, GPLEARN, KAN
correctness = FUZZING # FUZZING or VERIFICATION or NONE
n = 20 # Number of data points
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`bitween` was created by Ferhat Erata, Timos Antonopoulos. It is licensed under the terms of the MIT license.

## Credits

`bitween` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
