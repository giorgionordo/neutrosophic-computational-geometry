"""
Package Neutrosophic Computational Geometry (NCG)
07_non_polynomial_lifting.py

Example script that illustrates 07 non polynomial lifting
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from math import log1p

from ncg import NPoint2, NRN
from ncg.geometry.primitives import compare_dist2, dist, dist2

x = NRN.from_interval(3.0, 4.0)
print("functional lifting")
print("  x AH:", x.ah())
print("  sqrt(x) AH:", x.sqrt().ah())
print("  log1p(x) AH:", x.lift_function(log1p).ah())

Q = NPoint2.from_intervals((0.0, 0.2), (0.0, 0.0), "Q")
A = NPoint2(1.0, 0.0, "A")
B = NPoint2.from_intervals((1.1, 0.85), (0.0, 0.0), "B")

print("\ndistances from query")
print("  dist2(Q,A) AH:", dist2(Q, A).ah())
print("  dist2(Q,B) AH:", dist2(Q, B).ah())
print("  dist(Q,A)  AH:", dist(Q, A).ah())
print("  dist(Q,B)  AH:", dist(Q, B).ah())
print("  comparison by squares:", compare_dist2(Q, A, B, eps=0.0))
