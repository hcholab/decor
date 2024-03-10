import random
import csv


def vassume(condition):
    return condition


def vtrace1(x, y, q, r, a, b):
    with open("trace_output.csv", "a", newline="") as file:  # Append mode
        file_writer = csv.writer(file)
        file_writer.writerow(["vtrace1", x, y, q, r, a, b])


def vtrace2(x, y, q, r):
    with open("trace_output.csv", "a", newline="") as file:  # Append mode
        file_writer = csv.writer(file)
        file_writer.writerow(["vtrace2", x, y, q, r])


def mainQ(x, y):
    if not vassume(x >= 1 and y >= 1):
        return  # Skip this run if vassume is not met
    q = 0
    r = x
    a = 0
    b = 0
    while True:
        if not (r >= y):
            break
        a = 1
        b = y

        while True:
            vtrace1(x, y, q, r, a, b)
            if not (r >= 2 * b):
                break

            a = 2 * a
            b = 2 * b

        r = r - b
        q = q + a

    vtrace2(x, y, q, r)
    return q


if __name__ == "__main__":
    # Initialize the CSV file with headers
    with open("trace_output.csv", "w", newline="") as file:
        file_writer = csv.writer(file)
        file_writer.writerow(["Trace Type", "X", "Y", "Q", "R", "A", "B"])

    for _ in range(10):  # Number of runs, adjust as needed
        x = random.randint(1, 100)  # Random x between 1 and 100
        y = random.randint(1, 100)  # Random y between 1 and 100
        mainQ(x, y)
