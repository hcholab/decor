from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
)
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def addsub():
    file_path = "./benchmarks/bitween/float-benchs/_addsub.c"
    func_name = "addsub"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK

    st = time()

    addsub()

    log.debug(f"Total Time: {time() - st:.2f}s")
