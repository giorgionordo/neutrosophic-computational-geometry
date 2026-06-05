"""
Package Neutrosophic Computational Geometry (NCG)
02_error_encoding_and_lattice_box.py

Example script that illustrates 02 error encoding and lattice box
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
from ncg.geometry.point import neutrosophic_bounding_box

print("interval encoding")
for interval in [(1.0, 1.25), (-0.1, 0.2), (3.0, 3.0)]:
    x = NRN.from_interval(*interval)
    print(f"  x in {interval} -> {x!r}, AH={x.ah()}")

points = [
    NPoint2.from_intervals((0.0, 0.08), (0.0, 0.02), "A"),
    NPoint2.from_intervals((2.0, 2.10), (0.4, 0.30), "B"),
    NPoint2.from_intervals((1.4, 1.55), (1.7, 1.85), "C"),
    NPoint2.from_intervals((-0.2, -0.05), (1.1, 1.00), "D"),
]

xmin, ymin, xmax, ymax = neutrosophic_bounding_box(points)
print("\nneutrosophic lattice bounding box")
print("  x- AH:", xmin.ah())
print("  y- AH:", ymin.ah())
print("  x+ AH:", xmax.ah())
print("  y+ AH:", ymax.ah())

print("\nprojected point coordinates")
for p in points:
    print(f"  {p.label}: sure={p.sure()} realized={p.realized()} box={p.bbox()}")
