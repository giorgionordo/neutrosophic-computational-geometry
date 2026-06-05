"""
Package Neutrosophic Computational Geometry (NCG)
predicates.py

Module that defines sign-state logic and AH-order predicates for
neutrosophic real numbers.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from enum import Enum
from typing import Dict, Tuple

#------------------ import of basic neutrosophic structures
from .nrn import NRN, as_nrn


#------------------------------------------------------------------------------------
# enumeration class of classical signs
#------------------------------------------------------------------------------------

#------------------ class ClassicalSign
class ClassicalSign(int, Enum):
    """
    Enumeration that represents the classical sign of a real number.

    The three possible values are negative, zero and positive.  They are stored
    as integer values in order to keep the usual symbolic meaning of the sign.
    """

    NEG = -1      # negative sign
    ZERO = 0      # zero sign
    POS = 1       # positive sign

    # method that returns the symbolic representation of the classical sign
    def __str__(self) -> str:
        return {self.NEG: "-1", self.ZERO: "0", self.POS: "+1"}[self]


#------------------------------------------------------------------------------------
# enumeration class of neutrosophic sign states
#------------------------------------------------------------------------------------

#------------------ class SignState
class SignState(str, Enum):
    """
    Enumeration that represents the quotient sign algebra
    S_N = {-1, 0, +1, ?}.

    The value ? is used when the two AH components do not determine the same
    classical sign and the sign of the neutrosophic number is therefore mixed.
    """

    NEG = "-1"       # certified negative sign state
    ZERO = "0"       # certified zero sign state
    POS = "+1"       # certified positive sign state
    MIXED = "?"      # mixed or uncertified sign state

    # method that directly returns the symbolic value of the state
    def __str__(self) -> str:
        return self.value


#------------------------------------------------------------------------------------
# enumeration class of ternary truth values
#------------------------------------------------------------------------------------

#------------------ class Ternary
class Ternary(str, Enum):
    """
    Enumeration that represents the ternary truth values used by AH predicates.

    The value INDETERMINATE is returned when the two AH components do not give
    the same Boolean answer to the predicate under consideration.
    """

    TRUE = "TRUE"                         # predicate true in both AH components
    FALSE = "FALSE"                       # predicate false in both AH components
    INDETERMINATE = "INDETERMINATE"       # predicate not uniquely decided


#------------------------------------------------------------------------------------
# function that computes the tolerant classical sign of a real number
#------------------------------------------------------------------------------------

#------------------ function sign_real
def sign_real(x: float, eps: float = 1e-12) -> ClassicalSign:
    """
    Function that returns the classical tolerant sign of a real number.

    ----
    Parameters:
    - x: real number whose sign has to be computed
    - eps: tolerance used to decide whether x is numerically zero
    """

    if x > eps:
        return ClassicalSign.POS
    if x < -eps:
        return ClassicalSign.NEG
    return ClassicalSign.ZERO


#------------------------------------------------------------------------------------
# quotient function that maps two classical signs to the neutrosophic state
#------------------------------------------------------------------------------------

#------------------ function qsgn
def qsgn(sure_sign: ClassicalSign, realized_sign: ClassicalSign) -> SignState:
    """
    Function that implements the quotient map qsgn : S x S -> S_N.

    ----
    Parameters:
    - sure_sign: classical sign of the sure AH component
    - realized_sign: classical sign of the realized AH component
    """

    # if the two signs coincide, the sign state is certified
    if sure_sign == realized_sign:
        if sure_sign == ClassicalSign.POS:
            return SignState.POS
        if sure_sign == ClassicalSign.NEG:
            return SignState.NEG
        return SignState.ZERO

    # if the two signs do not coincide, the state is classified as mixed
    return SignState.MIXED


#------------------------------------------------------------------------------------
# function that computes the neutrosophic sign of a neutrosophic real number
#------------------------------------------------------------------------------------

#------------------ function sgn_n
def sgn_n(x: object, eps: float = 1e-12) -> SignState:
    """
    Function that returns the neutrosophic sign
    sgn_N(x) = qsgn(sgn(x_s), sgn(x_r)).

    ----
    Parameters:
    - x: object that can be converted into a neutrosophic real number
    - eps: tolerance used to compute the two classical signs
    """

    x = as_nrn(x)  # converts the object into a neutrosophic real number
    return qsgn(sign_real(x.sure, eps), sign_real(x.realized, eps))


#------------------------------------------------------------------------------------
# function that returns the pair of classical signs of the AH components
#------------------------------------------------------------------------------------

#------------------ function sign_nrn_pair
def sign_nrn_pair(x: object, eps: float = 1e-12) -> Tuple[ClassicalSign, ClassicalSign]:
    """
    Function that returns the pair of classical signs of the AH components.

    ----
    Parameters:
    - x: object that can be converted into a neutrosophic real number
    - eps: tolerance used to compute the classical signs
    """

    x = as_nrn(x)  # converts the object into a neutrosophic real number
    return sign_real(x.sure, eps), sign_real(x.realized, eps)


#------------------------------------------------------------------------------------
# function that multiplies two neutrosophic sign states
#------------------------------------------------------------------------------------

#------------------ function multiply_sign_states
def multiply_sign_states(a: SignState, b: SignState) -> SignState:
    """
    Function that computes the Cayley product in the sign-state algebra.

    The mixed state ? is absorbing with respect to the loss of precision,
    except when one factor is a certified zero.  In that case the product is
    forced to the strong zero state: 0 * ? = ? * 0 = 0.

    ----
    Parameters:
    - a: first sign state
    - b: second sign state
    """

    a, b = SignState(a), SignState(b)  # ensures that the two factors are sign states

    # a certified zero factor annihilates the product
    if a == SignState.ZERO or b == SignState.ZERO:
        return SignState.ZERO

    # if at least one factor is mixed, the product remains mixed
    if a == SignState.MIXED or b == SignState.MIXED:
        return SignState.MIXED

    # segni uguali danno prodotto positivo
    if a == b:
        return SignState.POS

    # segni opposti danno prodotto negativo
    return SignState.NEG


#------------------------------------------------------------------------------------
# function that builds the Cayley table of the sign-state product
#------------------------------------------------------------------------------------

#------------------ function cayley_product_table
def cayley_product_table() -> Dict[Tuple[SignState, SignState], SignState]:
    """
    Function that returns the Cayley table for multiplication in S_N.
    """

    states = [SignState.NEG, SignState.ZERO, SignState.POS, SignState.MIXED]
    return {(a, b): multiply_sign_states(a, b) for a in states for b in states}


#------------------------------------------------------------------------------------
# partial order predicate in AH coordinates
#------------------------------------------------------------------------------------

#------------------ function ah_leq
def ah_leq(x: object, y: object, eps: float = 1e-12) -> Ternary:
    """
    Function that evaluates the partial order predicate x <=_N y
    in AH coordinates.

    The predicate is true when both AH components satisfy the classical order,
    false when both components violate it, and indeterminate when the two
    components give different answers.

    ----
    Parameters:
    - x: first object that can be converted into a neutrosophic real number
    - y: second object that can be converted into a neutrosophic real number
    - eps: tolerance used in the comparison of the AH components
    """

    x, y = as_nrn(x), as_nrn(y)  # converts the objects into neutrosophic real numbers

    # checks the validity of the order in the two AH components
    ok_s = x.sure <= y.sure + eps
    ok_r = x.realized <= y.realized + eps

    # checks the violation of the order in the two AH components
    bad_s = x.sure > y.sure + eps
    bad_r = x.realized > y.realized + eps

    # the predicate is true if the order holds in both components
    if ok_s and ok_r:
        return Ternary.TRUE

    # the predicate is false if the order is violated in both components
    if bad_s and bad_r:
        return Ternary.FALSE

    # in the remaining cases the two AH components do not agree
    return Ternary.INDETERMINATE


#------------------------------------------------------------------------------------
# weak-zero predicate
#------------------------------------------------------------------------------------

#------------------ function weak_zero
def weak_zero(x: object, eps: float = 1e-12) -> bool:
    """
    Function that verifies whether an object is a weak zero.

    ----
    Parameters:
    - x: object that can be converted into a neutrosophic real number
    - eps: tolerance used in the zero test
    """

    return as_nrn(x).is_weak_zero(eps)


#------------------------------------------------------------------------------------
# strong-zero predicate
#------------------------------------------------------------------------------------

#------------------ function strong_zero
def strong_zero(x: object, eps: float = 1e-12) -> bool:
    """
    Function that verifies whether an object is a strong zero.

    ----
    Parameters:
    - x: object that can be converted into a neutrosophic real number
    - eps: tolerance used in the zero test
    """

    return as_nrn(x).is_strong_zero(eps)
