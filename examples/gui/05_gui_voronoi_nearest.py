"""
Package Neutrosophic Computational Geometry (NCG)
05_gui_voronoi_nearest.py

Graphical example script that demonstrates 05 gui voronoi nearest
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
from ncg.algorithms.voronoi import nearest_site_state
from examples.gui._gui_helpers import make_root, make_figure, controls_frame, slider, setup_axes, draw_point

root = make_root("NCG GUI 05 - Nearest-site state")
fig, ax, canvas = make_figure(root, figsize=(7.8, 5.4))
frame = controls_frame(root)
state = {}


#------------------ function make_sites
def make_sites():
    return [
        NPoint2.from_intervals((0.2, 0.2), (0.4, 0.4), "A"),
        NPoint2(NRN.from_ah(3.1, state["brx"].get()), NRN.from_ah(0.5, state["bry"].get()), "B"),
        NPoint2.from_intervals((1.5, 1.5), (2.7, 2.7), "C"),
    ]


#------------------ function make_Q
def make_Q():
    return NPoint2(NRN.from_ah(state["qsx"].get(), state["qrx"].get()), NRN.from_ah(state["qsy"].get(), state["qry"].get()), "Q")


#------------------ function redraw
def redraw():
    sites = make_sites()
    Q = make_Q()
    res = nearest_site_state(Q, sites)
    setup_axes(ax, "AH nearest-site state", (-0.3, 3.8), (-0.2, 3.4))
    for p in sites:
        draw_point(ax, p.sure(), f"{p.label}_s", marker="o")
        draw_point(ax, p.realized(), f"{p.label}_r", marker="s")
        ax.plot([p.sure()[0], p.realized()[0]], [p.sure()[1], p.realized()[1]], linestyle=":", linewidth=0.8)
    draw_point(ax, Q.sure(), r"$Q_s$", marker="D")
    draw_point(ax, Q.realized(), r"$Q_r$", marker="X")
    ax.plot([Q.sure()[0], Q.realized()[0]], [Q.sure()[1], Q.realized()[1]], linestyle=":", linewidth=1.2)
    ax.text(0.02, 0.97, f"nearest sure label: {res.sure_label}", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.90, f"nearest realized label: {res.realized_label}", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.83, f"certified: {res.certified}", transform=ax.transAxes, va="top")
    canvas.draw_idle()

state["brx"] = slider(frame, "realized B x-coordinate", 2.1, 3.5, 2.6, redraw, 0)
state["bry"] = slider(frame, "realized B y-coordinate", 0.0, 2.2, 1.4, redraw, 1)
state["qsx"] = slider(frame, "sure Q x-coordinate", 0.0, 3.4, 1.6, redraw, 2)
state["qsy"] = slider(frame, "sure Q y-coordinate", 0.0, 3.0, 1.1, redraw, 3)
state["qrx"] = slider(frame, "realized Q x-coordinate", 0.0, 3.4, 1.9, redraw, 4)
state["qry"] = slider(frame, "realized Q y-coordinate", 0.0, 3.0, 1.4, redraw, 5)
redraw()
root.mainloop()
