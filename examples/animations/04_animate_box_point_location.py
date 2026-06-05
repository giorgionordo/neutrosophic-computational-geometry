"""
Package Neutrosophic Computational Geometry (NCG)
04_animate_box_point_location.py

Animation script that illustrates 04 animate box point location
within the AH-lifted neutrosophic geometry framework.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ncg import NPoint2
from ncg.algorithms.point_location import locate_in_polygon
from examples.animations._animation_helpers import OUTPUT_DIR, setup_axes, plot_polyline, interp_point

polygon = [(0.0, 0.0), (4.0, 0.0), (4.0, 2.0), (0.0, 2.0)]
Q = NPoint2.from_intervals((3.35, 4.35), (1.0, 1.0), "Q")
result = locate_in_polygon(Q, polygon)

fig, ax = plt.subplots(figsize=(7.2, 4.8))


#------------------ function update
def update(frame):
    t = frame / 50.0
    setup_axes(ax, "Box-aware point location", (-0.5, 4.8), (-0.5, 2.6))
    plot_polyline(ax, polygon, closed=True, linewidth=2.0)
    qs = Q.sure()
    qr = Q.realized()
    qt = interp_point(Q, t)
    xmin, xmax = min(qs[0], qt[0]), max(qs[0], qt[0])
    ymin, ymax = min(qs[1], qt[1]), max(qs[1], qt[1])
    ax.plot(qs[0], qs[1], marker="o", linestyle="None")
    ax.plot(qr[0], qr[1], marker="s", linestyle="None")
    ax.plot(qt[0], qt[1], marker="D", linestyle="None")
    ax.text(qs[0] + 0.04, qs[1] + 0.06, r"$Q_s$")
    ax.text(qr[0] + 0.04, qr[1] + 0.06, r"$Q_r$")
    rect = Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=True, alpha=0.18)
    ax.add_patch(rect)
    status = "certified face" if xmax < 4.0 else "candidate set {face, exterior}"
    ax.text(0.02, 0.96, rf"$t={t:.2f}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.88, status, transform=ax.transAxes, va="top")
    ax.text(0.02, 0.80, f"final AH-aware result: {result.status}", transform=ax.transAxes, va="top")


ani = FuncAnimation(fig, update, frames=51, interval=90, repeat=True)
path = OUTPUT_DIR / "04_box_point_location.gif"
ani.save(path, writer=PillowWriter(fps=12))
print(f"[saved] {path}")
