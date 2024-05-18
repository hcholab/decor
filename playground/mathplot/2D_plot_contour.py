import matplotlib.pyplot as plt
import numpy as np


# Define the function
def f(x, y):
    return x + 2 * y


if __name__ == "__main__":
    # Generate x and y values
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)

    # Compute z values
    z = f(x, y)

    # Create the contour plot
    contour = plt.contour(x, y, z, levels=20, cmap="viridis")
    plt.contourf(x, y, z, levels=20, cmap="viridis", alpha=0.5)  # Filled contours
    plt.colorbar(contour, label="f(x, y)")  # Color bar

    # Add titles and labels
    plt.title("Contour plot of f(x, y) = x + 2xy + y^3")
    plt.xlabel("x")
    plt.ylabel("y")

    # Show the plot
    plt.show()
