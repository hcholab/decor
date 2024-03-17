"""
To run doctest
$ python -m doctest -v src/bitween/miscs.py
"""

import functools
import sympy
import itertools
import logging
from typing import Iterable

from bitween import settings


def getLogger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(name)s:%(levelname)s:%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def getLogLevel(level: int) -> int:
    assert level in set(range(5))

    if level == 0:
        return logging.CRITICAL
    elif level == 1:
        return logging.ERROR
    elif level == 2:
        return logging.WARNING
    elif level == 3:
        return logging.INFO
    else:
        return logging.DEBUG


log = getLogger(__name__, settings.LOGGER_LEVEL)


class Symbolic:

    @staticmethod
    def is_expr(x) -> bool:
        return isinstance(x, sympy.Expr)

    @classmethod
    def get_vars(cls, props) -> list[sympy.Symbol]:
        """
        Returns a list of uniq variables from a list of properties

        >>> a,b,c,x = sympy.symbols('a b c x')
        >>> assert [a, b, c, x] == Symbolic.get_vars([sympy.Expr(x**(a*b) + a**2+b+2), sympy.Eq(c**2-b,100), sympy.Gt(b**2 + c**2 + a**3,1)])
        >>> assert Symbolic.get_vars(a**2+b+5*c+2) == [a, b, c]
        >>> assert Symbolic.get_vars(x+x**2) == [x]
        >>> assert Symbolic.get_vars([3]) == []
        >>> assert Symbolic.get_vars((3,'x + c',x+b)) == [b, x]
        """

        props = props if isinstance(props, Iterable) else [props]
        props = (p for p in props if isinstance(p, (sympy.Expr, sympy.Rel)))
        vs = (v for p in props for v in p.free_symbols)
        return sorted(set(vs), key=str)

    @staticmethod
    @functools.cache
    def str2rat(s: str) -> sympy.Rational:
        """
        Convert the input 's' to a rational number if possible.

        Examples:
        >>> print(Symbolic.str2rat('.3333333'))
        3333333/10000000
        >>> print(Symbolic.str2rat('3/7'))
        3/7
        >>> print(Symbolic.str2rat('1.'))
        1
        >>> print(Symbolic.str2rat('1.2'))
        6/5
        >>> print(Symbolic.str2rat('.333'))
        333/1000
        >>> print(Symbolic.str2rat('-.333'))
        -333/1000
        >>> print(Symbolic.str2rat('-12.13'))
        -1213/100
        """
        return sympy.Rational(s)

    @staticmethod
    def get_terms(symbols: list[sympy.Symbol], deg: int) -> list:
        """
        get a list of terms from the given list of vars and deg
        the number of terms is len(rs) == binomial(len(symbols)+d, d)

        >>> a,b,c,d,e,f = sympy.symbols('a b c d e f')
        >>> ts = Symbolic.get_terms([a, b], 3)
        >>> assert ts == [1, a, b, a**2, a*b, b**2, a**3, a**2*b, a*b**2, b**3]
        >>> Symbolic.get_terms([a,b,c,d,e,f], 3)
        [1, a, b, c, d, e, f, a**2, a*b, a*c, a*d, a*e, a*f, b**2, b*c, b*d, b*e, b*f, c**2, c*d, c*e, c*f, d**2, d*e, d*f, e**2, e*f, f**2, a**3, a**2*b, a**2*c, a**2*d, a**2*e, a**2*f, a*b**2, a*b*c, a*b*d, a*b*e, a*b*f, a*c**2, a*c*d, a*c*e, a*c*f, a*d**2, a*d*e, a*d*f, a*e**2, a*e*f, a*f**2, b**3, b**2*c, b**2*d, b**2*e, b**2*f, b*c**2, b*c*d, b*c*e, b*c*f, b*d**2, b*d*e, b*d*f, b*e**2, b*e*f, b*f**2, c**3, c**2*d, c**2*e, c**2*f, c*d**2, c*d*e, c*d*f, c*e**2, c*e*f, c*f**2, d**3, d**2*e, d**2*f, d*e**2, d*e*f, d*f**2, e**3, e**2*f, e*f**2, f**3]
        """

        assert deg >= 0, deg
        assert symbols, symbols

        # ss_ = ([1] if ss else (1,)) + ss
        symbols_ = [1] + symbols
        combs = itertools.combinations_with_replacement(symbols_, deg)
        terms = [sympy.prod(c) for c in combs]
        return terms

    @classmethod
    def reduce_eqts(cls, ps: list[sympy.Expr]) -> list[sympy.Expr]:
        """
        Return the basis (e.g., a min subset of ps that implies ps)
        of the set of polynomial eqts using Groebner basis.
        Warning 1: Grobner basis sometimes results in a larger set of eqts,
        in which case we return the original set of eqts.
        Warning 2: seems to get stuck often.  So had to give it "nice" polynomials

        >>> a, y, b, q, k = sympy.symbols('a y b q k')


        # >>> rs = Symbolic.reduce_eqts([a*y-b==0,q*y+k-x==0,a*x-a*k-b*q==0])
        __main__:DEBUG:Grobner basis: got 2 ps from 3 ps
        # >>> assert set(rs) == set([a*y - b == 0, q*y + k - x == 0])

        # >>> rs =  Symbolic.reduce_eqts([x*y==6,y==2,x==3])
        __main__:DEBUG:Grobner basis: got 2 ps from 3 ps
        # >>> assert set(rs) == set([x - 3 == 0, y - 2 == 0])

        # Attribute error occurs when only 1 var, thus return as is
        # >>> rs =  Symbolic.reduce_eqts([x*x==4,x==2])
        __main__:ERROR:'Ideal_1poly_field' object has no attribute 'radical'
        # >>> assert set(rs) == set([x == 2, x**2 == 4])
        """

        if len(ps) <= 1:
            return ps

        ps_ = sympy.groebner(ps, *cls.get_vars(ps))
        ps_ = [x for x in ps_]
        log.debug(f"Grobner basis: from {len(ps)} to {len(ps_)} ps")
        return ps_ if len(ps_) < len(ps) else ps

    @staticmethod
    def elim_denom(p: sympy.Expr | sympy.Rel) -> sympy.Expr | sympy.Rel:
        """
        Eliminate (Integer) denominators in expression operands.
        Will not eliminate if denominators is a var (e.g.,  (3*x)/(y+2)).

        >>> x,y,z = sympy.symbols('x y z')

        >>> Symbolic.elim_denom(sympy.Rational(3, 4)*x**2 + sympy.Rational(7, 5)*y**3)
        15*x**2 + 28*y**3

        >>> Symbolic.elim_denom(x + y)
        x + y

        >>> Symbolic.elim_denom(-sympy.Rational(3,2)*x**2 - sympy.Rational(1,24)*z**2)
        -36*x**2 - z**2

        >>> Symbolic.elim_denom(15*x**2 - 12*z**2)
        15*x**2 - 12*z**2

        """
        denoms = [sympy.fraction(a)[1] for a in p.args]
        if all(denom == 1 for denom in denoms):  # no denominator like 1/2
            return p
        return p * sympy.lcm(denoms)

    @classmethod
    def get_coefs(cls, p: sympy.Expr | sympy.Rel) -> list[sympy.core.numbers.Integer]:
        """
        Return coefficients of an expression

        >>> x,y,z = sympy.symbols('x y z')
        >>> Symbolic.get_coefs(3*x+5*x*y**2)
        [3, 5]
        """

        p = p.lhs if p.is_Equality else p
        return list(p.as_coefficients_dict().values())

    @classmethod
    def remove_ugly(
        cls, ps: list[sympy.Expr | sympy.Rel]
    ) -> list[sympy.Expr | sympy.Rel]:

        @functools.cache
        def is_nice_coef(c: int | float) -> bool:
            return abs(c) <= settings.UGLY_FACTOR or c % 10 == 0 or c % 5 == 0

        @functools.cache
        def is_nice_eqt(eqt: sympy.Expr | sympy.Rel) -> bool:
            return len(eqt.args) <= settings.UGLY_FACTOR and all(
                is_nice_coef(c) for c in cls.get_coefs(eqt)
            )

        ps_ = []
        for p in ps:
            if is_nice_eqt(p):
                ps_.append(p)
            else:
                log.debug(f"ignoring large coefs {str(p)[:50]} ..")

        return ps_

    @classmethod
    def refine(cls, eqts: list[sympy.Expr | sympy.Rel]) -> list[sympy.Expr | sympy.Rel]:

        if not eqts:
            return eqts

        eqts = [cls.elim_denom(s) for s in eqts]
        eqts = cls.remove_ugly(eqts)
        eqts = cls.reduce_eqts(eqts)
        eqts = [cls.elim_denom(s) for s in eqts]
        eqts = cls.remove_ugly(eqts)

        return eqts


if __name__ == "__main__":
    import doctest

    doctest.testmod()
