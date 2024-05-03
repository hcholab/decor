from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
)
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def bresenham():
    file_path = "./benchmarks/bitween/dig/bresenham.c"
    func_name = "bresenham"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def cohencu():
    file_path = "./benchmarks/bitween/dig/cohencu.c"
    func_name = "cohencu"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=glpk
    )


def cohendiv():
    file_path = "./benchmarks/bitween/dig/cohendiv.c"
    func_name = "cohendiv"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=25, milp=None
    )


def dijkstra():
    file_path = "./benchmarks/bitween/dig/dijkstra.c"
    func_name = "dijkstra"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=20, bound=16, milp=glpk
    )


def divbin():
    file_path = "./benchmarks/bitween/dig/divbin.c"
    func_name = "divbin"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def egcd():
    file_path = "./benchmarks/bitween/dig/egcd.c"
    func_name = "egcd"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=25, milp=glpk
    )


def egcd2():
    file_path = "./benchmarks/bitween/dig/egcd2.c"
    func_name = "egcd2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


# NOTE: Dig and SymInfer cannot infer the invariants for this function for vtrace1 and vtrace2
def egcd3():
    file_path = "./benchmarks/bitween/dig/egcd3.c"
    func_name = "egcd3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=18, milp=glpk
    )


def fermat1():
    file_path = "./benchmarks/bitween/dig/fermat1.c"
    func_name = "fermat1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=200, milp=glpk
    )


def fermat2():
    file_path = "./benchmarks/bitween/dig/fermat2.c"
    func_name = "fermat2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=200, milp=glpk
    )


def freire1_int():
    file_path = "./benchmarks/bitween/dig/freire1_int.c"
    func_name = "freire1_int"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def freire1():
    file_path = "./benchmarks/bitween/dig/freire1.c"
    func_name = "freire1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


# TODO: Discuss this with the team: casting in properties
def freire2():
    file_path = "./benchmarks/bitween/dig/freire2.c"
    func_name = "freire2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=20, milp=glpk
    )


def geo1():
    file_path = "./benchmarks/bitween/dig/geo1.c"
    func_name = "geo1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def geo2():
    file_path = "./benchmarks/bitween/dig/geo2.c"
    func_name = "geo2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=glpk
    )


def geo3():
    file_path = "./benchmarks/bitween/dig/geo3.c"
    func_name = "geo3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=60, milp=glpk
    )


def hard():
    file_path = "./benchmarks/bitween/dig/hard.c"
    func_name = "hard"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def knuth():
    file_path = "./benchmarks/bitween/dig/knuth.c"
    func_name = "knuth"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=100, bound=8, milp=glpk
    )


def lcm1():
    file_path = "./benchmarks/bitween/dig/lcm1.c"
    func_name = "lcm1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def lcm2():
    file_path = "./benchmarks/bitween/dig/lcm2.c"
    func_name = "lcm2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=glpk
    )


def mannadiv():
    file_path = "./benchmarks/bitween/dig/mannadiv.c"
    func_name = "mannadiv"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def prod4br():
    file_path = "./benchmarks/bitween/dig/prod4br.c"
    func_name = "prod4br"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def prodbin():
    file_path = "./benchmarks/bitween/dig/prodbin.c"
    func_name = "prodbin"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def ps1():
    file_path = "./benchmarks/bitween/dig/ps1.c"
    func_name = "ps1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=1, n=10, milp=glpk
    )


def ps2():
    file_path = "./benchmarks/bitween/dig/ps2.c"
    func_name = "ps2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, bound=4, milp=glpk
    )


def ps3():
    file_path = "./benchmarks/bitween/dig/ps3.c"
    func_name = "ps3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=10, milp=glpk
    )


def ps4():
    file_path = "./benchmarks/bitween/dig/ps4.c"
    func_name = "ps4"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=4, n=12, milp=glpk
    )


def ps5():
    file_path = "./benchmarks/bitween/dig/ps5.c"
    func_name = "ps5"
    infer_invariants_and_check_correctness(
        file_path,
        func_name,
        max_degree=5,
        n=10,
        milp=None,
        method=settings.InitialMethod.FORWARD_SELECTION,
    )


def ps6():
    file_path = "./benchmarks/bitween/dig/ps6.c"
    func_name = "ps6"
    infer_invariants_and_check_correctness(
        file_path,
        func_name,
        max_degree=6,
        n=20,
        milp=glpk,
        method=settings.InitialMethod.FORWARD_SELECTION,
    )


def sqrt1():
    file_path = "./benchmarks/bitween/dig/sqrt1.c"
    func_name = "sqrt1"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


if __name__ == "__main__":

    glpk = settings.MILPSolver.GLPK

    st = time()

    # bresenham()
    # cohencu() # NOTE: use this in demo
    cohendiv()  # may generates an unsound invariant and we catch it in the check_correctness 4
    # dijkstra()
    # divbin()
    # egcd()  # NOTE: use this in demo 3
    # egcd2()
    # egcd3()
    # fermat1() # NOTE: use this in demo
    # fermat2()
    # freire1_int()
    # freire1()  # NOTE: use this in demo 2
    # freire2()
    # geo1()
    # geo2()
    # geo3()
    # hard()
    # knuth()  # NOTE: May generate unsound invariants and we catch it in the check_correctness
    # lcm1()
    # lcm2()  # NOTE: use this in demo
    # mannadiv()
    # prod4br()
    # prodbin()
    # ps1()
    # ps2()
    # ps3()
    # ps4()
    # ps5()
    # ps6()
    # sqrt1()  # NOTE: use this in demo 1

    log.debug(f"Total Time: {time() - st:.2f}s")
