import matplotlib.pyplot as plt
import numpy as np


# Define the first function
def f1(x, y):
    return x + x * y + y**2


# Define the second function
def f2(x, y):
    return x + 2 * y


if __name__ == "__main__":
    # Generate x and y values
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    x, y = np.meshgrid(x, y)

    # Compute z values for both functions
    z1 = f1(x, y)
    z2 = f2(x, y)

    # Create the plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the first function
    surface1 = ax.plot_surface(
        x, y, z1, cmap="viridis", alpha=0.6, label="x + xy + y^2"
    )
    # surface1._edgecolors2d = surface1._edgecolor3d
    # surface1._facecolors2d = surface1._facecolor3d

    # Plot the second function
    surface2 = ax.plot_surface(
        x, y, z2, cmap="plasma", alpha=0.6, label="x + 2xy + y^3"
    )
    # surface2._edgecolors2d = surface2._edgecolor3d
    # surface2._facecolors2d = surface2._facecolor3d

    # Add titles and labels
    ax.set_title(
        "Surface plots of f1(x, y) = x + xy + y^2 and f2(x, y) = x + 2xy + y^3"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("f(x, y)")

    # Add legend
    ax.legend()

    # Show the plot
    plt.show()
