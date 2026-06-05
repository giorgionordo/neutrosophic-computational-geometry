"""
Package Neutrosophic Computational Geometry (NCG)
_plotting.py

Auxiliary module that collects plotting utilities for the NCG
examples and visual demonstrations.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from ncg.geometry.point import NPoint2, Point2, Box2

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


#------------------ function setup_axes
def setup_axes(ax, title: str, equal: bool = True):
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    if equal:
        ax.set_aspect('equal', adjustable='box')


#------------------ function save_figure
def save_figure(fig, filename: str):
    path = OUTPUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches='tight')
    print(f"[saved] {path}")
    return path


#------------------ function draw_npoint
def draw_npoint(ax, p: NPoint2, annotate: bool = True, dx: float = 0.04, dy: float = 0.04):
    xs, ys = p.sure()
    xr, yr = p.realized()
    ax.plot(xs, ys, marker='o', linestyle='None')
    ax.plot(xr, yr, marker='s', linestyle='None')
    ax.plot([xs, xr], [ys, yr], linestyle=':', linewidth=1.0)
    if annotate and p.label is not None:
        ax.text(xs + dx, ys + dy, f"{p.label}_s")
        ax.text(xr + dx, yr - dy, f"{p.label}_r")


#------------------ function draw_box
def draw_box(ax, box: Box2, label: str | None = None, alpha: float = 0.15):
    xmin, ymin, xmax, ymax = box
    rect = Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, fill=True, alpha=alpha, linewidth=1.2)
    ax.add_patch(rect)
    if label is not None:
        ax.text((xmin + xmax) / 2.0, (ymin + ymax) / 2.0, label, ha='center', va='center')
    return rect


#------------------ function close_polygon
def close_polygon(points: Sequence[Point2]) -> list[Point2]:
    pts = list(points)
    if pts and pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


#------------------ function plot_polygon
def plot_polygon(ax, points: Sequence[Point2], linestyle='-', linewidth=1.8, label: str | None = None):
    pts = close_polygon(points)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, linestyle=linestyle, linewidth=linewidth, label=label)


#------------------ function fill_polygon
def fill_polygon(ax, points: Sequence[Point2], alpha: float = 0.12):
    pts = close_polygon(points)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.fill(xs, ys, alpha=alpha)
