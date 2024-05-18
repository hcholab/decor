import csv
import torch

# Your tensors
rs = [
    torch.tensor([0.7014, -1.9394, 0.5573], device="mps:0"),
    torch.tensor([-2.1858, -6.8175, -8.9779], device="mps:0"),
]

# Convert tensors to lists
x0_values = rs[0].cpu().numpy().tolist()
x1_values = rs[1].cpu().numpy().tolist()

# Write to CSV
with open("output.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(["x0", "x1"])

    # Write data
    for x0, x1 in zip(x0_values, x1_values):
        csv_writer.writerow([x0, x1])
