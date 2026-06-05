"""
Package Neutrosophic Computational Geometry (NCG)
02_animate_orientation_sign_state.py

Animation script that illustrates 02 animate orientation sign state
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

from ncg import NPoint2, NRN
from ncg.geometry.primitives import signed_area2, orientation_state
from examples.animations._animation_helpers import OUTPUT_DIR, setup_axes, draw_point_pair, interp_point, plot_polyline

A = NPoint2(0.0, 0.0, "A")
B = NPoint2(2.0, 0.0, "B")
C = NPoint2(NRN.from_ah(1.0, 1.0), NRN.from_ah(0.55, -0.45), "C")

area = signed_area2(A, B, C)
state = orientation_state(A, B, C, eps=0.0)

fig, ax = plt.subplots(figsize=(7.0, 5.2))


#------------------ function update
def update(frame):
    t = frame / 60.0
    setup_axes(ax, "Orientation sign-state along the AH scenario", (-0.3, 2.3), (-0.8, 0.9))
    for p in [A, B, C]:
        draw_point_pair(ax, p)
    Ct = interp_point(C, t)
    plot_polyline(ax, [A.sure(), B.sure(), Ct], closed=True, linewidth=1.8)
    ax.plot(Ct[0], Ct[1], marker="D", linestyle="None")
    current_area = (1 - t) * area.sure + t * area.realized
    current_sign = "+1" if current_area > 0 else "-1" if current_area < 0 else "0"
    ax.text(0.02, 0.96, rf"$\operatorname{{area}}_2^s={area.sure:.2f}$, "
                         rf"$\operatorname{{area}}_2^r={area.realized:.2f}$", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.89, rf"current interpolated sign: {current_sign}", transform=ax.transAxes, va="top")
    ax.text(0.02, 0.82, rf"$\operatorname{{sgn}}_N={state}$", transform=ax.transAxes, va="top")
    ax.axhline(0.0, linewidth=0.8)


ani = FuncAnimation(fig, update, frames=61, interval=80, repeat=True)
path = OUTPUT_DIR / "02_orientation_sign_state.gif"
ani.save(path, writer=PillowWriter(fps=12))
print(f"[saved] {path}")
