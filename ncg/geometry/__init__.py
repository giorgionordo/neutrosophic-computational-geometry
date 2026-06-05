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
from .point import NPoint2, NVector2, Point2, Box2

__all__ = ["NPoint2", "NVector2", "Point2", "Box2"]
