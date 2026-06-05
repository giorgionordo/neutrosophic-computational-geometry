"""
Package Neutrosophic Computational Geometry (NCG)
03_gui_convex_hull.py

Graphical example script that demonstrates 03 gui convex hull
for the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ncg import NPoint2, NRN
from ncg.algorithms.hull import neutrosophic_convex_hull
from examples.gui._gui_helpers import make_root, make_figure, controls_frame, slider, setup_axes, draw_point, plot_polyline

root = make_root("NCG GUI 03 - Convex hull labels")
fig, ax, canvas = make_figure(root, figsize=(8.0, 5.7))
frame = controls_frame(root)
state = {}


#------------------ function make_points
def make_points():
    # A, C, D are stable hull labels; B and E can become projection-dependent.
    return [
        NPoint2.from_intervals((0.0, 0.0), (0.0, 0.0), "A"),
        NPoint2(NRN.from_ah(4.0, state["brx"].get()), NRN.from_ah(0.0, state["bry"].get()), "B"),
        NPoint2.from_intervals((4.0, 4.0), (3.0, 3.0), "C"),
        NPoint2.from_intervals((0.0, 0.0), (3.0, 3.0), "D"),
        NPoint2(NRN.from_ah(2.0, state["erx"].get()), NRN.from_ah(1.5, state["ery"].get()), "E"),
    ]


#------------------ function redraw
def redraw():
    pts = make_points()
    hull = neutrosophic_convex_hull(pts)
    setup_axes(ax, "Certified and uncertain convex-hull labels", (-0.7, 4.8), (-0.8, 3.7))
    # builds dictionaries that associate each label with the corresponding projected point
    sure_by_label = {p.label: p.sure() for p in pts}
    realized_by_label = {p.label: p.realized() for p in pts}

    for p in pts:
        draw_point(ax, p.sure(), f"{p.label}_s", marker="o")
        draw_point(ax, p.realized(), f"{p.label}_r", marker="s")
        ax.plot([p.sure()[0], p.realized()[0]], [p.sure()[1], p.realized()[1]], linestyle=":", linewidth=0.9)
    # the algorithm returns hull labels; the GUI converts them back into projected coordinates
    if getattr(hull, "sure_hull", None):
        plot_polyline(ax, [sure_by_label[lab] for lab in hull.sure_hull], closed=True, linestyle="--", linewidth=1.8)
    if getattr(hull, "realized_hull", None):
        plot_polyline(ax, [realized_by_label[lab] for lab in hull.realized_hull], closed=True, linewidth=2.2)
    ax.text(0.02, 0.97, rf"$H^+={{{', '.join(map(str, sorted(hull.certified_vertices)))}}}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.90, rf"$H^?={{{', '.join(map(str, sorted(hull.uncertain_vertices)))}}}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.83, "dashed = sure hull; solid = realized hull", transform=ax.transAxes, va="top")
    canvas.draw_idle()

state["brx"] = slider(frame, "realized B x-coordinate", 2.0, 4.6, 4.0, redraw, 0)
state["bry"] = slider(frame, "realized B y-coordinate", -0.8, 1.2, 0.0, redraw, 1)
state["erx"] = slider(frame, "realized E x-coordinate", -0.2, 4.2, 2.0, redraw, 2)
state["ery"] = slider(frame, "realized E y-coordinate", -1.0, 4.2, -0.8, redraw, 3)
redraw()
root.mainloop()
