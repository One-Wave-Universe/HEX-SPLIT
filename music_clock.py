#!/usr/bin/env python3
"""E-510 music clock sitting on the hex split.

6 pyramids × 2 (face + flip) = 12 pitch classes.
Opposite pyramids share a midline — the M4 clock axis in this toy.
"""
from __future__ import annotations

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# pyramid i owns NOTES[i] and its tritone NOTES[i+6]
PYRAMIDS = [
    {"id": i + 1, "face": NOTES[i], "flip": NOTES[i + 6], "opposite": ((i + 3) % 6) + 1}
    for i in range(6)
]


def fifths_walk(start: str = "C") -> list[str]:
    idx = NOTES.index(start)
    return [NOTES[(idx + 7 * k) % 12] for k in range(12)]


def main() -> None:
    print("HEX-SPLIT music clock")
    print("pyramid  face  flip  opposite")
    for p in PYRAMIDS:
        print(f"  P{p['id']}     {p['face']:<3}  {p['flip']:<3}  P{p['opposite']}")
    print()
    print("circle of fifths from C:", " ".join(fifths_walk()))
    print()
    print("midline pairs (M4 candidates):")
    seen = set()
    for p in PYRAMIDS:
        pair = tuple(sorted((p["id"], p["opposite"])))
        if pair in seen:
            continue
        seen.add(pair)
        print(f"  P{pair[0]} — P{pair[1]}   {PYRAMIDS[pair[0]-1]['face']}/{PYRAMIDS[pair[0]-1]['flip']} vs {PYRAMIDS[pair[1]-1]['face']}/{PYRAMIDS[pair[1]-1]['flip']}")


if __name__ == "__main__":
    main()
