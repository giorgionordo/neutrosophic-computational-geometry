"""
Package Neutrosophic Computational Geometry (NCG)
04_gui_point_location.py

Graphical example script that demonstrates 04 gui point location
for the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from matplotlib.patches import Rectangle
from ncg import NPoint2, NRN
from ncg.algorithms.point_location import locate_in_polygon
from examples.gui._gui_helpers import make_root, make_figure, controls_frame, slider, setup_axes, draw_point, plot_polyline

polygon = [(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (0.0, 2.0)]
root = make_root("NCG GUI 04 - Box-aware point location")
fig, ax, canvas = make_figure(root, figsize=(7.8, 5.2))
frame = controls_frame(root)
state = {}


#------------------ function make_Q
def make_Q():
    return NPoint2(NRN.from_ah(3.35, state["qrx"].get()), NRN.from_ah(1.0, state["qry"].get()), "Q")


#------------------ function redraw
def redraw():
    Q = make_Q()
    res = locate_in_polygon(Q, polygon)
    xmin, ymin, xmax, ymax = Q.bbox()
    setup_axes(ax, "Neutrosophic query footprint", (-0.5, 5.0), (-0.6, 2.7))
    plot_polyline(ax, polygon, closed=True, linewidth=2.2)
    rect = Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, fill=True, alpha=0.18)
    ax.add_patch(rect)
    draw_point(ax, Q.sure(), r"$Q_s$", marker="o")
    draw_point(ax, Q.realized(), r"$Q_r$", marker="s")
    ax.plot([Q.sure()[0], Q.realized()[0]], [Q.sure()[1], Q.realized()[1]], linestyle=":", linewidth=1.0)
    ax.text(0.02, 0.97, f"sure={res.sure_status}; realized={res.realized_status}", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.90, f"AH-aware result: {res.status}", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.83, f"candidates: {sorted(res.candidate_faces or [])}", transform=ax.transAxes, va="top")
    canvas.draw_idle()

state["qrx"] = slider(frame, "realized Q x-coordinate", 2.8, 4.7, 4.35, redraw, 0)
state["qry"] = slider(frame, "realized Q y-coordinate", -0.3, 2.4, 1.0, redraw, 1)
redraw()
root.mainloop()
