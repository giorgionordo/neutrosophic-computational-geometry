"""
Package Neutrosophic Computational Geometry (NCG)
primitives.py

Module that implements the basic geometric predicates and primitives
used in the neutrosophic computational geometry algorithms.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from typing import Tuple

from ncg.algebra.nrn import NRN
from ncg.algebra.predicates import SignState, sgn_n
from .point import NPoint2, NVector2, Point2


#------------------ function det2
def det2(u: Point2, v: Point2) -> float:
    ux, uy = u
    vx, vy = v
    return ux * vy - uy * vx


#------------------ function signed_area2
def signed_area2(a: NPoint2, b: NPoint2, c: NPoint2) -> NRN:
    """Neutrosophic signed double area of triangle ``abc``."""
    a_s, b_s, c_s = a.sure(), b.sure(), c.sure()
    a_r, b_r, c_r = a.realized(), b.realized(), c.realized()
    det_s = det2((b_s[0] - a_s[0], b_s[1] - a_s[1]), (c_s[0] - a_s[0], c_s[1] - a_s[1]))
    det_r = det2((b_r[0] - a_r[0], b_r[1] - a_r[1]), (c_r[0] - a_r[0], c_r[1] - a_r[1]))
    return NRN.from_ah(det_s, det_r)


#------------------ function orientation_state
def orientation_state(a: NPoint2, b: NPoint2, c: NPoint2, eps: float = 1e-12) -> SignState:
    """Return the sign-state of the AH-lifted orientation predicate."""
    return sgn_n(signed_area2(a, b, c), eps)


#------------------ function orientation
def orientation(a: NPoint2, b: NPoint2, c: NPoint2, eps: float = 1e-12) -> str:
    """Return ``CCW``, ``CW``, ``COLLINEAR`` or ``MIXED``."""
    state = orientation_state(a, b, c, eps)
    return {
        SignState.POS: "CCW",
        SignState.NEG: "CW",
        SignState.ZERO: "COLLINEAR",
        SignState.MIXED: "MIXED",
    }[state]


#------------------ function epsilon_collinear
def epsilon_collinear(a: NPoint2, b: NPoint2, c: NPoint2, eps_s: float, eps_r: float | None = None) -> bool:
    """Return true iff both projected signed areas are inside their tolerance bands."""
    eps_r = eps_s if eps_r is None else eps_r
    area = signed_area2(a, b, c)
    return abs(area.sure) <= eps_s and abs(area.realized) <= eps_r


#------------------ function perp
def perp(v: NVector2) -> NVector2:
    return NVector2(-v.y, v.x)


#------------------ function dot
def dot(u: NVector2, v: NVector2) -> NRN:
    return u.x * v.x + u.y * v.y


#------------------ function norm2
def norm2(v: NVector2) -> NRN:
    return dot(v, v)


#------------------ function dist2
def dist2(p: NPoint2, q: NPoint2) -> NRN:
    return norm2(p - q)


#------------------ function dist
def dist(p: NPoint2, q: NPoint2) -> NRN:
    """Euclidean distance lifted by the AH functional calculus."""
    return dist2(p, q).sqrt()


#------------------ function compare_dist2
def compare_dist2(p: NPoint2, q: NPoint2, r: NPoint2, eps: float = 1e-12) -> str:
    """Compare ``||p-q||`` and ``||p-r||`` by squared distances.

    Squared distances are polynomial predicates, so no square roots are needed.
    """
    state = sgn_n(dist2(p, q) - dist2(p, r), eps)
    if state == SignState.NEG:
        return "Q_NEARER"
    if state == SignState.POS:
        return "R_NEARER"
    if state == SignState.ZERO:
        return "EQUAL"
    return "MIXED"


#------------------ function segment_footprint
def segment_footprint(p: NPoint2, q: NPoint2) -> Tuple[Point2, Point2, Point2, Point2]:
    """Return the four projected endpoints of a neutrosophic segment."""
    return p.sure(), p.realized(), q.sure(), q.realized()
