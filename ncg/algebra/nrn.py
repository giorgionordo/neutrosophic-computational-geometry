"""
Package Neutrosophic Computational Geometry (NCG)
nrn.py

Module that defines neutrosophic real numbers in the algebra R[I]/(I^2-I)
and implements the Abobala--Hatip representation used in computational geometry.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from dataclasses import dataclass
from math import isclose, sqrt
from typing import Callable, Iterable, Tuple


#------------------ module-specific exceptions
class DegeneracyError(ArithmeticError):
    """
    Exception raised when a zero-divisor degeneracy is used as if it were
    an invertible neutrosophic number.
    """


#------------------ class of neutrosophic real numbers
@dataclass(frozen=True, order=False)
class NRN:
    """
    Class that defines a neutrosophic real number a + bI.

    ----
    Parameters:
    - a: sure coefficient of the neutrosophic number
    - b: indeterminate coefficient of the neutrosophic number; the realized
         AH value is a+b
    """

    a: float = 0.0   # sure coefficient
    b: float = 0.0   # indeterminate coefficient

    #------------------------------------------------------------------------------------

    # alternative constructor from the AH components
    @classmethod
    def from_ah(cls, sure: float, realized: float) -> "NRN":
        """
        Method that builds the unique neutrosophic number a+bI whose AH image
        is the pair (sure, realized).

        ----
        Parameters:
        - sure: first AH component
        - realized: second AH component
        """
        return cls(float(sure), float(realized) - float(sure))

    #-----------

    # alternative constructor from a real interval
    @classmethod
    def from_interval(cls, lower: float, upper: float) -> "NRN":
        """
        Method that encodes the interval [lower, upper] as the neutrosophic
        number lower + (upper-lower)I.

        This is a scenario encoding, not a probabilistic model.  In AH
        coordinates it gives exactly the pair (lower, upper).

        ----
        Parameters:
        - lower: lower bound of the interval
        - upper: upper bound of the interval
        """
        return cls(float(lower), float(upper) - float(lower))

    #------------------------------------------------------------------------------------

    # property that returns the sure component
    @property
    def sure(self) -> float:
        return self.a

    #-----------

    # property that returns the indeterminate coefficient
    @property
    def indeterminate(self) -> float:
        return self.b

    #-----------

    # short alias for the previous property
    @property
    def ind(self) -> float:
        """Alias for the indeterminate coefficient."""
        return self.b

    #-----------

    # property that returns the realized component in the AH representation
    @property
    def realized(self) -> float:
        return self.a + self.b

    #-----------

    # method that returns the Abobala--Hatip representation of the number
    def ah(self) -> Tuple[float, float]:
        """
        Method that returns the AH representation phi(self) = (sure, realized).
        """
        return (self.sure, self.realized)

    #------------------------------------------------------------------------------------

    # method that checks whether the number is a strong zero
    def is_strong_zero(self, eps: float = 0.0) -> bool:
        """
        Method that returns True iff both AH components vanish within eps.

        ----
        Parameters:
        - eps: tolerance used in the comparison with zero
        """
        return abs(self.sure) <= eps and abs(self.realized) <= eps

    #-----------

    # method that checks whether the number is a weak zero
    def is_weak_zero(self, eps: float = 0.0) -> bool:
        """
        Method that returns True iff at least one AH component vanishes within eps.

        Weak zero is a degeneracy predicate; it is not an equality relation.

        ----
        Parameters:
        - eps: tolerance used in the comparison with zero
        """
        return abs(self.sure) <= eps or abs(self.realized) <= eps

    #-----------

    # method that checks whether the number is a zero divisor
    def is_zero_divisor(self, eps: float = 0.0) -> bool:
        """
        Method that returns True iff the number is nonzero but weakly null.

        ----
        Parameters:
        - eps: tolerance used in the comparison with zero
        """
        return self.is_weak_zero(eps) and not self.is_strong_zero(eps)

    #-----------

    # method that checks whether the number is invertible
    def is_unit(self, eps: float = 0.0) -> bool:
        """
        Method that returns True iff both AH components are nonzero.

        ----
        Parameters:
        - eps: tolerance used in the comparison with zero
        """
        return abs(self.sure) > eps and abs(self.realized) > eps

    #-----------

    # method that returns the multiplicative inverse of the number
    def inverse(self, eps: float = 0.0) -> "NRN":
        """
        Method that returns the multiplicative inverse of the current
        neutrosophic number.

        Raises DegeneracyError if the number is not invertible.

        ----
        Parameters:
        - eps: tolerance used in the invertibility test
        """
        if not self.is_unit(eps):   # checks that the number is not a zero divisor
            raise DegeneracyError(f"{self!r} is a non-unit in R[I]/(I^2-I)")
        return NRN.from_ah(1.0 / self.sure, 1.0 / self.realized)

    #------------------------------------------------------------------------------------

    # method that checks approximate equality in the AH components
    def almost_equal(self, other: object, eps: float = 1e-12) -> bool:
        """
        Method that returns True iff two neutrosophic numbers are equal in AH
        coordinates within the tolerance eps.

        ----
        Parameters:
        - other: object to compare with the current neutrosophic number
        - eps: tolerance used in the componentwise comparison
        """
        other = as_nrn(other)   # converts the object into a neutrosophic real number
        return isclose(self.sure, other.sure, abs_tol=eps) and isclose(
            self.realized, other.realized, abs_tol=eps
        )

    #-----------

    # special method that checks exact equality in the AH components
    def __eq__(self, other: object) -> bool:
        try:
            other = as_nrn(other)   # tries to convert the object into a neutrosophic real number
        except TypeError:
            return NotImplemented
        return self.sure == other.sure and self.realized == other.realized

    #-----------

    # somma tra numeri reali neutrosofici
    def __add__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return NRN(self.a + other.a, self.b + other.b)

    #-----------

    # right addition with an object convertible to a neutrosophic real number
    def __radd__(self, other: object) -> "NRN":
        return self.__add__(other)

    #-----------

    # additive inverse of the neutrosophic real number
    def __neg__(self) -> "NRN":
        return NRN(-self.a, -self.b)

    #-----------

    # differenza tra numeri reali neutrosofici
    def __sub__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return NRN(self.a - other.a, self.b - other.b)

    #-----------

    # right subtraction with an object convertible to a neutrosophic real number
    def __rsub__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return other.__sub__(self)

    #-----------

    # prodotto tra numeri reali neutrosofici mediante prodotto componente per componente in AH
    def __mul__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return NRN.from_ah(self.sure * other.sure, self.realized * other.realized)

    #-----------

    # right multiplication with an object convertible to a neutrosophic real number
    def __rmul__(self, other: object) -> "NRN":
        return self.__mul__(other)

    #-----------

    # divisione tra numeri reali neutrosofici
    def __truediv__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return self * other.inverse()

    #-----------

    # right division with an object convertible to a neutrosophic real number
    def __rtruediv__(self, other: object) -> "NRN":
        other = as_nrn(other)
        return other.__truediv__(self)

    #------------------------------------------------------------------------------------

    # method that extends a scalar function to the AH components
    def lift_function(self, f: Callable[[float], float]) -> "NRN":
        """
        Method that applies a scalar function componentwise in AH coordinates.

        This is the functional extension used for non-polynomial operations,
        such as square roots: f(x~)=phi^{-1}(f(x_s), f(x_r)).

        ----
        Parameters:
        - f: scalar function to apply to the two AH components
        """
        return NRN.from_ah(f(self.sure), f(self.realized))

    #-----------

    # method that computes the square root in AH coordinates
    def sqrt(self, eps: float = 1e-12) -> "NRN":
        """
        Method that returns the square root of the current neutrosophic number
        in AH coordinates.

        Raises ValueError if at least one AH component is robustly negative.

        ----
        Parameters:
        - eps: tolerance used to detect robustly negative components
        """
        if self.sure < -eps or self.realized < -eps:   # checks compatibility with the real square root
            raise ValueError("Square root of a neutrosophic number with a negative AH component")
        return NRN.from_ah(sqrt(max(self.sure, 0.0)), sqrt(max(self.realized, 0.0)))

    #-----------

    # compact textual representation of the neutrosophic real number
    def __repr__(self) -> str:
        sign = "+" if self.b >= 0 else "-"
        return f"NRN({self.a:g} {sign} {abs(self.b):g}I)"


#------------------------------------------------------------------------------------
# lattice operations in the product order induced by the AH representation
#------------------------------------------------------------------------------------

# meet of two neutrosophic real numbers in the AH order

#------------------ function meet
def meet(x: object, y: object) -> NRN:
    """
    Function that returns the lattice meet in the AH product order.

    ----
    Parameters:
    - x: first object convertible into a neutrosophic real number
    - y: second object convertible into a neutrosophic real number
    """
    x, y = as_nrn(x), as_nrn(y)   # converts both objects into neutrosophic real numbers
    return NRN.from_ah(min(x.sure, y.sure), min(x.realized, y.realized))


#-----------

# join of two neutrosophic real numbers in the AH order

#------------------ function join
def join(x: object, y: object) -> NRN:
    """
    Function that returns the lattice join in the AH product order.

    ----
    Parameters:
    - x: first object convertible into a neutrosophic real number
    - y: second object convertible into a neutrosophic real number
    """
    x, y = as_nrn(x), as_nrn(y)   # converts both objects into neutrosophic real numbers
    return NRN.from_ah(max(x.sure, y.sure), max(x.realized, y.realized))


#-----------

# meet of a non-empty family of neutrosophic real numbers

#------------------ function meet_all
def meet_all(values: Iterable[object]) -> NRN:
    """
    Function that returns the meet of a non-empty iterable of objects
    convertible into neutrosophic real numbers.

    ----
    Parameters:
    - values: iterable of objects convertible into neutrosophic real numbers
    """
    it = iter(values)   # creates the iterator over the given values
    try:
        acc = as_nrn(next(it))   # inizializza l'accumulatore con il primo valore
    except StopIteration:
        raise ValueError("meet_all requires at least one value")
    for v in it:
        acc = meet(acc, v)   # aggiorna progressivamente l'estremo inferiore
    return acc


#-----------

# join of a non-empty family of neutrosophic real numbers

#------------------ function join_all
def join_all(values: Iterable[object]) -> NRN:
    """
    Function that returns the join of a non-empty iterable of objects
    convertible into neutrosophic real numbers.

    ----
    Parameters:
    - values: iterable of objects convertible into neutrosophic real numbers
    """
    it = iter(values)   # creates the iterator over the given values
    try:
        acc = as_nrn(next(it))   # inizializza l'accumulatore con il primo valore
    except StopIteration:
        raise ValueError("join_all requires at least one value")
    for v in it:
        acc = join(acc, v)   # aggiorna progressivamente l'estremo superiore
    return acc


#------------------------------------------------------------------------------------

# conversion function from an object to a neutrosophic real number

#------------------ function as_nrn
def as_nrn(value: object) -> NRN:
    """
    Function that converts a compatible object into a neutrosophic real number.

    ----
    Parameters:
    - value: object to convert into a neutrosophic real number
    """
    if isinstance(value, NRN):   # if the object is already an NRN, it is returned unchanged
        return value
    if isinstance(value, (int, float)):   # real numbers are interpreted as determined neutrosophic numbers
        return NRN(float(value), 0.0)
    raise TypeError(f"Cannot convert {type(value)!r} to NRN")


#------------------------------------------------------------------------------------
# costanti fondamentali dell'algebra R[I]/(I^2-I)
#------------------------------------------------------------------------------------

ZERO = NRN(0.0, 0.0)   # zero forte
ONE = NRN(1.0, 0.0)    # multiplicative unit
I = NRN(0.0, 1.0)      # indeterminate unit
