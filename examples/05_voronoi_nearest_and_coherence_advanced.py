"""
Package Neutrosophic Computational Geometry (NCG)
05_voronoi_nearest_and_coherence_advanced.py

Example script that illustrates 05 voronoi nearest and coherence advanced
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NPoint2
from ncg.algorithms.voronoi import coherent_perturbation_scale, nearest_neighbor, potential_voronoi_boundary
from examples._plotting import draw_npoint, draw_box, save_figure, setup_axes

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

scale = coherent_perturbation_scale(sites)
print("coherent perturbation diagnostic (max displacement, minimum sure site distance):")
print(" ", scale)
for q in queries:
    res = nearest_neighbor(q, sites)
    print(f"\nquery {q.label}: sure={q.sure()} realized={q.realized()}")
    print("  certified label:", res.certified_label)
    print("  competing labels:", sorted(res.competing_labels))
    print("  potential boundary A/B:", potential_voronoi_boundary(q, sites[0], sites[1]))

fig, ax = plt.subplots(figsize=(8.4, 6.0))
setup_axes(ax, "Nearest-site decisions and coherent perturbation")
for s in sites:
    draw_npoint(ax, s)
for q in queries:
    draw_npoint(ax, q)
    draw_box(ax, q.bbox(), alpha=0.06)
    res = nearest_neighbor(q, sites)
    label_text = res.certified_label if res.certified_label is not None else f"mixed {sorted(res.competing_labels)}"
    ax.text(q.sure()[0] + 0.1, q.sure()[1] + 0.14, f"{q.label}: {label_text}", fontsize=8)

# sure bisector of A and B
A_s, B_s = sites[0].sure(), sites[1].sure()
mid_x = 0.5 * (A_s[0] + B_s[0])
ax.plot([mid_x, mid_x], [-0.3, 2.2], linestyle='--', linewidth=1.4)
ax.text(mid_x + 0.05, 2.05, "sure A/B bisector")
ax.text(0.02, 0.98, f"max displacement = {scale[0]:.3f}\nmin sure-site distance = {scale[1]:.3f}", transform=ax.transAxes, va='top')
save_figure(fig, '05_voronoi_nearest_and_coherence_advanced.png')
