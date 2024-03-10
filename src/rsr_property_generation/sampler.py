import random
from enum import Enum

from sympy import Symbol


class Domain(Enum):
    """
    Domain of the variables.
    """

    Real = 1
    Integer = 2

    def __str__(self):
        """
        :return: string representation of the domain
        """
        if self == Domain.Real:
            return "Real"
        elif self == Domain.Integer:
            return "Integer"
        else:
            raise ValueError("Invalid domain")

    def latex(self):
        """
        :return: latex representation of the domain
        """
        if self == Domain.Real:
            return "\\mathbb{R}"
        elif self == Domain.Integer:
            return "\\mathbb{Z}"
        else:
            raise ValueError("Invalid domain")


class Distribution(Enum):
    """
    Distribution of the values of the variables.

    Small: [-10, 10] for integers and [-5, 5] for reals
    Standard: [-1000, 1000] for integers and [-500, 500] for reals
    """

    Small = 1
    Standard = 2

    def __str__(self):
        """
        :return: string representation of the distribution
        """
        if self == Distribution.Small:
            return "Small"
        elif self == Distribution.Standard:
            return "Standard"
        else:
            raise ValueError("Invalid distribution")

    def latex(self):
        """
        :return: latex representation of the distribution
        """
        if self == Distribution.Small:
            return "\\mathcal{U}(-10, 10)"
        elif self == Distribution.Standard:
            return "\\mathcal{U}(-1000, 1000)"
        else:
            raise ValueError("Invalid distribution")


def sample(domain: Domain, distribution: Distribution, variables: list[str | Symbol]):
    """
    Sample values for the given list of variables.

    :param domain: domain of the variables
    :param distribution: distribution of the values
    :param variables: variables to be sampled
    :return: dictionary of sampled values
    """
    if domain == Domain.Real:
        if distribution == Distribution.Small:
            # for exponential functions such as f(x) = e^x
            values = {}
            for var in variables:
                values[str(var)] = random.random() * 10 - 5
        else:
            # standard range
            values = {}
            for var in variables:
                values[str(var)] = random.random() * 1000 - 500
    elif domain == Domain.Integer:
        if distribution == Distribution.Small:
            values = {}
            for var in variables:
                values[str(var)] = random.randint(-10, 10)
        else:
            values = {}
            for var in variables:
                values[str(var)] = random.randint(-1000, 1000)

    return values


if __name__ == "__main__":  # noqa E123
    """
    Test cases
    """
    pass
