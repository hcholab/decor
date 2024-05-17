from sklearn.preprocessing import Normalizer
import numpy as np


if __name__ == "__main__":

    # Example data: Replace this with your dataset
    X = np.array([[0, 2, 3], [4, 5, 6]])

    # Initialize the Normalizer
    normalizer = Normalizer(norm="l2")

    # Fit and transform the data
    X_normalized = normalizer.transform(X)

    # Since sklearn Normalizer normalizes to a norm of 1, multiply by 10
    X_normalized *= 10

    # Check the result
    print("Normalized Data:")
    print(X_normalized)

    # Verify the L2-norm of the first sample is 10
    print("\nL2-norm of the first sample:", np.linalg.norm(X_normalized[0]))
