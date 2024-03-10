def sqrtNewton(n, precision):
    guess = n / 2.0
    while abs(guess * guess - n) > precision:
        guess = (guess + n / guess) / 2.0
    return guess


# Example usage:
n = 49.0
precision = 0.01
print(sqrtNewton(n, precision))  # Should print something very close to 7.0
