#!/usr/bin/env python3
"""Three-winding nerve cell — kickable model.

Not SPICE. The law in numbers:
  BC-DC  engage
  TC-AC  lean on three windings around G
  QC-RC  views up / action down as one flip
State of the windings IS the memory. Bidirectional at center. Not linear.

Run: python nerve_cell.py
"""
from __future__ import annotations

from dataclasses import dataclass, field

BELT = 0.05
TAU = 0.15
DT = 0.05
DECAY = 0.08


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


@dataclass
class Receipt:
    seq: int
    engage: int
    live_gate: int
    lean: float
    i_g: float
    g: float
    windings: tuple
    ternary: int
    stamp: str
    views: tuple
    action: tuple


@dataclass
class NerveCell:
    """One hexagon of body: 3 mirrored gates / 3 windings / 1 mid."""

    g: float = 0.0
    w: list = field(default_factory=lambda: [0.0, 0.0, 0.0])
    engage: int = 0
    live: int = 0
    seq: int = 0
    last_w: list = field(default_factory=lambda: [0.0, 0.0, 0.0])

    def i_g(self) -> float:
        return sum(self.w)

    def ternary(self) -> int:
        x = self.i_g()
        if abs(x) < BELT:
            return 0
        return 1 if x > 0 else -1

    def stamp_of(self) -> str:
        if self.engage == 0:
            return "hold"
        t = self.ternary()
        return "hold" if t == 0 else "commit"

    def tick(self, engage: int, live: int, lean: float) -> Receipt:
        """One crossing. New views up and last action down — same seq."""
        self.engage = 1 if engage else 0
        self.live = int(live) % 3
        lean = clamp(float(lean), -1.0, 1.0)

        prev = list(self.w)
        if self.engage == 0 or abs(lean) < BELT:
            for i in range(3):
                self.w[i] *= 1.0 - DECAY
            self.g += DT * (-self.g / TAU)
        else:
            drive = [0.0, 0.0, 0.0]
            drive[self.live] = lean
            drive[(self.live + 1) % 3] = -0.5 * lean
            drive[(self.live + 2) % 3] = -0.5 * lean
            for i in range(3):
                self.w[i] += DT * (drive[i] - self.w[i]) / TAU
            self.g += DT * (self.i_g() - self.g) / TAU

        action = tuple(self.w[i] - prev[i] for i in range(3))
        views = tuple(self.w)
        self.last_w = list(self.w)
        self.seq += 1
        st = self.stamp_of()
        return Receipt(
            seq=self.seq,
            engage=self.engage,
            live_gate=self.live,
            lean=lean,
            i_g=self.i_g(),
            g=self.g,
            windings=views,
            ternary=self.ternary() if st == "commit" else 0,
            stamp=st,
            views=views,
            action=action,
        )


def demo() -> None:
    cell = NerveCell()
    print("NERVE CELL  3 windings  mid=vagus  process=memory")
    print(f"{'seq':>4} {'eng':>3} {'g':>2} {'lean':>6} {'I_G':>7} {'tern':>5} {'stamp':<7} {'w0':>7} {'w1':>7} {'w2':>7}")

    def show(r: Receipt) -> None:
        print(
            f"{r.seq:4d} {r.engage:3d} {r.live_gate:2d} {r.lean:6.2f} {r.i_g:7.3f} "
            f"{r.ternary:5d} {r.stamp:<7} {r.views[0]:7.3f} {r.views[1]:7.3f} {r.views[2]:7.3f}"
        )
        return r

    rest = show(cell.tick(0, 0, 0.0))
    assert rest.stamp == "hold" and rest.ternary == 0
    assert abs(rest.i_g) < BELT

    right = show(cell.tick(1, 0, 0.8))
    assert right.stamp == "commit" and right.ternary == 1
    assert right.seq == rest.seq + 1
    assert abs(sum(right.action) - (sum(right.views) - sum(rest.views))) < 1e-9

    hold = show(cell.tick(1, 0, 0.0))
    assert hold.stamp == "hold"
    assert hold.views != (0.0, 0.0, 0.0)

    left = show(cell.tick(1, 1, -0.8))
    assert left.ternary == -1
    assert left.live_gate == 1

    quiet = show(cell.tick(0, 1, 0.0))
    assert quiet.stamp == "hold"

    print()
    print("memory after lean-then-hold:", tuple(round(x, 3) for x in hold.views))
    print("vagus I_G hold", round(hold.i_g, 3), "g", round(hold.g, 3))
    print("law: process is memory. flip = views up + action down. mid home.")
    print("hold: 1(0)1")


if __name__ == "__main__":
    demo()
