"""
Package Neutrosophic Computational Geometry (NCG)
launcher.py

Launcher module that opens the graphical demonstrations of the
Neutrosophic Computational Geometry package.

----------------------------------------------------------------------------------
author: Giorgio Nordo - Dipartimento MIFT. Università di Messina, Italy
www.nordo.it   |  giorgio.nordo@unime.it
"""

from __future__ import annotations

#------------------ import of required modules
from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import ttk

HERE = Path(__file__).resolve().parent
SCRIPTS = [
    ("AH projection / scenario parameter", "01_gui_ah_projection.py"),
    ("Orientation sign-state", "02_gui_orientation_sign.py"),
    ("Convex hull certified labels", "03_gui_convex_hull.py"),
    ("Box-aware point location", "04_gui_point_location.py"),
    ("Nearest-site state", "05_gui_voronoi_nearest.py"),
]

root = tk.Tk()
root.title("NCG interactive GUI examples")
root.geometry("520x300")
frame = ttk.Frame(root, padding=12)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Neutrosophic Computational Geometry - GUI examples", font=("TkDefaultFont", 11, "bold")).pack(anchor="w", pady=(0, 10))


#------------------ function run
def run(script: str):
    subprocess.Popen([sys.executable, str(HERE / script)])

for label, script in SCRIPTS:
    ttk.Button(frame, text=label, command=lambda s=script: run(s)).pack(fill=tk.X, pady=4)

root.mainloop()
