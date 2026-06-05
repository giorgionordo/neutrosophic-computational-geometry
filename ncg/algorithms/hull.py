"""
Package Neutrosophic Computational Geometry (NCG)
hull.py

Module that implements the AH-lifted neutrosophic convex hull by
combining the two projected Euclidean hulls.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from dataclasses import dataclass
from typing import Sequence

from ncg.algebra.predicates import SignState
from ncg.geometry.point import NPoint2, Point2, label_of
from ncg.geometry.primitives import orientation_state


#------------------------------------------------------------------------------------

# auxiliary function that computes the planar cross product of three Euclidean points
def _cross(o: Point2, a: Point2, b: Point2) -> float:
    """
    Auxiliary function that computes the oriented area of the triangle oab.

    ----
    Parameters:
    - o: first point, used as origin of the two vectors
    - a: second point
    - b: third point

    Returns:
    - positive value if the turn is counterclockwise;
    - negative value if the turn is clockwise;
    - zero value in the collinear case.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


#------------------------------------------------------------------------------------

# auxiliary function that builds the classical hull by the monotone chain algorithm
def _monotone_chain(items: list[tuple[Point2, object]], eps: float = 1e-12) -> list[object]:
    """
    Classical convex hull labels in counterclockwise order.

    ----
    Parameters:
    - items: list of pairs constituted by a Euclidean point and its label
    - eps: tolerance used in the orientation test

    Returns:
    - list of labels of the vertices of the convex hull.
    """
    # sorts points lexicographically by coordinates and then by label
    items = sorted(items, key=lambda z: (z[0][0], z[0][1], str(z[1])))

    # treats separately the empty case or the one-point case
    if len(items) <= 1:
        return [items[0][1]] if items else []

    # builds a boundary chain by removing non-left turns
    def build(seq):
        hull: list[tuple[Point2, object]] = []
        for p in seq:
            # removes the last point until the chain becomes convex within the fixed tolerance
            while len(hull) >= 2 and _cross(hull[-2][0], hull[-1][0], p[0]) <= eps:
                hull.pop()
            hull.append(p)
        return hull

    # builds the lower and upper chains of the hull
    lower = build(items)
    upper = build(reversed(items))

    # returns the labels while avoiding repeated shared endpoints
    return [lab for _, lab in lower[:-1] + upper[:-1]]


#------------------------------------------------------------------------------------

#------------------ class HullResult
@dataclass(frozen=True)
class HullResult:
    """
    Data structure that stores the result of the neutrosophic convex hull.

    ----
    Fields:
    - sure_hull: labels of the convex hull in the sure projection
    - realized_hull: labels of the convex hull in the realized projection
    - certified_vertices: labels appearing in both projected hulls
    - uncertain_vertices: labels appearing in only one projection or involved in mixed cases
    - mixed_orientation_labels: labels involved in mixed or degenerate orientation decisions
    """

    sure_hull: list[object]
    realized_hull: list[object]
    certified_vertices: set[object]
    uncertain_vertices: set[object]
    mixed_orientation_labels: set[object]

    # property that keeps an alternative name for certified vertices
    @property
    def definite_vertices(self) -> set[object]:
        """
        Property that returns the certified vertices using the alternative name
        definite_vertices.
        """
        return self.certified_vertices


#------------------------------------------------------------------------------------

# main function that computes the neutrosophic hull by AH lifting
def neutrosophic_convex_hull(points: Sequence[NPoint2], eps: float = 1e-12) -> HullResult:
    """
    Reference AH-lifted routine for the neutrosophic convex hull.

    The algorithm computes the classical convex hull separately in the sure and
    realized AH projections.  The intersection of the two sets of labels gives
    the certified vertices, whereas the symmetric difference gives the first
    group of uncertain vertices.  Further uncertain labels are obtained from
    mixed or degenerate neutrosophic orientation tests.

    ----
    Parameters:
    - points: sequence of neutrosophic points in the plane
    - eps: tolerance used in the orientation tests

    Returns:
    - HullResult object containing projected hulls, certified labels and uncertain labels.
    """
    # converts the sequence into a list in order to scan it more than once
    pts = list(points)

    # associates each point with its own label or with a label generated from its position
    labelled = [(label_of(p, i), p) for i, p in enumerate(pts)]

    # builds the two lists of projected points according to the AH components
    sure_items = [(p.sure(), lab) for lab, p in labelled]
    realized_items = [(p.realized(), lab) for lab, p in labelled]

    # computes separately the hull of the sure projection and of the realized projection
    h_s = _monotone_chain(sure_items, eps)
    h_r = _monotone_chain(realized_items, eps)

    # transforms the label lists into sets in order to compare the two projected hulls
    set_s, set_r = set(h_s), set(h_r)

    # vertices appearing in both projections are certified
    certified = set_s & set_r

    # vertices appearing in only one projection are initially classified as uncertain
    uncertain = set_s ^ set_r

    # set of labels involved in mixed or degenerate orientations
    mixed_labels: set[object] = set()

    # checks all triples of points in order to detect uncertified neutrosophic orientations
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            for k in range(j + 1, len(pts)):
                state = orientation_state(pts[i], pts[j], pts[k], eps)

                # treats mixed and zero orientations as non-certified cases
                if state in (SignState.MIXED, SignState.ZERO):
                    labs = {label_of(pts[i], i), label_of(pts[j], j), label_of(pts[k], k)}

                    # exposes only the labels that are relevant for at least one of the two projected hulls
                    mixed_labels |= labs & (set_s | set_r)

    # adds to the uncertain set the mixed labels that are not already certified
    uncertain |= mixed_labels - certified

    # returns all collected data in a single result object
    return HullResult(h_s, h_r, certified, uncertain, mixed_labels)
