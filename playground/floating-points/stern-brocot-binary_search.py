from fractions import Fraction


class RationalApprox:
    @staticmethod
    def mediant(r1, r2):
        return Fraction(r1.numerator + r2.numerator, r1.denominator + r2.denominator)

    @staticmethod
    def approximate(x, epsilon=1e-15):
        left = Fraction(0)
        right = Fraction(1)
        best = left
        best_error = abs(x - float(best))
        print(f"{best} = {float(best)}, error = {best_error}")

        # Stern-Brocot binary search
        while best_error > epsilon:
            mediant = RationalApprox.mediant(left, right)
            if x < float(mediant):
                right = mediant  # go left
            else:
                left = mediant  # go right

            error = abs(float(mediant) - x)
            if error < best_error:
                best = mediant
                best_error = error
                print(f"{best} = {float(best)}, error = {best_error}")

        print()


if __name__ == "__main__":
    RationalApprox.approximate(0.333334, epsilon=1e-3)
    RationalApprox.approximate(0.2, epsilon=1e-3)
    RationalApprox.approximate(0.666667, epsilon=1e-3)
