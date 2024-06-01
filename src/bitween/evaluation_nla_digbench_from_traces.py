from bitween.config import Config

config = Config()

file_path = "benchmarks/bitween/dig/bresenham.dig.traces.csv"  # NOTE: NO NEED MILP
# file_path = "benchmarks/bitween/dig/cohencu.dig.dyn.traces.csv"  # NOTE: NO NEED MILP
# file_path = "benchmarks/bitween/dig/cohendiv.dig.dyn.traces.csv"  # NOTE: NO NEED MILP
# file_path = "benchmarks/bitween/dig/dijkstra.dig.dyn.traces.csv"  # NOTE: NO NEED MILP
# file_path = "benchmarks/bitween/dig/egcd.dig.dyn.traces.csv"  # NOTE: NO NEED MILP / ForwardSelection performs well
# file_path = "benchmarks/bitween/dig/egcd2.dig.dyn.traces.csv"  # NOTE: NO NEED MILP
# file_path = "benchmarks/bitween/dig/egcd3.dig.dyn.traces.csv"  # NOTE: NO NEED MILP / COMPARE this with egcd2
# file_path = "benchmarks/bitween/dig/fermat1.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/fermat2.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/freire1_int.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/freire1.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/freire2.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/geo1.dig.traces.csv"
# file_path = "benchmarks/bitween/dig/geo2.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/geo3.dig.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/hard.dig.traces.csv"
# file_path = "benchmarks/bitween/dig/knuth.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/lcm1.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/lcm2.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/mannadiv.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/prod4br.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/prodbin.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/ps1.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/ps2.dig.dyn.traces.csv"  # NOTE: Check on DIG
# file_path = "benchmarks/bitween/dig/ps3.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/ps4.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/ps5.dig.dyn.traces.csv"  # NOTE: Check on BITWEEN
# file_path = "benchmarks/bitween/dig/ps5.dig.dyn.traces1.csv"  # NOTE: Check on BITWEEN
# file_path = "benchmarks/bitween/dig/ps5.dig.traces.csv"  # NOTE: Check on BITWEEN
# file_path = "benchmarks/bitween/dig/ps6.dig.traces.csv"  # NOTE: Check on BITWEEN
# file_path = "benchmarks/bitween/dig/sqrt1.dig.traces.csv"

# file_path = "benchmarks/bitween/dig/poly3.dig.dyn.traces1.csv"
# file_path = "benchmarks/bitween/dig/poly3.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/poly4.dig.dyn.traces.csv"
# file_path = "benchmarks/bitween/dig/poly5.dig.dyn.traces.csv"

config.file_path = file_path

if __name__ == "__main__":
    from bitween.main import bitween

    bitween()
