"""
Package Neutrosophic Computational Geometry (NCG)
_animation_helpers.py

Auxiliary module that collects reusable helpers for the animated
visual demonstrations of AH-lifted geometry.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from pathlib import Path
import matplotlib.pyplot as plt

from ncg.geometry.point import NPoint2

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output" / "animations"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


#------------------ function setup_axes
def setup_axes(ax, title: str, xlim=None, ylim=None, equal=True):
    ax.clear()
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)


#------------------ function interp_point
def interp_point(p: NPoint2, t: float):
    xs, ys = p.sure()
    xr, yr = p.realized()
    return (xs + t * (xr - xs), ys + t * (yr - ys))


#------------------ function draw_point_pair
def draw_point_pair(ax, p: NPoint2, label=True):
    xs, ys = p.sure()
    xr, yr = p.realized()
    ax.plot(xs, ys, marker="o", linestyle="None")
    ax.plot(xr, yr, marker="s", linestyle="None")
    ax.plot([xs, xr], [ys, yr], linestyle=":", linewidth=1.0)
    if label and p.label is not None:
        ax.text(xs + 0.04, ys + 0.04, f"{p.label}_s")
        ax.text(xr + 0.04, yr - 0.07, f"{p.label}_r")


#------------------ function close
def close(poly):
    pts = list(poly)
    if pts and pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


#------------------ function plot_polyline
def plot_polyline(ax, pts, closed=False, **kwargs):
    pts = list(pts)
    if closed:
        pts = close(pts)
    if not pts:
        return
    ax.plot([p[0] for p in pts], [p[1] for p in pts], **kwargs)
