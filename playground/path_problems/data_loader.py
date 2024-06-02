import os


def load_data(file_name):
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the data file relative to the project root
    data_path = os.path.join(current_dir, "data", file_name)
    with open(data_path, "r") as file:
        data = file.read()
    return data


print(load_data("data.txt"))
