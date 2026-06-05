"""
Package Neutrosophic Computational Geometry (NCG)
demo.py

Demonstration script that runs a compact overview of the main NCG
objects, predicates and algorithms.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NRN, NPoint2
from ncg.algebra.predicates import SignState, cayley_product_table, sgn_n
from ncg.algorithms.hull import neutrosophic_convex_hull
from ncg.algorithms.point_location import locate_in_polygon
from ncg.algorithms.voronoi import coherent_perturbation_scale, nearest_neighbor
from ncg.geometry.primitives import orientation, signed_area2, compare_dist2, dist


# Practical error encoding: x in [a,b] -> a + (b-a)I, AH image (a,b).
x = NRN.from_interval(1.0, 1.0000000001)
print("interval encoding AH:", x.ah())
print("sgn_N(x-1):", sgn_n(x - 1.0))

print("Cayley product table:")
for key, value in cayley_product_table().items():
    print(f"  {key[0]} * {key[1]} = {value}")

# Nearly collinear triple: sure area positive, realized area negative -> MIXED.
A = NPoint2(0.0, 0.0, "A")
B = NPoint2(1.0, 0.0, "B")
C = NPoint2(NRN(0.5, 0.0), NRN(1e-16, -2e-16), "C")
print("area(A,B,C):", signed_area2(A, B, C).ah())
print("orientation(A,B,C):", orientation(A, B, C, eps=0.0))

points = [
    NPoint2.from_intervals((0.0, 0.05), (0.0, 0.02), "A"),
    NPoint2.from_intervals((1.0, 1.10), (0.10, 0.06), "B"),
    NPoint2.from_intervals((0.8, 0.75), (1.0, 1.08), "C"),
    NPoint2.from_intervals((0.1, 0.13), (0.9, 1.02), "D"),
    NPoint2.from_intervals((0.45, 0.65), (0.45, 0.30), "E"),
]
hull = neutrosophic_convex_hull(points)
print("sure hull:", hull.sure_hull)
print("realized hull:", hull.realized_hull)
print("certified hull labels:", sorted(hull.certified_vertices))
print("uncertain hull labels:", sorted(hull.uncertain_vertices))

query = NPoint2.from_intervals((0.50, 0.58), (0.40, 0.52), "Q")
print("nearest:", nearest_neighbor(query, points))
print("coherent perturbation diagnostic:", coherent_perturbation_scale(points))
print("distance A-B:", dist(points[0], points[1]).ah())
print("distance comparison Q-A vs Q-B:", compare_dist2(query, points[0], points[1]))

polygon = [(0, 0), (4, 0), (4, 2), (0, 2)]
q = NPoint2.from_intervals((3.9, 4.2), (1.0, 1.0), "uncertain_boundary")
print("point location:", locate_in_polygon(q, polygon))
