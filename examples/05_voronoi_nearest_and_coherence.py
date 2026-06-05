"""
Package Neutrosophic Computational Geometry (NCG)
05_voronoi_nearest_and_coherence.py

Example script that illustrates 05 voronoi nearest and coherence
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
from ncg.algorithms.voronoi import coherent_perturbation_scale, nearest_neighbor, potential_voronoi_boundary

sites = [
    NPoint2.from_intervals((0.0, 0.04), (0.0, 0.03), "A"),
    NPoint2.from_intervals((2.0, 2.03), (0.0, 0.02), "B"),
    NPoint2.from_intervals((1.0, 1.02), (1.8, 1.83), "C"),
]

queries = [
    NPoint2.from_intervals((0.2, 0.22), (0.1, 0.11), "near_A"),
    NPoint2.from_intervals((1.0, 1.1), (0.05, 0.05), "near_boundary_AB"),
    NPoint2.from_intervals((1.0, 1.02), (1.1, 1.25), "near_C"),
]

print("coherent perturbation diagnostic (max displacement, minimum sure site distance):")
print(" ", coherent_perturbation_scale(sites))

for q in queries:
    res = nearest_neighbor(q, sites)
    print(f"\nquery {q.label}: sure={q.sure()} realized={q.realized()}")
    print("  certified label:", res.certified_label)
    print("  competing labels:", sorted(res.competing_labels))
    for lab, d in sorted(res.distances.items(), key=lambda item: str(item[0])):
        print(f"  dist2 to {lab}: AH={d}")
    print("  potential boundary A/B:", potential_voronoi_boundary(q, sites[0], sites[1]))
