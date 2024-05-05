import sympy
from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
    infer_invariants,
    verify,
)
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def identity():
    file_path = "./benchmarks/bitween/rsr-benchs/identity.c"
    func_name = "identity"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=1, n=40, milp=glpk
    )


def exp():
    file_path = "./benchmarks/bitween/rsr-benchs/euler.c"
    func_name = "euler"

    # NOTE: civl cannot verify this, therefore we use our own verify function
    # infer_invariants_and_verify_correctness(
    #     file_path, func_name, max_degree=2, n=200, milp=glpk
    # )

    equations = infer_invariants(file_path, func_name, max_degree=2, n=200, milp=glpk)

    def f(x):
        return sympy.exp(x)

    for eqts in equations.values():
        for eqt in eqts:
            assert verify(eqt.lhs, f)


def sin():
    file_path = "./benchmarks/bitween/rsr-benchs/sine.c"
    func_name = "sine"

    # NOTE: civl cannot verify this, therefore we use our own verify function
    # infer_invariants_and_verify_correctness(
    #     file_path, func_name, max_degree=2, n=150, milp=glpk
    # )

    equations = infer_invariants(file_path, func_name, max_degree=2, n=200, milp=glpk)

    def f(x):
        return sympy.sin(x)

    for eqts in equations.values():
        for eqt in eqts:
            assert verify(eqt.lhs, f)


def sin_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/sine_taylor.c"
    func_name = "sine_taylor"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK

    st = time()

    # identity()
    # exp()
    # sin() # NOTE: civl cannot verify this, therefore we use our own verify function
    sin_taylor()  # NOTE: civl verifies this

    log.debug(f"Total Time: {time() - st:.2f}s")
