from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
)
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def addsub():
    file_path = "./benchmarks/bitween/float-benchs/_addsub.c"
    func_name = "_addsub"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def arctan_Pade():
    file_path = "./benchmarks/bitween/float-benchs/_arctan_Pade.c"
    func_name = "_arctan_Pade"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def cos_polynomial():
    file_path = "./benchmarks/bitween/float-benchs/_cos_polynomial.c"
    func_name = "_cos_polynomial"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def exp_loop():
    file_path = "./benchmarks/bitween/float-benchs/_exp_loop.c"
    func_name = "_exp_loop"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK

    st = time()

    # addsub()
    arctan_Pade()  # NOTE: This is the function that we are interested in
    # cos_polynomial()
    # exp_loop()

    log.debug(f"Total Time: {time() - st:.2f}s")
