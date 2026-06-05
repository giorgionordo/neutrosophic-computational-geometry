"""
Package Neutrosophic Computational Geometry (NCG)
01_gui_ah_projection.py

Graphical example script that demonstrates 01 gui ah projection
for the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ncg import NPoint2
from examples.gui._gui_helpers import make_root, make_figure, controls_frame, slider, setup_axes, draw_point, point_at

points = [
    NPoint2.from_intervals((0.0, 0.50), (0.1, 0.25), "A"),
    NPoint2.from_intervals((2.0, 2.45), (0.2, 0.65), "B"),
    NPoint2.from_intervals((1.2, 0.85), (1.9, 2.35), "C"),
    NPoint2.from_intervals((-0.3, -0.60), (1.2, 0.95), "D"),
]

root = make_root("NCG GUI 01 - AH projection")
fig, ax, canvas = make_figure(root)
frame = controls_frame(root)

state = {}

#------------------ function redraw
def redraw():
    t = state["t"].get()
    setup_axes(ax, r"AH scenario: $(1-t)P_s+tP_r$", (-0.9, 2.9), (-0.3, 2.7))
    for p in points:
        ps, pr = p.sure(), p.realized()
        ax.plot([ps[0], pr[0]], [ps[1], pr[1]], linestyle=":", linewidth=1.0)
        draw_point(ax, ps, f"{p.label}_s", marker="o")
        draw_point(ax, pr, f"{p.label}_r", marker="s")
        draw_point(ax, point_at(p, t), f"{p.label}(t)", marker="D")
    ax.text(0.02, 0.97, rf"$t={t:.2f}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.91, r"$t=0$: sure projection;   $t=1$: realized projection", transform=ax.transAxes, va="top")
    canvas.draw_idle()

state["t"] = slider(frame, "scenario parameter t", 0.0, 1.0, 0.0, redraw, 0)
redraw()
root.mainloop()
