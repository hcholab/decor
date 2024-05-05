from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
)
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def division():
    file_path = "./benchmarks/bitween/civl_arithmetic_examples/division.c"
    func_name = "division"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def equivalence():
    file_path = "./benchmarks/bitween/civl_arithmetic_examples/equivalence.c"
    func_name = "equivalence"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=1, n=30, milp=glpk
    )


def mean():
    file_path = "./benchmarks/bitween/civl_arithmetic_examples/mean.c"
    func_name = "mean"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def power_simplify1():
    file_path = "./benchmarks/bitween/civl_arithmetic_examples/power_simplify1.c"
    func_name = "power_simplify1"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK

    st = time()

    # division()
    # equivalence()
    # mean()
    power_simplify1()

    log.debug(f"Total Time: {time() - st:.2f}s")
