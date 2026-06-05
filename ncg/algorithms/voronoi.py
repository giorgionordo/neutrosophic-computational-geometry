"""
Package Neutrosophic Computational Geometry (NCG)
voronoi.py

Module that implements reference Voronoi and nearest-neighbour
routines in the AH-lifted neutrosophic setting.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from dataclasses import dataclass
from math import hypot
from typing import Sequence

from ncg.algebra.predicates import SignState, sgn_n
from ncg.geometry.point import NPoint2, label_of
from ncg.geometry.primitives import dist2


#------------------ class NearestResult
@dataclass(frozen=True)
class NearestResult:
    certified_label: object | None
    competing_labels: set[object]
    distances: dict[object, tuple[float, float]]

    # method definite_label
    @property
    def definite_label(self):
        return self.certified_label


#------------------ function nearest_neighbor
def nearest_neighbor(query: NPoint2, sites: Sequence[NPoint2], eps: float = 1e-12) -> NearestResult:
    """Return a certified nearest site if both AH projections agree."""
    if not sites:
        raise ValueError("At least one site is required")
    labelled = [(label_of(s, i), s) for i, s in enumerate(sites)]
    d = {lab: dist2(query, site).ah() for lab, site in labelled}
    min_s = min(v[0] for v in d.values())
    min_r = min(v[1] for v in d.values())
    labs_s = {lab for lab, (ds, _) in d.items() if ds <= min_s + eps}
    labs_r = {lab for lab, (_, dr) in d.items() if dr <= min_r + eps}
    if len(labs_s) == len(labs_r) == 1 and labs_s == labs_r:
        return NearestResult(next(iter(labs_s)), labs_s, d)
    return NearestResult(None, labs_s | labs_r, d)


#------------------ function potential_voronoi_boundary
def potential_voronoi_boundary(query: NPoint2, p: NPoint2, q: NPoint2, eps: float = 1e-12) -> bool:
    """Return true when the bisector state between two sites is non-certified."""
    return sgn_n(dist2(query, p) - dist2(query, q), eps) != SignState.POS and sgn_n(
        dist2(query, p) - dist2(query, q), eps
    ) != SignState.NEG


#------------------ function coherent_perturbation_scale
def coherent_perturbation_scale(sites: Sequence[NPoint2]) -> tuple[float, float]:
    """Return ``(max_displacement, min_sure_site_distance)``.

    This simple diagnostic supports the coherent-perturbation discussion in the
    paper: when the displacement is small with respect to the minimum sure
    site distance, the realized Voronoi diagram is expected to be a local
    perturbation of the sure diagram.
    """
    pts = list(sites)
    if len(pts) < 2:
        return 0.0, float("inf")
    max_disp = max(hypot(p.realized()[0] - p.sure()[0], p.realized()[1] - p.sure()[1]) for p in pts)
    min_dist = float("inf")
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            a, b = pts[i].sure(), pts[j].sure()
            min_dist = min(min_dist, hypot(a[0] - b[0], a[1] - b[1]))
    return max_disp, min_dist
