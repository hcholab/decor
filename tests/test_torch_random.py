import torch
import sympy as sp
import csv
from time import process_time


def evaluate_expression(expr, symbols, values):
    subs = {symbol: value for symbol, value in zip(symbols, values)}
    return float(expr.subs(subs))


def generate_degree_2_terms_tensor(x0_tensor, x1_tensor):
    x0x1_tensor = x0_tensor * x1_tensor
    x0_square_tensor = x0_tensor * x0_tensor
    x1_square_tensor = x1_tensor * x1_tensor

    sin_x0_tensor = torch.sin(x0_tensor)
    sin_x1_tensor = torch.sin(x1_tensor)
    sin_x0x1_tensor = torch.sin(x0x1_tensor)
    sin_x0_square_tensor = torch.sin(x0_square_tensor)
    sin_x1_square_tensor = torch.sin(x1_square_tensor)

    return (
        x0_tensor,
        x1_tensor,
        x0x1_tensor,
        x0_square_tensor,
        x1_square_tensor,
        sin_x0_tensor,
        sin_x1_tensor,
        sin_x0x1_tensor,
        sin_x0_square_tensor,
        sin_x1_square_tensor,
    )


if __name__ == "__main__":
    symbols = sp.symbols(
        "x0 x1 x0x1 x0_square x1_square sin_x0 sin_x1 sin_x0x1 sin_x0_square sin_x1_square"
    )
    user_expr = sp.sympify(input("Enter the function in terms of the symbols: "))

    t0 = process_time()
    # Define the number of random samples you'd like to generate
    num_samples = 1000

    # Generate random numbers for x0 and x1 using PyTorch
    x0_tensor = torch.FloatTensor(num_samples).uniform_(-10, 10)
    x1_tensor = torch.FloatTensor(num_samples).uniform_(-10, 10)

    # Generate degree 2 and sine terms using tensors
    tensors = generate_degree_2_terms_tensor(x0_tensor, x1_tensor)

    y_tensor = torch.zeros(num_samples)

    # Evaluate the function in parallel for all tensor values
    for i in range(num_samples):
        y_tensor[i] = evaluate_expression(
            user_expr, symbols, [tensor[i].item() for tensor in tensors]
        )

    # Write to CSV file
    with open("results.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = [
            "x0",
            "x1",
            "x0x1",
            "x0_square",
            "x1_square",
            "sin_x0",
            "sin_x1",
            "sin_x0x1",
            "sin_x0_square",
            "sin_x1_square",
            "y",
        ]
        csvwriter.writerow(headers)
        for data in zip(*tensors, y_tensor):
            csvwriter.writerow([value.item() for value in data])

    print("Results written to results.csv")
    t1 = process_time()
    print(f"Total time with gpu: {t1-t0}")
