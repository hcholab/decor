from fractions import Fraction

# https://en.wikipedia.org/wiki/Stern–Brocot_tree


class RationalApprox:
    @staticmethod
    def mediant(r1, r2):
        return Fraction(r1.numerator + r2.numerator, r1.denominator + r2.denominator)

    @staticmethod
    def approximate(x, epsilon=1e-15, max_iterations=10, verbose=False):
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

            iterations += 1

            if iterations > max_iterations:
                break
        if iterations > max_iterations and verbose:
            print(f"Warning: max iterations reached ({max_iterations})")
            return Fraction(x).limit_denominator(1000)
        return best


if __name__ == "__main__":
    print("SB-Tree:", RationalApprox.approximate(0.333334, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.333334).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(0.2, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.2).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(0.25, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.25).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(0.666667, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.666667).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(0.1667, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.1667).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(0.999, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(0.999).limit_denominator(1000))

    print("SB-Tree:", RationalApprox.approximate(1.2, epsilon=1e-3, verbose=True))
    print("Fraction:", Fraction(1.2).limit_denominator(1000))
