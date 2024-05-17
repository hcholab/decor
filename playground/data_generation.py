import random
import csv

# Number of features and samples
num_features = 10
num_samples = 20

# Generate the table of data
data = []
header = [f"Feature {i+1}" for i in range(num_features)]
data.append(header)  # Add the header row to the data table
for _ in range(num_samples):
    row = [random.randint(1, 100) for _ in range(num_features)]
    data.append(row)

# Write data to a CSV file
filename = "x.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Data written to {filename}")
