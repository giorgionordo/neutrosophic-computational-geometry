"""
Package Neutrosophic Computational Geometry (NCG)
04_convex_hull_progressive_advanced.py

Example script that illustrates 04 convex hull progressive advanced
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
from ncg.algorithms.hull import neutrosophic_convex_hull
from examples._plotting import draw_npoint, save_figure, setup_axes, fill_polygon, plot_polygon

points = [
    NPoint2.from_intervals((0.0, 0.0), (0.0, 0.0), "A"),
    NPoint2.from_intervals((4.0, 4.0), (0.0, 0.0), "B"),
    NPoint2.from_intervals((4.0, 4.0), (3.0, 3.0), "C"),
    NPoint2.from_intervals((0.0, 0.0), (3.0, 3.0), "D"),
    NPoint2.from_intervals((2.0, -0.8), (1.5, 1.5), "E"),
    NPoint2.from_intervals((2.0, 4.5), (1.2, 1.2), "F"),
]

hull = neutrosophic_convex_hull(points, eps=1e-12)
print("sure hull labels:     ", hull.sure_hull)
print("realized hull labels: ", hull.realized_hull)
print("certified H+ labels:  ", sorted(hull.certified_vertices))
print("uncertain H? labels:  ", sorted(hull.uncertain_vertices))
print("mixed-or-collinear labels exposed by scan diagnostics:", sorted(hull.mixed_orientation_labels))

point_map = {p.label: p for p in points}
sure_poly = [point_map[label].sure() for label in hull.sure_hull]
real_poly = [point_map[label].realized() for label in hull.realized_hull]

fig, ax = plt.subplots(figsize=(8.8, 6.2))
setup_axes(ax, "Certified and uncertain labels in the AH-lifted hull")
fill_polygon(ax, sure_poly, alpha=0.07)
fill_polygon(ax, real_poly, alpha=0.07)
plot_polygon(ax, sure_poly, linestyle='--', linewidth=1.8, label='sure hull')
plot_polygon(ax, real_poly, linestyle='-', linewidth=2.0, label='realized hull')

for p in points:
    draw_npoint(ax, p)
    status = 'certified' if p.label in hull.certified_vertices else 'uncertain'
    ax.text(p.sure()[0], p.sure()[1] + 0.18, status, ha='center', fontsize=8)

ax.text(0.02, 0.98, f"H+ = {sorted(hull.certified_vertices)}\nH? = {sorted(hull.uncertain_vertices)}", transform=ax.transAxes, va='top')
ax.legend(loc='lower right')
save_figure(fig, '04_convex_hull_progressive_advanced.png')
