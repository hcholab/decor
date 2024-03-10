import numpy as np


def parse_input_to_ndarrays_with_vars(input_data):
    # Splitting the input data into lines
    lines = input_data.strip().split("\n")

    # Dictionary to store the data and variable names for each trace type
    traces = {}

    # Processing each line
    for line in lines:
        parts = line.split("; ")
        trace_type = parts[0]
        values = parts[1:]

        # Handle header lines
        if "I " in values[0]:
            # Strip 'I ' from the names and store them as variable names
            traces[trace_type] = {"vars": [name[2:] for name in values], "data": []}
            continue

        # Check if the trace type is already initialized
        if trace_type not in traces:
            continue

        # Append the data to the respective list in the trace
        traces[trace_type]["data"].append([int(value) for value in values])

    # Convert data lists to numpy arrays
    for trace in traces:
        traces[trace]["data"] = np.array(traces[trace]["data"])

    return traces


# Example usage
input_data = """
traceA; I alpha; I beta; I gamma
traceA; 1; 2; 3
traceA; 4; 5; 6
traceB; I delta; I epsilon; I zeta; I eta
traceB; 7; 8; 9; 10
traceB; 11; 12; 13; 14
"""

parsed_data = parse_input_to_ndarrays_with_vars(input_data)
for trace, content in parsed_data.items():
    print(f"{trace} Variables: {content['vars']}")
    print(f"{trace} Data:\n{content['data']}\n")
