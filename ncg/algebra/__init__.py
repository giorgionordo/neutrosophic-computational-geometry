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
from .nrn import NRN, ZERO, ONE, I, DegeneracyError, as_nrn
from .predicates import SignState, qsgn, sgn_n, cayley_product_table

__all__ = [
    "NRN", "ZERO", "ONE", "I", "DegeneracyError", "as_nrn",
    "SignState", "qsgn", "sgn_n", "cayley_product_table",
]
