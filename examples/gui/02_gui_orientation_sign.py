"""
Package Neutrosophic Computational Geometry (NCG)
02_gui_orientation_sign.py

Graphical example script that demonstrates 02 gui orientation sign
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
from ncg.geometry.primitives import signed_area2, orientation_state
from examples.gui._gui_helpers import make_root, make_figure, controls_frame, slider, setup_axes, draw_point, plot_polyline

root = make_root("NCG GUI 02 - Orientation sign-state")
fig, ax, canvas = make_figure(root)
frame = controls_frame(root)
state = {}

A = NPoint2(0.0, 0.0, "A")
B = NPoint2(2.0, 0.0, "B")


#------------------ function make_C
def make_C():
    xr = state["cxr"].get()
    yr = state["cyr"].get()
    return NPoint2(NRN.from_ah(1.0, xr), NRN.from_ah(0.55, yr), "C")


#------------------ function redraw
def redraw():
    C = make_C()
    eps = state["eps"].get()
    area = signed_area2(A, B, C)
    orient = orientation_state(A, B, C, eps=eps)
    setup_axes(ax, "AH-lifted orientation predicate", (-0.3, 2.4), (-1.1, 1.4))
    ps = [A.sure(), B.sure(), C.sure()]
    pr = [A.realized(), B.realized(), C.realized()]
    plot_polyline(ax, ps, closed=True, linewidth=1.8, linestyle="--")
    plot_polyline(ax, pr, closed=True, linewidth=2.2)
    for p in [A, B, C]:
        draw_point(ax, p.sure(), f"{p.label}_s", marker="o")
        draw_point(ax, p.realized(), f"{p.label}_r", marker="s")
    ax.axhline(0.0, linewidth=0.8)
    ax.text(0.02, 0.97, rf"$area_s={area.sure:.3f}$,  $area_r={area.realized:.3f}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.90, rf"$\varepsilon={eps:.3f}$,  $\operatorname{{Orient}}_N={orient}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.83, "dashed = sure triangle; solid = realized triangle", transform=ax.transAxes, va="top")
    canvas.draw_idle()

state["cxr"] = slider(frame, "realized C x-coordinate", 0.20, 1.80, 1.00, redraw, 0)
state["cyr"] = slider(frame, "realized C y-coordinate", -0.90, 1.20, -0.45, redraw, 1)
state["eps"] = slider(frame, "tolerance eps", 0.00, 0.50, 0.00, redraw, 2)
redraw()
root.mainloop()
