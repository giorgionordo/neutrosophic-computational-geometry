"""
Package Neutrosophic Computational Geometry (NCG)
point.py

Module that defines Euclidean and neutrosophic points used by the
AH-lifted computational geometry routines.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from dataclasses import dataclass
from typing import Iterable, Tuple

from ncg.algebra.nrn import NRN, as_nrn, meet_all, join_all

Point2 = Tuple[float, float]
Box2 = Tuple[float, float, float, float]  # xmin, ymin, xmax, ymax


#------------------ class NPoint2
@dataclass(frozen=True)
class NPoint2:
    """A labelled point in ``R(I)^2`` with sure and realized AH projections."""

    x: NRN
    y: NRN
    label: str | int | None = None

    # method __init__
    def __init__(self, x: NRN | float, y: NRN | float, label: str | int | None = None):
        object.__setattr__(self, "x", as_nrn(x))
        object.__setattr__(self, "y", as_nrn(y))
        object.__setattr__(self, "label", label)

    # method from_intervals
    @classmethod
    def from_intervals(
        cls,
        x_interval: Tuple[float, float],
        y_interval: Tuple[float, float],
        label: str | int | None = None,
    ) -> "NPoint2":
        """Encode coordinate intervals by ``a+(b-a)I``."""
        return cls(NRN.from_interval(*x_interval), NRN.from_interval(*y_interval), label)

    # method sure
    def sure(self) -> Point2:
        return (self.x.sure, self.y.sure)

    # method realized
    def realized(self) -> Point2:
        return (self.x.realized, self.y.realized)

    # method ah
    def ah(self) -> Tuple[Point2, Point2]:
        return self.sure(), self.realized()

    # method uncertainty_box
    def uncertainty_box(self) -> Box2:
        xs, ys = self.sure()
        xr, yr = self.realized()
        return (min(xs, xr), min(ys, yr), max(xs, xr), max(ys, yr))

    # method bbox
    def bbox(self) -> Box2:
        return self.uncertainty_box()

    # method __sub__
    def __sub__(self, other: "NPoint2") -> "NVector2":
        return NVector2(self.x - other.x, self.y - other.y)

    # method __add__
    def __add__(self, v: "NVector2") -> "NPoint2":
        return NPoint2(self.x + v.x, self.y + v.y, self.label)


#------------------ class NVector2
@dataclass(frozen=True)
class NVector2:
    x: NRN
    y: NRN

    # method __init__
    def __init__(self, x: NRN | float, y: NRN | float):
        object.__setattr__(self, "x", as_nrn(x))
        object.__setattr__(self, "y", as_nrn(y))

    # method sure
    def sure(self) -> Point2:
        return (self.x.sure, self.y.sure)

    # method realized
    def realized(self) -> Point2:
        return (self.x.realized, self.y.realized)

    # method ah
    def ah(self) -> Tuple[Point2, Point2]:
        return self.sure(), self.realized()

    # method __add__
    def __add__(self, other: "NVector2") -> "NVector2":
        return NVector2(self.x + other.x, self.y + other.y)

    # method __sub__
    def __sub__(self, other: "NVector2") -> "NVector2":
        return NVector2(self.x - other.x, self.y - other.y)

    # method __neg__
    def __neg__(self) -> "NVector2":
        return NVector2(-self.x, -self.y)

    # method __mul__
    def __mul__(self, scalar: NRN | float) -> "NVector2":
        scalar = as_nrn(scalar)
        return NVector2(self.x * scalar, self.y * scalar)

    # method __rmul__
    def __rmul__(self, scalar: NRN | float) -> "NVector2":
        return self.__mul__(scalar)


#------------------ function label_of
def label_of(p: NPoint2, fallback: int | None = None):
    return p.label if p.label is not None else fallback


#------------------ function labels
def labels(points: Iterable[NPoint2]) -> list[str | int | None]:
    return [p.label for p in points]


#------------------ function neutrosophic_bounding_box
def neutrosophic_bounding_box(points: Iterable[NPoint2]) -> Tuple[NRN, NRN, NRN, NRN]:
    """Lattice bounding box ``(x-, y-, x+, y+)`` in ``R(I)^2``.

    The meet/join operations preserve AH label-coupling; the returned endpoints
    are neutrosophic coordinates rather than unrelated interval extrema.
    """
    pts = list(points)
    if not pts:
        raise ValueError("At least one point is required")
    xmin = meet_all(p.x for p in pts)
    xmax = join_all(p.x for p in pts)
    ymin = meet_all(p.y for p in pts)
    ymax = join_all(p.y for p in pts)
    return xmin, ymin, xmax, ymax
