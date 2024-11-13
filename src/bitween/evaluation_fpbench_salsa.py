from time import time
from bitween.main import infer_invariants
from bitween import miscs
from bitween.config import Config, MILPSolver


config = Config()
log = miscs.getLogger(__name__, config.logger_level)


def odometry():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "Odometry"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=None)


def pid():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "PID"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=None)


def runge_kutta_4():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "Runge_Kutta_4"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=None)


def lead_lag_system():
    file_path = "./benchmarks/bitween/fpcore/salsa.c"
    func_name = "Lead_lag_System"
    infer_invariants(file_path, func_name, max_degree=2, n=10, milp=None)


if __name__ == "__main__":

    solver = MILPSolver.GUROBI

    start = time()

    # odometry()
    pid()
    # runge_kutta_4()
    # lead_lag_system()

    end = time()
    print(f"Total time: {end - start}")
