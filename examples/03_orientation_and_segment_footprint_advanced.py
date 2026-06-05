"""
Package Neutrosophic Computational Geometry (NCG)
03_orientation_and_segment_footprint_advanced.py

Example script that illustrates 03 orientation and segment footprint advanced
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg import NPoint2, NRN
from ncg.geometry.primitives import epsilon_collinear, orientation, orientation_state, segment_footprint, signed_area2
from examples._plotting import draw_npoint, save_figure, setup_axes, plot_polygon

A = NPoint2(0.0, 0.0, "A")
B = NPoint2(2.0, 0.0, "B")
C = NPoint2(NRN.from_ah(1.0, 1.0), NRN.from_ah(1.0e-8, -1.0e-8), "C")

area = signed_area2(A, B, C)
print("signed area AH:", area.ah())
print("orientation state:", orientation_state(A, B, C, eps=0.0))
print("orientation label:", orientation(A, B, C, eps=0.0))
print("epsilon-collinear at eps=1e-7:", epsilon_collinear(A, B, C, 1e-7))
print("epsilon-collinear at eps=1e-10:", epsilon_collinear(A, B, C, 1e-10))

P = NPoint2.from_intervals((0.0, 0.15), (0.0, 0.10), "P")
Q = NPoint2.from_intervals((2.0, 2.20), (1.0, 0.85), "Q")
foot = segment_footprint(P, Q)
print("\nsegment footprint endpoints P_s,P_r,Q_s,Q_r:")
for item in foot:
    print(" ", item)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
ax0, ax1 = axes
setup_axes(ax0, "Mixed orientation")
for p in [A, B, C]:
    draw_npoint(ax0, p)
plot_polygon(ax0, [A.sure(), B.sure(), C.sure()], linestyle='--', label='sure triangle')
plot_polygon(ax0, [A.realized(), B.realized(), C.realized()], linestyle='-', label='realized triangle')
ax0.legend(loc='upper right')
ax0.text(0.5, 0.92, f"state = {orientation_state(A,B,C,0.0)}", transform=ax0.transAxes)

setup_axes(ax1, "Segment footprint")
draw_npoint(ax1, P)
draw_npoint(ax1, Q)
poly = list(foot) + [foot[0]]
ax1.fill([u[0] for u in poly], [u[1] for u in poly], alpha=0.12)
ax1.plot([P.sure()[0], Q.sure()[0]], [P.sure()[1], Q.sure()[1]], linestyle='--', label='sure segment')
ax1.plot([P.realized()[0], Q.realized()[0]], [P.realized()[1], Q.realized()[1]], linestyle='-', label='realized segment')
ax1.legend(loc='upper left')

save_figure(fig, '03_orientation_and_segment_footprint_advanced.png')
