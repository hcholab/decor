from bitween.main import (  # noqa F401
    infer_invariants_and_check_correctness,
    infer_invariants_and_verify_correctness,
)
from bitween import miscs
from bitween.config import Config, Method, MILPSolver
import numpy as np

from time import time

config = Config()
log = miscs.getLogger(__name__, config.logger_level)


def bresenham():
    file_path = "./benchmarks/bitween/dig/bresenham.c"
    func_name = "bresenham"
    infer_invariants_and_verify_correctness(
        file_path,
        func_name,
        max_degree=2,
        n=20,
        milp=None,
        # method=Method.FORWARD_SELECTION,
    )


def cohencu():
    file_path = "./benchmarks/bitween/dig/cohencu.c"
    func_name = "cohencu"
    infer_invariants_and_verify_correctness(
        file_path,
        func_name,
        max_degree=3,
        n=10,
        milp=None,
        # method=Method.MULTIPLE_REGRESSION,
    )


def bresenham_extra():
    import statistics

    max_input = 300
    max_iter = 3
    # for each iteration, we will query with different samples (n) and get different errors
    sample_error = {}
    file_path = "./benchmarks/bitween/dig/bresenham.c"
    func_name = "bresenham"
    for i in range(5, max_input, 5):
        e_sum = 0
        s_sample = 0
        error_j = 0
        sample_j = 0
        prop_j = []
        count = 0
        for j in range(max_iter):
            props, error, sample = infer_invariants_and_check_correctness(
                file_path,
                func_name,
                max_degree=2,
                n=i,
                milp=None,
                epsilon=0.2,
                # method=Method.MULTIPLE_REGRESSION,
            )

            if props:
                print("Properties found:")
                for loc, props in props.items():
                    print(f"Loc: {loc}")
                    for prop in props:
                        print(f" {prop}")
                    if not props:
                        continue
                    if loc == "vtrace1":
                        continue
                    e = round(error[loc], 5)
                    print(f"Error: {e}")
                    s = sample[loc]
                    print(f"Sample: {s}")
                    (e_sum, s_sample) = (e_sum + e, s_sample + s)
                if len(props) > 0:
                    error_j += e_sum / len(props)
                    sample_j += s_sample / len(props)
                    prop_j.append(len(props))
                    count += 1
            else:
                print("No properties found")
        if count > 0:
            sample_error[i] = (
                error_j / count,
                sample_j / count,
                statistics.median(prop_j),
            )
        else:
            sample_error[i] = (e_sum, i, 0)

    # create a panda dataset for figure and order by sample
    import pandas as pd

    df = pd.DataFrame(sample_error).T
    df.columns = ["Error", "Sample", "Properties"]
    df = df.sort_values(by="Sample")
    # save the dataset to a csv file
    df.to_csv("bresenham_extra.csv")
    print(df)


def cohendiv():
    file_path = "./benchmarks/bitween/dig/cohendiv.c"
    func_name = "cohendiv"
    infer_invariants_and_verify_correctness(
        file_path,
        func_name,
        max_degree=2,
        n=20,
        milp=None,
        # method=Method.FORWARD_SELECTION,
    )


def dijkstra():
    file_path = "./benchmarks/bitween/dig/dijkstra.c"
    func_name = "dijkstra"
    infer_invariants_and_check_correctness(
        file_path,
        func_name,
        max_degree=3,
        n=20,
        # bound=16,
        # milp=gurobi,
        # method=Method.FORWARD_SELECTION,
    )


def divbin():
    file_path = "./benchmarks/bitween/dig/divbin.c"
    func_name = "divbin"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=None
    )


def egcd():
    file_path = "./benchmarks/bitween/dig/egcd.c"
    func_name = "egcd"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=25, milp=None
    )


def egcd2():
    file_path = "./benchmarks/bitween/dig/egcd2.c"
    func_name = "egcd2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=None
    )


# NOTE: Dig and SymInfer cannot infer the invariants for this function for vtrace1 and vtrace2
def egcd3():
    file_path = "./benchmarks/bitween/dig/egcd3.c"
    func_name = "egcd3"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=18, milp=None
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
        file_path, func_name, max_degree=2, n=20, milp=gurobi
    )


def mannadiv():
    file_path = "./benchmarks/bitween/dig/mannadiv.c"
    func_name = "mannadiv"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=glpk
    )


def petter():
    file_path = "./benchmarks/bitween/dig/petter.c"
    func_name = "petter"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, milp=glpk
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
        method=Method.FORWARD_SELECTION,
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
        method=Method.FORWARD_SELECTION,
    )


def readers_writers():
    file_path = "./benchmarks/bitween/dig/readers_writers.c"
    func_name = "readers_writers"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=20, milp=None
    )


def sqrt1():
    file_path = "./benchmarks/bitween/dig/sqrt1.c"
    func_name = "sqrt1"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=15, method=Method.MULTIPLE_REGRESSION
    )


def wensley2():
    file_path = "./benchmarks/bitween/dig/wensley2.c"
    func_name = "wensley2"
    infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=100, milp=None
    )


def z3sqrt():
    file_path = "./benchmarks/bitween/dig/z3sqrt.c"
    func_name = "z3sqrt"
    props, error, sample = infer_invariants_and_check_correctness(
        file_path, func_name, max_degree=2, n=10, milp=None
    )


def isqrt():
    file_path = "./benchmarks/bitween/dig/isqrt.c"
    func_name = "isqrt"
    infer_invariants_and_verify_correctness(
        file_path, func_name, max_degree=2, n=30, milp=None
    )


if __name__ == "__main__":

    glpk = MILPSolver.GLPK
    gurobi = MILPSolver.GUROBI
    pulp = MILPSolver.PULP

    st = time()

    # bresenham()
    cohencu()  # NOTE: use this in demo
    # bresenham_extra()
    # cohendiv()  # may generates an unsound invariant and we catch it in the check_correctness 4
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
    # petter()
    # prod4br()
    # prodbin()
    # ps1()
    # ps2()
    # ps3()
    # ps4()
    # ps5()
    # ps6()
    # readers_writers()
    # sqrt1()  # NOTE: use this in demo 1
    # wensley2()
    # z3sqrt()
    # isqrt()

    log.debug(f"Total Time: {time() - st:.2f}s")
