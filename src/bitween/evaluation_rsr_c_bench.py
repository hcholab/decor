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
    equations = infer_invariants(file_path, func_name, max_degree=2, n=200, milp=glpk)

    def f(x):
        return sympy.exp(x)

    for eqts in equations.values():
        for eqt in eqts:
            assert verify(eqt.lhs, f)


def exp_math():
    file_path = "./benchmarks/bitween/rsr-benchs/euler.c"
    func_name = "euler"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=200, milp=glpk
    )


def exp_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/euler_taylor.c"
    func_name = "euler_taylor"

    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def sin():
    file_path = "./benchmarks/bitween/rsr-benchs/sine.c"
    func_name = "sine"

    # NOTE: civl cannot verify this, therefore we use our own verify function
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


def sin_taylor_1():
    file_path = "./benchmarks/bitween/rsr-benchs/sine_taylor_1.c"
    func_name = "sine_taylor_1"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def sinh_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/sinh_taylor.c"
    func_name = "sinh_taylor"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def tanh_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/tanh_taylor.c"
    func_name = "tanh_taylor"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def sigmoid():
    file_path = "./benchmarks/bitween/rsr-benchs/sigmoid.c"
    func_name = "sigmoid"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=200, milp=glpk
    )


def sigmoid_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/sigmoid_taylor.c"
    func_name = "sigmoid_taylor"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def exp1():
    file_path = "./benchmarks/bitween/rsr-benchs/euler1.c"
    func_name = "euler1"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


def exp1_taylor():
    file_path = "./benchmarks/bitween/rsr-benchs/euler1_taylor.c"
    func_name = "euler1_taylor"

    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=150, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK
    gurobi = settings.MILPSolver.GUROBI

    st = time()

    # identity()
    # exp()
    # exp_math()
    exp_taylor()  # NOTE: civl gives error
    # sigmoid()
    # sigmoid_taylor()  # NOTE: civl cannot verify this
    # exp1()
    # exp1_taylor()
    # sin()  # NOTE: civl cannot verify this, therefore we use our own verify function
    # sin_taylor()  # NOTE: civl verifies this
    # sin_taylor_1()  # NOTE: civl verifies this
    # sinh_taylor()  # NOTE: civl verifies this
    # tanh_taylor()  # NOTE: civl verifies this

    log.debug(f"Total Time: {time() - st:.2f}s")
