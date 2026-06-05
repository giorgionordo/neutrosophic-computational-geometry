"""
Package Neutrosophic Computational Geometry (NCG)
test_basic.py

Test module that checks the basic algebraic, geometric and algorithmic
components of the NCG package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

#------------------ import of required modules
from ncg import NRN, NPoint2
from ncg.algebra.predicates import SignState, multiply_sign_states, sgn_n
from ncg.geometry.primitives import orientation, dot, perp, dist
from ncg.algorithms.hull import neutrosophic_convex_hull


#------------------ function test_ah_product
def test_ah_product():
    x = NRN(2, 3)      # AH (2,5)
    y = NRN(4, -1)     # AH (4,3)
    assert (x * y).almost_equal(NRN.from_ah(8, 15))


#------------------ function test_interval_encoding
def test_interval_encoding():
    assert NRN.from_interval(2, 5).ah() == (2, 5)


#------------------ function test_sign_mixed_product
def test_sign_mixed_product():
    assert multiply_sign_states(SignState.POS, SignState.MIXED) == SignState.MIXED
    assert multiply_sign_states(SignState.ZERO, SignState.MIXED) == SignState.ZERO


#------------------ function test_orientation_classical_reduction
def test_orientation_classical_reduction():
    a = NPoint2(0, 0, "A")
    b = NPoint2(1, 0, "B")
    c = NPoint2(0, 1, "C")
    assert orientation(a, b, c) == "CCW"


#------------------ function test_mixed_orientation
def test_mixed_orientation():
    a = NPoint2(0, 0, "A")
    b = NPoint2(1, 0, "B")
    c = NPoint2(NRN(0.5, 0), NRN(1e-16, -2e-16), "C")
    assert orientation(a, b, c, eps=0.0) == "MIXED"


#------------------ function test_perp_orthogonal
def test_perp_orthogonal():
    v = NPoint2(NRN(1, 2), NRN(3, -1)) - NPoint2(0, 0)
    assert dot(v, perp(v)).is_strong_zero(1e-12)


#------------------ function test_hull_labels
def test_hull_labels():
    pts = [NPoint2(0,0,"A"), NPoint2(1,0,"B"), NPoint2(0,1,"C"), NPoint2(0.2,0.2,"D")]
    hull = neutrosophic_convex_hull(pts)
    assert hull.certified_vertices == {"A", "B", "C"}
