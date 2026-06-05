"""
Package Neutrosophic Computational Geometry (NCG)
04_convex_hull_progressive.py

Example script that illustrates 04 convex hull progressive
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NPoint2
from ncg.algorithms.hull import neutrosophic_convex_hull

points = [
    NPoint2.from_intervals((0.0, 0.0), (0.0, 0.0), "A"),
    NPoint2.from_intervals((4.0, 4.0), (0.0, 0.0), "B"),
    NPoint2.from_intervals((4.0, 4.0), (3.0, 3.0), "C"),
    NPoint2.from_intervals((0.0, 0.0), (3.0, 3.0), "D"),
    # E is interior in the sure projection but becomes extreme on the left.
    NPoint2.from_intervals((2.0, -0.8), (1.5, 1.5), "E"),
    # F is interior in the sure projection but becomes extreme on the right.
    NPoint2.from_intervals((2.0, 4.5), (1.2, 1.2), "F"),
]

hull = neutrosophic_convex_hull(points, eps=1e-12)
print("sure hull labels:     ", hull.sure_hull)
print("realized hull labels: ", hull.realized_hull)
print("certified H+ labels:  ", sorted(hull.certified_vertices))
print("uncertain H? labels:  ", sorted(hull.uncertain_vertices))
print("mixed-or-collinear labels exposed by scan diagnostics:", sorted(hull.mixed_orientation_labels))

print("\nAH coordinates")
for p in points:
    print(f"  {p.label}: sure={p.sure()} realized={p.realized()} box={p.bbox()}")
