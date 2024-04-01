def get_rate(degree, initial_rate=1, decay_rate=0.3):
    """
    Calculate the rate for a given degree using an exponential decay formula.

    :param degree: The degree for which to calculate the rate.
    :param initial_rate: The initial rate at degree 1.
    :param decay_rate: The rate of decay per degree increase.
    :return: The calculated rate.
    """
    return initial_rate * ((1 - decay_rate) ** (degree - 1))


# Test the function
for degree in range(1, 7):  # Testing for degrees 1 through 4
    rate = get_rate(degree)
    print(f"Degree {degree}: Rate {rate}")
