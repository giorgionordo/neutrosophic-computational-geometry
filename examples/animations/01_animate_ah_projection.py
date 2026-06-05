"""
Package Neutrosophic Computational Geometry (NCG)
01_animate_ah_projection.py

Animation script that illustrates 01 animate ah projection
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

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ncg import NPoint2
from examples.animations._animation_helpers import OUTPUT_DIR, setup_axes, draw_point_pair, interp_point

points = [
    NPoint2.from_intervals((0.0, 0.35), (0.0, 0.15), "A"),
    NPoint2.from_intervals((2.0, 2.25), (0.2, 0.55), "B"),
    NPoint2.from_intervals((1.1, 0.80), (1.9, 2.25), "C"),
    NPoint2.from_intervals((-0.3, -0.55), (1.2, 1.00), "D"),
]

fig, ax = plt.subplots(figsize=(6.8, 5.2))


#------------------ function update
def update(frame):
    t = frame / 50.0
    setup_axes(ax, r"AH interpolation: $\widetilde P=(1-t)P_s+tP_r$", (-0.9, 2.7), (-0.3, 2.6))
    for p in points:
        draw_point_pair(ax, p)
        x, y = interp_point(p, t)
        ax.plot(x, y, marker="D", linestyle="None")
        ax.text(x + 0.04, y + 0.04, str(p.label))
    ax.text(0.02, 0.96, rf"$t={t:.2f}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.90, r"$t=0$: sure projection;  $t=1$: realized projection", transform=ax.transAxes, va="top")


ani = FuncAnimation(fig, update, frames=51, interval=80, repeat=True)
path = OUTPUT_DIR / "01_ah_projection.gif"
ani.save(path, writer=PillowWriter(fps=12))
print(f"[saved] {path}")
