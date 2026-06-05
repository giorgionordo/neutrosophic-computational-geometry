"""
Package Neutrosophic Computational Geometry (NCG)
07_non_polynomial_lifting_advanced.py

Example script that illustrates 07 non polynomial lifting advanced
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

from math import log1p

from ncg import NPoint2, NRN
from ncg.geometry.primitives import compare_dist2, dist, dist2
from examples._plotting import draw_npoint, save_figure, setup_axes

x = NRN.from_interval(3.0, 4.0)
sqrt_x = x.sqrt()
log_x = x.lift_function(log1p)
print("functional lifting")
print("  x AH:", x.ah())
print("  sqrt(x) AH:", sqrt_x.ah())
print("  log1p(x) AH:", log_x.ah())

Q = NPoint2.from_intervals((0.0, 0.2), (0.0, 0.0), "Q")
A = NPoint2(1.0, 0.0, "A")
B = NPoint2.from_intervals((1.1, 0.85), (0.0, 0.0), "B")

print("\ndistances from query")
print("  dist2(Q,A) AH:", dist2(Q, A).ah())
print("  dist2(Q,B) AH:", dist2(Q, B).ah())
print("  dist(Q,A)  AH:", dist(Q, A).ah())
print("  dist(Q,B)  AH:", dist(Q, B).ah())
print("  comparison by squares:", compare_dist2(Q, A, B, eps=0.0))

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
ax0, ax1 = axes
setup_axes(ax0, "Componentwise functional lifting", equal=False)
labels = ['x', 'sqrt(x)', 'log1p(x)']
sure_vals = [x.sure, sqrt_x.sure, log_x.sure]
real_vals = [x.realized, sqrt_x.realized, log_x.realized]
idx = list(range(len(labels)))
ax0.plot(idx, sure_vals, marker='o', linestyle='--', label='sure')
ax0.plot(idx, real_vals, marker='s', linestyle='-', label='realized')
ax0.set_xticks(idx)
ax0.set_xticklabels(labels)
ax0.legend()
ax0.grid(True, alpha=0.25)

setup_axes(ax1, "Distance comparison by squared distances")
for p in [Q, A, B]:
    draw_npoint(ax1, p)
ax1.plot([Q.sure()[0], A.sure()[0]], [Q.sure()[1], A.sure()[1]], linestyle='--', label='Q_s A_s')
ax1.plot([Q.realized()[0], A.realized()[0]], [Q.realized()[1], A.realized()[1]], linestyle=':', label='Q_r A_r')
ax1.plot([Q.sure()[0], B.sure()[0]], [Q.sure()[1], B.sure()[1]], linestyle='--', label='Q_s B_s')
ax1.plot([Q.realized()[0], B.realized()[0]], [Q.realized()[1], B.realized()[1]], linestyle='-', label='Q_r B_r')
ax1.legend(loc='upper right', fontsize=8)
ax1.text(0.02, 0.98, f"compare dist^2: {compare_dist2(Q,A,B,eps=0.0)}", transform=ax1.transAxes, va='top')

save_figure(fig, '07_non_polynomial_lifting_advanced.png')
