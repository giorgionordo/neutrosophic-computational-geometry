"""
Package Neutrosophic Computational Geometry (NCG)
01_sign_state_logic_advanced.py

Example script that illustrates 01 sign state logic advanced
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

from ncg.algebra.nrn import NRN
from ncg.algebra.predicates import SignState, cayley_product_table, sign_nrn_pair, sgn_n
from examples._plotting import save_figure

values = {
    "positive certified": NRN.from_ah(2.0, 3.0),
    "negative certified": NRN.from_ah(-3.0, -1.0),
    "strong zero": NRN.from_ah(0.0, 0.0),
    "mixed sign": NRN.from_ah(-1.0, 2.0),
    "weak zero": NRN.from_ah(0.0, 4.0),
}

print("sgn_N examples")
for name, x in values.items():
    pair = tuple(str(s) for s in sign_nrn_pair(x, eps=0.0))
    print(f"  {name:20s} AH={x.ah()} signs={pair} -> {sgn_n(x, eps=0.0)}")

states = [SignState.NEG, SignState.ZERO, SignState.POS, SignState.MIXED]
table = cayley_product_table()
print("\nCayley product table in S_N")
header = "      " + " ".join(f"{str(s):>3s}" for s in states)
print(header)
for a in states:
    row = [f"{str(table[(a, b)]):>3s}" for b in states]
    print(f"{str(a):>3s} | " + " ".join(row))

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
ax0, ax1 = axes
ax0.axis('off')
ax1.axis('off')

pair_rows = []
for name, x in values.items():
    sig_s, sig_r = sign_nrn_pair(x, eps=0.0)
    pair_rows.append([name, f"{sig_s}", f"{sig_r}", f"{sgn_n(x, eps=0.0)}"])

ax0.set_title("Quotient sign map")
t0 = ax0.table(
    cellText=pair_rows,
    colLabels=["example", r"$\sigma_s$", r"$\sigma_r$", r"$\operatorname{sgn}_N$"],
    loc='center',
    cellLoc='center',
)
t0.auto_set_font_size(False)
t0.set_fontsize(9)
t0.scale(1.05, 1.6)

ax1.set_title("Cayley product table in $S_N$")
cell_rows = [[str(table[(a, b)]) for b in states] for a in states]
t1 = ax1.table(
    cellText=cell_rows,
    rowLabels=[str(s) for s in states],
    colLabels=[str(s) for s in states],
    loc='center',
    cellLoc='center',
)
t1.auto_set_font_size(False)
t1.set_fontsize(10)
t1.scale(1.15, 1.8)
ax1.text(0.5, 0.05, r"$?$ is absorbing for precision, except $0\cdot ? = 0$.", ha='center', transform=ax1.transAxes)

save_figure(fig, '01_sign_state_logic_advanced.png')
