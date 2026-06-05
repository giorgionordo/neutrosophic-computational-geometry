# AH-Lifting for Robust Computational Geometry — Python reference layer

This code accompanies the latest version of the manuscript.  It implements the
core mathematical mechanisms used in the paper:

- `ncg.algebra.nrn.NRN`: neutrosophic real numbers `a+bI`, AH map `(a,a+b)`,
  strong zero, weak-zero degeneracy, units and zero divisors;
- `NRN.from_interval(a,b)`: practical error encoding `x in [a,b] -> a+(b-a)I`;
- `ncg.algebra.predicates`: sign-state logic `S_N={-1,0,+1,?}`, the quotient
  operator `sgn_N(x)=qsgn(sgn(x_s),sgn(x_r))`, and the Cayley product table;
- `ncg.geometry`: AH-lifted points, vectors, uncertainty boxes, inner products,
  orientation, distances, and non-polynomial functional lifting for square roots;
- `ncg.algorithms`: reference hull, Voronoi nearest-site decision layer, coherent
  perturbation diagnostic, and box-aware point location.

Run the demo:

```bash
python examples/demo.py
```

Run the tests:

```bash
python -m pytest tests
```

No third-party dependency is required for the reference layer.

## Progressive examples

The `examples/` directory now contains a sequence of increasingly structured scripts:

1. `01_sign_state_logic.py` — quotient sign logic and Cayley table in `S_N`.
2. `02_error_encoding_and_lattice_box.py` — interval-to-neutrosophic encoding and lattice bounding boxes.
3. `03_orientation_and_segment_footprint.py` — mixed orientation, epsilon-collinearity and segment footprints.
4. `04_convex_hull_progressive.py` — certified and uncertain hull labels.
5. `05_voronoi_nearest_and_coherence.py` — nearest-site decisions and coherent perturbation diagnostics.
6. `06_box_aware_point_location.py` — uncertainty-box point location.
7. `07_non_polynomial_lifting.py` — square roots, functional lifting and distance comparison by squares.

Run all examples with:

```bash
for f in examples/0*.py; do python "$f"; done
```


## Advanced graphical examples

The `examples/` directory also contains advanced graphical counterparts:

- `01_sign_state_logic_advanced.py`
- `02_error_encoding_and_lattice_box_advanced.py`
- `03_orientation_and_segment_footprint_advanced.py`
- `04_convex_hull_progressive_advanced.py`
- `05_voronoi_nearest_and_coherence_advanced.py`
- `06_box_aware_point_location_advanced.py`
- `07_non_polynomial_lifting_advanced.py`

These scripts produce explanatory PNG figures in `examples/output/`.
They require `matplotlib`.

Run all advanced examples with:

```bash
for f in examples/*_advanced.py; do python "$f"; done
```


## Step-by-step animations

The directory `examples/animations/` contains the first animation layer:

- `01_animate_ah_projection.py`
- `02_animate_orientation_sign_state.py`
- `03_animate_convex_hull_scan.py`
- `04_animate_box_point_location.py`

The scripts generate GIF files in `examples/output/animations/`.
They require `matplotlib` and `pillow`:

```bash
pip install matplotlib pillow
```

Run all animations with:

```bash
for f in examples/animations/0*.py; do python "$f"; done
```


## Interactive GUI examples

The directory `examples/gui/` contains interactive Tk/Matplotlib interfaces:

- `01_gui_ah_projection.py` — AH scenario slider from sure to realized projection;
- `02_gui_orientation_sign.py` — interactive orientation predicate and sign state;
- `03_gui_convex_hull.py` — certified and uncertain hull labels under moving realized points;
- `04_gui_point_location.py` — box-aware point location with a moving query footprint;
- `05_gui_voronoi_nearest.py` — nearest-site certification under two AH projections;
- `launcher.py` — small menu to open the GUI examples.

They require `matplotlib`; Tkinter is included with most standard Python installations.

```bash
pip install matplotlib
python examples/gui/launcher.py
```

You can also run a single GUI directly, for example:

```bash
python examples/gui/02_gui_orientation_sign.py
```
