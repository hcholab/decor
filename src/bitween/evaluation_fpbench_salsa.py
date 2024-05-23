from bitween.main import infer_invariants
from bitween import miscs
from bitween.config import Config, MILPSolver

from time import time

config = Config()
log = miscs.getLogger(__name__, config.logger_level)


def odometry():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "Odometry"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=solver)


def pid():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "PID"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=solver)


if __name__ == "__main__":

    solver = MILPSolver.GUROBI

    start = time.time()

    # odometry()
    pid()

    end = time.time()
    print(f"Total time: {end - start}")
