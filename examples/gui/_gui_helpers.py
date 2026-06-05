"""
Package Neutrosophic Computational Geometry (NCG)
_gui_helpers.py

Auxiliary module that collects reusable helpers for the graphical
interfaces of the NCG examples.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


#------------------ function make_root
def make_root(title: str, geometry: str = "1040x720") -> tk.Tk:
    root = tk.Tk()
    root.title(title)
    root.geometry(geometry)
    return root


#------------------ function make_figure
def make_figure(root: tk.Tk, figsize=(7.2, 5.2)):
    fig = Figure(figsize=figsize, dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    return fig, ax, canvas


#------------------ function controls_frame
def controls_frame(root: tk.Tk) -> ttk.Frame:
    frame = ttk.Frame(root, padding=8)
    frame.pack(side=tk.BOTTOM, fill=tk.X)
    return frame


#------------------ function slider
def slider(frame: ttk.Frame, label: str, from_: float, to: float, initial: float, command, row: int, resolution=0.01):
    var = tk.DoubleVar(value=initial)
    ttk.Label(frame, text=label, width=26).grid(row=row, column=0, sticky="w")
    scale = ttk.Scale(frame, from_=from_, to=to, variable=var, command=lambda _v: command())
    scale.grid(row=row, column=1, sticky="ew", padx=6)
    value_label = ttk.Label(frame, text=f"{initial:.2f}", width=8)
    value_label.grid(row=row, column=2, sticky="e")
    # method update_label
    def update_label(*_):
        value_label.configure(text=f"{var.get():.2f}")
    var.trace_add("write", update_label)
    frame.columnconfigure(1, weight=1)
    return var


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


#------------------ function draw_point
def draw_point(ax, pt, label, marker="o"):
    ax.plot(pt[0], pt[1], marker=marker, linestyle="None")
    ax.text(pt[0] + 0.04, pt[1] + 0.04, label)


#------------------ function plot_polyline
def plot_polyline(ax, pts, closed=False, **kwargs):
    pts = list(pts)
    if closed and pts:
        pts = pts + [pts[0]]
    if pts:
        ax.plot([p[0] for p in pts], [p[1] for p in pts], **kwargs)


#------------------ function point_at
def point_at(p, t: float):
    xs, ys = p.sure()
    xr, yr = p.realized()
    return (xs + t * (xr - xs), ys + t * (yr - ys))
