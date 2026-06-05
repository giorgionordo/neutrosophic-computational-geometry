"""
Package Neutrosophic Computational Geometry (NCG)
03_orientation_and_segment_footprint.py

Example script that illustrates 03 orientation and segment footprint
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NPoint2, NRN
from ncg.geometry.primitives import epsilon_collinear, orientation, orientation_state, segment_footprint, signed_area2

A = NPoint2(0.0, 0.0, "A")
B = NPoint2(2.0, 0.0, "B")
C = NPoint2(NRN.from_ah(1.0, 1.0), NRN.from_ah(1.0e-8, -1.0e-8), "C")

area = signed_area2(A, B, C)
print("signed area AH:", area.ah())
print("orientation state:", orientation_state(A, B, C, eps=0.0))
print("orientation label:", orientation(A, B, C, eps=0.0))
print("epsilon-collinear at eps=1e-7:", epsilon_collinear(A, B, C, 1e-7))
print("epsilon-collinear at eps=1e-10:", epsilon_collinear(A, B, C, 1e-10))

P = NPoint2.from_intervals((0.0, 0.15), (0.0, 0.10), "P")
Q = NPoint2.from_intervals((2.0, 2.20), (1.0, 0.85), "Q")
print("\nsegment footprint endpoints P_s,P_r,Q_s,Q_r:")
for item in segment_footprint(P, Q):
    print(" ", item)
