from fractions import Fraction

# https://en.wikipedia.org/wiki/Stern–Brocot_tree
# https://dotink.co/posts/rational-binary-search/
# https://stackoverflow.com/questions/13437589/how-is-pythons-fractions-limit-denominator-implemented
# https://github.com/alidasdan/best-rational-approximation/blob/master/ad_rat_by_fast_farey.py


class RationalApprox:
    """
    Rational approximation using Stern-Brocot binary search
    """

    @staticmethod
    def mediant(r1, r2):
        return Fraction(r1.numerator + r2.numerator, r1.denominator + r2.denominator)

    @staticmethod
    def approximate(x, epsilon=1e-15, max_iterations=15, verbose=False):
        left = Fraction(0)
        right = Fraction(1)
        best = left
        best_error = abs(x)

        if verbose:
            print(f"{best} = {float(best)}, error = {best_error}")

        # Stern-Brocot binary search
        iterations = 0
        while best_error > epsilon:
            mediant = RationalApprox.mediant(left, right)
            if x < float(mediant):
                right = mediant  # go left
            else:
                left = mediant  # go right

            # check if better and update champion
            error = abs(float(mediant) - x)
            if error < best_error:
                best = mediant
                best_error = error
                if verbose:
                    print(f"{best} = {float(best)}, error = {best_error}")

            if iterations > max_iterations:
                break

            iterations += 1

        if iterations > max_iterations and verbose:
            print(f"Warning: max iterations reached ({max_iterations})")
            return Fraction(x).limit_denominator(int(1 / epsilon / 10))
        return best


if __name__ == "__main__":
    x = 0.1
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.333334
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.2
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.25
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.666667
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.1667
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.167
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.083
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.1111
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 1.1111
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 0.999
    print("SB-Tree:", RationalApprox.approximate(x, epsilon=1e-3, verbose=False))
    print("Fraction:", Fraction(x).limit_denominator(100))
    print()

    x = 1.2
    print("SB-Tree:", RationalApprox.approximate(1.2, epsilon=1e-3, verbose=False))
    print("Fraction:", Fraction(1.2).limit_denominator(100))
