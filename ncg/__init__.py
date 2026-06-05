"""
Package Neutrosophic Computational Geometry (NCG)
__init__.py

Package initialization module for the Neutrosophic Computational
Geometry library.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from ncg.algebra.nrn import NRN, ZERO, ONE, I, DegeneracyError, as_nrn
from ncg.algebra.predicates import SignState, qsgn, sgn_n, cayley_product_table
from ncg.geometry.point import NPoint2, NVector2

__all__ = [
    "NRN", "ZERO", "ONE", "I", "DegeneracyError", "as_nrn",
    "SignState", "qsgn", "sgn_n", "cayley_product_table",
    "NPoint2", "NVector2",
]
