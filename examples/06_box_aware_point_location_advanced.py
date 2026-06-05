"""
Package Neutrosophic Computational Geometry (NCG)
06_box_aware_point_location_advanced.py

Example script that illustrates 06 box aware point location advanced
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
from ncg.algorithms.point_location import locate_in_polygon
from examples._plotting import draw_box, draw_npoint, save_figure, setup_axes, plot_polygon

polygon = [(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (0.0, 2.0)]
queries = [
    NPoint2.from_intervals((1.0, 1.1), (1.0, 1.1), "inside"),
    NPoint2.from_intervals((3.9, 4.2), (1.0, 1.0), "cross_right_edge"),
    NPoint2.from_intervals((4.2, 4.4), (1.0, 1.2), "outside"),
    NPoint2.from_intervals((2.0, 2.0), (-0.1, 0.1), "cross_bottom_edge"),
]

for q in queries:
    res = locate_in_polygon(q, polygon)
    print(f"query {q.label:17s} sure={q.sure()} realized={q.realized()} box={res.box}")
    print(f"  projected statuses: sure={res.sure_status}, realized={res.realized_status}")
    print(f"  AH-aware result:    {res.status}, candidates={sorted(res.candidate_faces or [])}")

fig, axes = plt.subplots(2, 2, figsize=(10, 7.8))
for ax, q in zip(axes.ravel(), queries):
    setup_axes(ax, q.label)
    plot_polygon(ax, polygon, linewidth=1.8)
    draw_npoint(ax, q)
    draw_box(ax, q.bbox(), alpha=0.12)
    res = locate_in_polygon(q, polygon)
    ax.text(0.02, 0.98, res.status, transform=ax.transAxes, va='top')
    ax.set_xlim(-0.5, 4.8)
    ax.set_ylim(-0.5, 2.6)

save_figure(fig, '06_box_aware_point_location_advanced.png')
