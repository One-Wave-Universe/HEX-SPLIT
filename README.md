# HEX-SPLIT

One hexagon. Cut from the center. Six triangles. Stand them up. Six pyramids.

This is not decoration. In One Wave terms it is D-408 (sixfold 2D lattice) standing up into volume so D-409 (twelvefold 3D) has a doorway.

Sister benches:
- [`GRAV-LAB`](https://github.com/One-Wave-Universe/GRAV-LAB) — magnetism / gravity lock
- [`One-Wave-Science`](https://github.com/One-Wave-Universe/One-Wave-Science) — the node bible
- [`BUCKET-R2`](https://github.com/One-Wave-Universe/BUCKET-R2) — follower of this clock
- [`GCAC`](https://github.com/One-Wave-Universe/GCAC) — ternary polarity bit

## What this repo *does*

1. Builds a regular hexagon in the plane.
2. Splits it into 6 central triangles.
3. Raises each triangle to a pyramid with a shared apex option (one mountain) or six local apices (six tents).
4. Maps the 6 walls onto the 12-tone music clock (E-510): each pyramid owns a tritone pair — a facing and its flip.
5. Walks those 12 slots by fifths (`circle_of_fifths.py` + bench UI).
6. Syncs followers with protocol `one-wave-clock/1` (`SYNC.md`, `clock_sync.py`).
7. Prints numbers you can feed a 3D printer or a Jetson viz later.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python hex_split.py
python music_clock.py
python circle_of_fifths.py
python clock_sync.py
```

Open `circle_of_fifths.html` in a browser. Payload for other benches: `clock.json`.
Wire law: `SYNC.md`.

## Why 6 and 12 and not vibes

- 6 neighbors in the plane (triangular / hex lattice).
- 12 nearest neighbors in 3D close-pack (one center + twelve).
- 12-tone clock is the same count wearing ears.
- Each pyramid is a *choice face*. The midline between opposite pyramids is the M4 clock line.
- Flip a pyramid through the plane and you get the mirror gate, not a new particle.
- Fifths weave *between* pyramids. Tritone stays home and flips polarity.
- Hold freezes phase. Opposed rings quit. Dream does not vote.

Gate status for this repo itself: BROWN→YELLOW scaffolding. Geometry is exact. Physics claim stays parked until a print or a field map shows a 6-fold preference that a square lattice cannot fake.
