from bitween.main import infer_invariants_and_check_correctness
from bitween import miscs, settings

from time import time

log = miscs.getLogger(__name__, settings.LOGGER_LEVEL)


def bresenham():
    file_path = "./benchmarks/bitween/dig/bresenham.c"
    func_name = "bresenham"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=solver
    )


def cohencu():
    file_path = "./benchmarks/bitween/dig/cohencu.c"
    func_name = "cohencu"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=solver
    )


def cohendiv():
    file_path = "./benchmarks/bitween/dig/cohendiv.c"
    func_name = "cohendiv"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=25, milp=solver
    )


def dijkstra():
    file_path = "./benchmarks/bitween/dig/dijkstra.c"
    func_name = "dijkstra"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=20, bound=16, milp=solver
    )


def divbin():
    file_path = "./benchmarks/bitween/dig/divbin.c"
    func_name = "divbin"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=solver
    )


def egcd():
    file_path = "./benchmarks/bitween/dig/egcd.c"
    func_name = "egcd"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=25, milp=solver
    )


def egcd2():
    file_path = "./benchmarks/bitween/dig/egcd2.c"
    func_name = "egcd2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=solver
    )


# NOTE: Dig and SymInfer cannot infer the invariants for this function for vtrace1 and vtrace2
def egcd3():
    file_path = "./benchmarks/bitween/dig/egcd3.c"
    func_name = "egcd3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=18, milp=solver
    )


def fermat1():
    file_path = "./benchmarks/bitween/dig/fermat1.c"
    func_name = "fermat1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=200, milp=solver
    )


def fermat2():
    file_path = "./benchmarks/bitween/dig/fermat2.c"
    func_name = "fermat2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=200, milp=solver
    )


def freire1_int():
    file_path = "./benchmarks/bitween/dig/freire1_int.c"
    func_name = "freire1_int"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def freire1():
    file_path = "./benchmarks/bitween/dig/freire1.c"
    func_name = "freire1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


# TODO: Discuss this with the team: casting in properties
def freire2():
    file_path = "./benchmarks/bitween/dig/freire2.c"
    func_name = "freire2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=20, milp=solver
    )


def geo1():
    file_path = "./benchmarks/bitween/dig/geo1.c"
    func_name = "geo1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def geo2():
    file_path = "./benchmarks/bitween/dig/geo2.c"
    func_name = "geo2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=solver
    )


def geo3():
    file_path = "./benchmarks/bitween/dig/geo3.c"
    func_name = "geo3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=60, milp=solver
    )


def hard():
    file_path = "./benchmarks/bitween/dig/hard.c"
    func_name = "hard"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def knuth():
    file_path = "./benchmarks/bitween/dig/knuth.c"
    func_name = "knuth"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=100, bound=8, milp=solver
    )


def lcm1():
    file_path = "./benchmarks/bitween/dig/lcm1.c"
    func_name = "lcm1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def lcm2():
    file_path = "./benchmarks/bitween/dig/lcm2.c"
    func_name = "lcm2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def mannadiv():
    file_path = "./benchmarks/bitween/dig/mannadiv.c"
    func_name = "mannadiv"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def prod4br():
    file_path = "./benchmarks/bitween/dig/prod4br.c"
    func_name = "prod4br"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def prodbin():
    file_path = "./benchmarks/bitween/dig/prodbin.c"
    func_name = "prodbin"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


def ps1():
    file_path = "./benchmarks/bitween/dig/ps1.c"
    func_name = "ps1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=1, n=10, milp=solver
    )


def ps2():
    file_path = "./benchmarks/bitween/dig/ps2.c"
    func_name = "ps2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, bound=4, milp=solver
    )


def ps3():
    file_path = "./benchmarks/bitween/dig/ps3.c"
    func_name = "ps3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=3, n=10, milp=solver
    )


def ps4():
    file_path = "./benchmarks/bitween/dig/ps4.c"
    func_name = "ps4"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=4, n=12, milp=solver
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
        n=8,
        milp=solver,
        method=settings.InitialMethod.FORWARD_SELECTION,
    )


def sqrt1():
    file_path = "./benchmarks/bitween/dig/sqrt1.c"
    func_name = "sqrt1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=solver
    )


if __name__ == "__main__":

    solver = settings.MILPSolver.GUROBI

    st = time()

    # bresenham()
    # cohencu()
    # cohendiv()
    # dijkstra()
    # divbin()
    # egcd()
    # egcd2()
    # egcd3()
    # fermat1()
    # fermat2()
    # freire1_int()
    # freire1()
    # freire2()
    # geo1()
    # geo2()
    # geo3()
    # hard()
    knuth()
    # lcm1()
    # lcm2()
    # mannadiv()
    # prod4br()
    # prodbin()
    # ps1()
    # ps2()
    # ps3()
    # ps4()
    # ps5()
    # ps6()
    # sqrt1()

    log.debug(f"Total Time: {time() - st:.2f}s")
