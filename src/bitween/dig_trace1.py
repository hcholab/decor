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
            traces[trace_type] = {"terms": [name[2:] for name in values], "data": []}
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
vtrace1; I X; I Y; I x; I y; I v
vtrace1; 298; 288; 150; 145; 258
vtrace1; 295; 15; 189; 10; -495
vtrace1; 274; 276; 174; 174; 974
vtrace1; 274; 289; 106; 106; 3484
vtrace1; 293; 14; 70; 3; -63
vtrace1; 274; 276; 212; 212; 1126
vtrace1; 16; 25; 4; 4; 106
vtrace1; 271; 12; 5; 0; -127
vtrace1; 289; 24; 2; 0; -145
vtrace2; I X; I Y; I x; I y; I v
vtrace2; 287; 13; 288; 13; -235
vtrace2; 2; 294; 3; 3; 2338
vtrace2; 1; 274; 2; 2; 1639
vtrace2; 4; 13; 5; 5; 112
vtrace2; 284; 8; 285; 8; -252
vtrace2; 7; 13; 8; 8; 115
vtrace2; 297; 9; 298; 9; -261
vtrace2; 19; 6; 20; 6; 5
vtrace2; 270; 29; 271; 29; -154
vtrace2; 3; 287; 4; 4; 2843
vtrace2; 3; 11; 4; 4; 83
vtrace2; 4; 10; 5; 5; 76
vtrace2; 295; 11; 296; 11; -251
"""
parsed_data = parse_input_to_ndarrays_with_vars(input_data)
for trace, content in parsed_data.items():
    print(f"{trace}")
    print(f"{content['terms']}")
    print(f"{content['data']}\n")
