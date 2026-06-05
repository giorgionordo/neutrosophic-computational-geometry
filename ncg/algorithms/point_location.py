"""
Package Neutrosophic Computational Geometry (NCG)
point_location.py

Module that implements box-aware point location for neutrosophic
points and polygonal subdivisions.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from dataclasses import dataclass
from typing import Sequence, Tuple

from ncg.geometry.point import NPoint2, Box2, Point2


#------------------ function _orient
def _orient(a: Point2, b: Point2, c: Point2) -> float:
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


#------------------ function _on_segment
def _on_segment(a: Point2, b: Point2, p: Point2, eps: float) -> bool:
    return (
        min(a[0], b[0])-eps <= p[0] <= max(a[0], b[0])+eps and
        min(a[1], b[1])-eps <= p[1] <= max(a[1], b[1])+eps and
        abs(_orient(a, b, p)) <= eps
    )


#------------------ function _segments_intersect
def _segments_intersect(a: Point2, b: Point2, c: Point2, d: Point2, eps: float) -> bool:
    o1, o2, o3, o4 = _orient(a,b,c), _orient(a,b,d), _orient(c,d,a), _orient(c,d,b)
    if o1*o2 < -eps and o3*o4 < -eps:
        return True
    return any([
        _on_segment(a,b,c,eps), _on_segment(a,b,d,eps),
        _on_segment(c,d,a,eps), _on_segment(c,d,b,eps)
    ])


#------------------ function point_in_polygon
def point_in_polygon(p: Point2, polygon: Sequence[Point2], eps: float = 1e-12) -> str:
    """Return ``INSIDE``, ``OUTSIDE`` or ``BOUNDARY`` for a simple polygon."""
    x, y = p
    inside = False
    n = len(polygon)
    for i in range(n):
        a, b = polygon[i], polygon[(i + 1) % n]
        if _on_segment(a, b, p, eps):
            return "BOUNDARY"
        xi, yi = a
        xj, yj = b
        crosses = (yi > y) != (yj > y)
        if crosses:
            xint = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xint:
                inside = not inside
    return "INSIDE" if inside else "OUTSIDE"


#------------------ function bbox_corners
def bbox_corners(box: Box2) -> list[Point2]:
    xmin, ymin, xmax, ymax = box
    return [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]


#------------------ function bbox_intersects_polygon_boundary
def bbox_intersects_polygon_boundary(box: Box2, polygon: Sequence[Point2], eps: float = 1e-12) -> bool:
    corners = bbox_corners(box)
    box_edges = list(zip(corners, corners[1:] + corners[:1]))
    poly_edges = list(zip(polygon, polygon[1:] + polygon[:1]))
    return any(_segments_intersect(a, b, c, d, eps) for a, b in box_edges for c, d in poly_edges)


#------------------ class LocationResult
@dataclass(frozen=True)
class LocationResult:
    status: str
    sure_status: str
    realized_status: str
    box: Box2
    candidate_faces: set[str] | None = None


#------------------ function locate_in_polygon
def locate_in_polygon(point: NPoint2, polygon: Sequence[Point2], eps: float = 1e-12) -> LocationResult:
    """Conservative location in one polygonal face.

    A unique status is certified only if both AH projections agree and the
    uncertainty box does not cross the boundary.
    """
    sure_status = point_in_polygon(point.sure(), polygon, eps)
    realized_status = point_in_polygon(point.realized(), polygon, eps)
    box = point.bbox()
    crosses = bbox_intersects_polygon_boundary(box, polygon, eps)
    if sure_status == realized_status == "INSIDE" and not crosses:
        return LocationResult("DEFINITELY_INSIDE", sure_status, realized_status, box, {"face"})
    if sure_status == realized_status == "OUTSIDE" and not crosses:
        return LocationResult("DEFINITELY_OUTSIDE", sure_status, realized_status, box, {"exterior"})
    return LocationResult("MIXED", sure_status, realized_status, box, {"face", "exterior"})
