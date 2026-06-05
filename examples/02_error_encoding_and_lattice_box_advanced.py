"""
Package Neutrosophic Computational Geometry (NCG)
02_error_encoding_and_lattice_box_advanced.py

Example script that illustrates 02 error encoding and lattice box advanced
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NPoint2, NRN
from ncg.geometry.point import neutrosophic_bounding_box
from examples._plotting import draw_box, draw_npoint, save_figure, setup_axes

print("interval encoding")
for interval in [(1.0, 1.25), (-0.1, 0.2), (3.0, 3.0)]:
    x = NRN.from_interval(*interval)
    print(f"  x in {interval} -> {x!r}, AH={x.ah()}")

points = [
    NPoint2.from_intervals((0.0, 0.08), (0.0, 0.02), "A"),
    NPoint2.from_intervals((2.0, 2.10), (0.4, 0.30), "B"),
    NPoint2.from_intervals((1.4, 1.55), (1.7, 1.85), "C"),
    NPoint2.from_intervals((-0.2, -0.05), (1.1, 1.00), "D"),
]

xmin, ymin, xmax, ymax = neutrosophic_bounding_box(points)
print("\nneutrosophic lattice bounding box")
print("  x- AH:", xmin.ah())
print("  y- AH:", ymin.ah())
print("  x+ AH:", xmax.ah())
print("  y+ AH:", ymax.ah())

fig, ax = plt.subplots(figsize=(7.2, 5.8))
setup_axes(ax, "Practical error encoding and lattice bounding box")
for p in points:
    draw_npoint(ax, p)
    draw_box(ax, p.bbox(), alpha=0.08)

# sure and realized global boxes
xs = [p.sure()[0] for p in points]
ys = [p.sure()[1] for p in points]
xr = [p.realized()[0] for p in points]
yr = [p.realized()[1] for p in points]

sure_box = Rectangle((min(xs), min(ys)), max(xs)-min(xs), max(ys)-min(ys), fill=False, linestyle='--', linewidth=1.8)
real_box = Rectangle((min(xr), min(yr)), max(xr)-min(xr), max(yr)-min(yr), fill=False, linewidth=2.0)
ax.add_patch(sure_box)
ax.add_patch(real_box)
ax.text(min(xs), max(ys)+0.08, "sure bounding box")
ax.text(min(xr), min(yr)-0.14, "realized bounding box")

lx0, ly0 = xmin.sure, ymin.sure
lx1, ly1 = xmax.realized, ymax.realized
ax.plot([lx0, lx1], [ly0, ly0], linestyle=':')
ax.plot([lx1, lx1], [ly0, ly1], linestyle=':')
ax.plot([lx1, lx0], [ly1, ly1], linestyle=':')
ax.plot([lx0, lx0], [ly1, ly0], linestyle=':')
ax.text((lx0+lx1)/2, (ly0+ly1)/2, r"AH-coupled box endpoints", ha='center')

save_figure(fig, '02_error_encoding_and_lattice_box_advanced.png')
