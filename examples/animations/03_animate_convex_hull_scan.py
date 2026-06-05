"""
Package Neutrosophic Computational Geometry (NCG)
03_animate_convex_hull_scan.py

Animation script that illustrates 03 animate convex hull scan
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
from ncg.algorithms.hull import neutrosophic_convex_hull
from examples.animations._animation_helpers import OUTPUT_DIR, setup_axes, plot_polyline

points = [
    NPoint2.from_intervals((0.0, 0.0), (0.0, 0.0), "A"),
    NPoint2.from_intervals((4.0, 4.0), (0.0, 0.0), "B"),
    NPoint2.from_intervals((4.0, 4.0), (3.0, 3.0), "C"),
    NPoint2.from_intervals((0.0, 0.0), (3.0, 3.0), "D"),
    NPoint2.from_intervals((2.0, -0.8), (1.5, 1.5), "E"),
    NPoint2.from_intervals((2.0, 4.5), (1.2, 1.2), "F"),
]

hull = neutrosophic_convex_hull(points)


#------------------ function monotone_steps
def monotone_steps(coords_by_label):
    items = sorted(coords_by_label.items(), key=lambda kv: (kv[1][0], kv[1][1], str(kv[0])))
    steps = []
    lower = []
    for lab, pt in items:
        lower.append((lab, pt))
        steps.append(("lower: add " + str(lab), [x[1] for x in lower], set()))
        while len(lower) >= 3:
            o, a, b = lower[-3][1], lower[-2][1], lower[-1][1]
            cross = (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
            if cross <= 1e-12:
                removed = lower[-2][0]
                lower.pop(-2)
                steps.append(("lower: pop " + str(removed), [x[1] for x in lower], {removed}))
            else:
                break
    upper = []
    for lab, pt in reversed(items):
        upper.append((lab, pt))
        steps.append(("upper: add " + str(lab), [x[1] for x in upper], set()))
        while len(upper) >= 3:
            o, a, b = upper[-3][1], upper[-2][1], upper[-1][1]
            cross = (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
            if cross <= 1e-12:
                removed = upper[-2][0]
                upper.pop(-2)
                steps.append(("upper: pop " + str(removed), [x[1] for x in upper], {removed}))
            else:
                break
    final = lower[:-1] + upper[:-1]
    steps.append(("final hull", [x[1] for x in final], set()))
    return steps


sure_steps = monotone_steps({p.label: p.sure() for p in points})
real_steps = monotone_steps({p.label: p.realized() for p in points})
nframes = max(len(sure_steps), len(real_steps)) + 12

fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4))


#------------------ function draw_projection
def draw_projection(ax, title, coords_by_label, steps, frame):
    setup_axes(ax, title, (-1.2, 4.9), (-0.5, 3.6))
    for lab, pt in coords_by_label.items():
        ax.plot(pt[0], pt[1], marker="o", linestyle="None")
        status = ""
        if frame >= nframes - 10:
            if lab in hull.certified_vertices:
                status = " H+"
            elif lab in hull.uncertain_vertices:
                status = " H?"
        ax.text(pt[0] + 0.05, pt[1] + 0.05, f"{lab}{status}")
    idx = min(frame, len(steps) - 1)
    caption, chain, popped = steps[idx]
    plot_polyline(ax, chain, closed=(caption == "final hull" or frame >= nframes - 10), linewidth=2.0)
    ax.text(0.02, 0.96, caption, transform=ax.transAxes, va="top")
    if popped:
        ax.text(0.02, 0.89, "orientation test removes: " + ", ".join(map(str, popped)), transform=ax.transAxes, va="top")


#------------------ function update
def update(frame):
    draw_projection(axes[0], "Sure projection: monotone chain", {p.label: p.sure() for p in points}, sure_steps, frame)
    draw_projection(axes[1], "Realized projection: monotone chain", {p.label: p.realized() for p in points}, real_steps, frame)
    if frame >= nframes - 10:
        axes[0].text(0.02, 0.10, f"H+ = {sorted(hull.certified_vertices)}", transform=axes[0].transAxes)
        axes[1].text(0.02, 0.10, f"H? = {sorted(hull.uncertain_vertices)}", transform=axes[1].transAxes)


ani = FuncAnimation(fig, update, frames=nframes, interval=350, repeat=True)
path = OUTPUT_DIR / "03_convex_hull_scan.gif"
ani.save(path, writer=PillowWriter(fps=3))
print(f"[saved] {path}")
