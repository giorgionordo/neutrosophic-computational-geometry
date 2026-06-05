"""
Package Neutrosophic Computational Geometry (NCG)
01_sign_state_logic.py

Example script that illustrates 01 sign state logic
within the Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ncg.algebra.nrn import NRN
from ncg.algebra.predicates import SignState, cayley_product_table, sign_nrn_pair, sgn_n


#------------------ function fmt_state
def fmt_state(s: SignState) -> str:
    return str(s)


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
