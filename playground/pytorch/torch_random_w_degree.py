import torch
import sympy as sp
import csv

# mps_device = torch.device("mps")
dev = None


# def filter_invalid_columns(terms_list):
#     # Create masks for tensors with NaN, Inf, or complex values
#     nan_mask = [torch.isnan(term_tensor).any() for _, term_tensor in terms_list]
#     inf_mask = [torch.isinf(term_tensor).any() for _, term_tensor in terms_list]
#     complex_mask = [term_tensor.is_complex() for _, term_tensor in terms_list]

#     # Calculate the counts for each mask
#     nan_count = sum(nan_mask)
#     inf_count = sum(inf_mask)
#     complex_count = sum(complex_mask)

#     # Create a union of the masks
#     invalid_mask = [
#         nan or inf or complex_
#         for nan, inf, complex_ in zip(nan_mask, inf_mask, complex_mask)
#     ]

#     # Use the union mask to filter out invalid tensors
#     filtered_terms_list = [
#         (term_name, term_tensor)
#         for (term_name, term_tensor), is_invalid in zip(terms_list, invalid_mask)
#         if not is_invalid
#     ]

#     return filtered_terms_list, nan_count, inf_count, complex_count


def filter_invalid_columns(terms_list):
    # First, filter out tensors with nan or complex values
    terms_list = [
        (term_name, term_tensor)
        for term_name, term_tensor in terms_list
        if not (torch.isnan(term_tensor).any() or term_tensor.is_complex())
    ]

    # Identify which tensors have any inf values
    inf_mask = [torch.isinf(term_tensor).any() for _, term_tensor in terms_list]

    # Count the number of terms that have inf values
    inf_count = sum(inf_mask)

    # Use this mask to filter out tensors with inf values
    filtered_terms_list = [
        (term_name, term_tensor)
        for (term_name, term_tensor), has_inf in zip(terms_list, inf_mask)
        if not has_inf
    ]

    return filtered_terms_list, inf_count


def count_terms(
    num_vars, degree, num_funcs, depth, user_function=False, one_symbol=False
):
    # Count original polynomial terms
    total_terms = 0
    for d in range(1, degree + 1):
        total_terms += len(sp.multinomial_coefficients(num_vars, d))

    if num_funcs == 1:  # Handle edge case where denominator would be zero
        total_after_functions = total_terms * (depth + 1)
    else:
        total_after_functions = (
            total_terms * (1 - num_funcs ** (depth + 1)) / (1 - num_funcs)
        )

    if user_function:
        total_terms += 1

    if one_symbol:
        total_terms += 1

    return int(total_after_functions)


def evaluate_expression(expr, symbols, values):
    subs = {symbol: value for symbol, value in zip(symbols, values)}
    return float(expr.subs(subs))


def generate_terms_tensors(  # noqa: C901
    x_tensors, degree, functions, depth=1, user_function=None, one_symbol=False
):
    # Generate polynomial terms
    num_vars = len(x_tensors)
    all_terms = []

    # Initial polynomial terms
    for d in range(1, degree + 1):
        for combination in sp.multinomial_coefficients(num_vars, d).keys():
            term_tensor = torch.ones_like(x_tensors[0], device=dev)
            term_name = []
            for var_idx, var_power in enumerate(combination):
                term_tensor *= x_tensors[var_idx] ** var_power
                if var_power:
                    term_name.append(f"x{var_idx}**{var_power}")
            term_name = "*".join(term_name)
            all_terms.append((sp.sympify(term_name), term_tensor))

    # Iteratively apply functions based on depth
    depth_terms = all_terms.copy()
    for _ in range(depth):
        terms = []
        for func in functions:
            for term_name, term_tensor in depth_terms:
                new_term_name = sp.sympify(f"{func}({term_name})")
                if func == "sin":
                    new_term_tensor = torch.sin(term_tensor)
                elif func == "cos":
                    new_term_tensor = torch.cos(term_tensor)
                elif func == "tan":
                    new_term_tensor = torch.tan(term_tensor)
                elif func == "log":
                    new_term_tensor = torch.where(
                        term_tensor > 0,
                        torch.log(term_tensor),
                        torch.zeros_like(term_tensor),
                    )
                elif func == "exp":
                    new_term_tensor = torch.exp(term_tensor)
                elif func == "sign":
                    new_term_tensor = torch.sign(term_tensor)
                elif func == "sqrt":
                    new_term_tensor = torch.sqrt(term_tensor)
                elif func == "abs":
                    new_term_tensor = torch.abs(term_tensor)
                elif func == "cot":
                    new_term_tensor = torch.cos(term_tensor) / torch.sin(term_tensor)
                else:
                    raise ValueError(f"Unsupported function: {func}")
                terms.append((new_term_name, new_term_tensor))
        all_terms.extend(terms)  # Add the new terms back
        depth_terms = terms.copy()

    # Add the one-symbol "1" (all ones tensor) to the end
    if one_symbol:
        ones_tensor = torch.ones_like(x_tensors[0], device=dev)
        all_terms.append((sp.sympify("1"), ones_tensor))

    # Add user function to the end if provided
    if user_function is not None:
        if isinstance(user_function, sp.Expr):
            # Prepare a substitution dictionary for SymPy expression
            subs_dict = {sp.symbols(f"x{i}"): x_tensors[i] for i in range(num_vars)}

            for term_name, term_tensor in all_terms.copy():
                # Substitute the tensors into the SymPy expression and evaluate
                new_term_tensor = user_function.subs(subs_dict)
                new_term_name = sp.sympify(f"f({term_name})")
                all_terms.append(
                    (new_term_name, torch.tensor(float(new_term_tensor), device=dev))
                )

        elif callable(user_function):
            for term_name, term_tensor in all_terms.copy():
                new_term_name = sp.sympify(f"user_function({term_name})")
                new_term_tensor = user_function(term_tensor)
                all_terms.append((new_term_name, new_term_tensor))
        else:
            raise ValueError("Unsupported user_function type")

    return all_terms


# Run the test
def test_generate_terms_tensors():
    num_samples = 7

    # # Test for degree 1 with no additional functions
    # x_tensors = [
    #     torch.empty(num_samples, device=mps_device).uniform_(-10, 10) for _ in range(1)
    # ]
    # terms = generate_terms_tensors(x_tensors, 1, [])
    # assert len(terms) == 1, f"Expected 1 term for degree 1, but got {len(terms)} terms."
    # assert str(terms[0][0]) == "x0", f"Expected term name 'x0', but got {terms[0][0]}."

    # Test for degree 2 with two variables and sin function
    # x_tensors = [
    #     torch.empty(num_samples, device=mps_device).uniform_(-10, 10) for _ in range(3)
    # ]
    num_vars = 3
    degree = 3
    depth = 2
    funcs = ["sin", "cos", "tan", "log", "exp", "sign", "sqrt", "abs"]
    num_funcs = len(funcs)

    # user_function = sp.sympify("x0*x1")
    def f(x0, x1):
        return x0 * x1

    one_symbol = True
    # x_tensors = [
    #     torch.randint(-10, 10, (num_samples,), device=mps_device)
    #     for _ in range(num_vars)
    # ]
    x_tensors = [torch.rand(num_samples, device=dev) * 10 - 5 for _ in range(3)]
    for x in x_tensors:
        print(x)
    terms = generate_terms_tensors(x_tensors, degree, funcs, depth, f, one_symbol)
    for term in terms:
        print(term)
    print(len(terms))
    print(count_terms(num_vars, degree, num_funcs, depth, True))
    assert len(terms) == count_terms(num_vars, degree, num_funcs, depth, True)

    # Filter out columns with inf values
    # terms, nan_count, inf_count, complex_count = filter_invalid_columns(terms)
    terms, inf_count = filter_invalid_columns(terms)
    print(f"filtered: {len(terms)}")
    # print(f"nan counts: {nan_count}")
    # print(f"complex counts: {complex_count}")
    print(f"inf counts: {inf_count}")
    # all_symbols = [name for name, _ in terms]

    # sp.sympify(input(f"Enter the function in terms of the symbols: {', '.join([term[0] for term in all_terms])}: "))

    # Write to CSV file
    with open("data.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = [term[0] for term in terms]
        csvwriter.writerow(headers)
        for data in zip(*[term[1] for term in terms]):
            csvwriter.writerow([value.item() for value in data])

    print("All tests passed!")


if __name__ == "__main__":
    import time

    start_time = time.time()
    test_generate_terms_tensors()
    elapsed_time = time.time() - start_time
    print("Test time = ", elapsed_time)
    exit()

    degree = 2  # int(input("Enter the polynomial degree: "))
    functions = [
        "sin",
        "cos",
    ]  # input("Enter functions separated by commas (e.g., sin,cos): ").split(",")

    # Generate random numbers for variables using PyTorch
    num_samples = 3
    x_tensors = [
        torch.empty(num_samples, device=dev).uniform_(-10, 10) for _ in range(degree)
    ]

    # Generate terms and tensors
    all_terms = generate_terms_tensors(x_tensors, degree, functions)
    all_symbols = [name for name, _ in all_terms]

    user_expr = sp.sympify("x0*x1")
    # sp.sympify(input(f"Enter the function in terms of the symbols: {', '.join([term[0] for term in all_terms])}: "))
    one_tensor = torch.ones(num_samples, device=dev)
    y_tensor = torch.zeros(num_samples, device=dev)

    # Evaluate the function in parallel for all tensor values
    for i in range(num_samples):
        y_tensor[i] = evaluate_expression(
            user_expr, all_symbols, [term[1][i].item() for term in all_terms]
        )

    # Write to CSV file
    with open("data.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = [term[0] for term in all_terms] + ["1"] + ["y"]
        csvwriter.writerow(headers)
        for data in zip(*[term[1] for term in all_terms], one_tensor, y_tensor):
            csvwriter.writerow([value.item() for value in data])

    print("Results written to data.csv")
