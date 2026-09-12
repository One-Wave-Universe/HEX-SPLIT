# Clock sync protocols

Owner bench: HEX-SPLIT. M4 picks the hallway. This file is the wire.

Not NTP. Not close enough. A follower is in sync when it can name the same
`(phase, m4_pair, lap)` the coordinator just committed, or it is in **hold**.

## Roles

| role | who | may |
|---|---|---|
| coordinator | M4 (CPU / Gate-7) | freeze `m4_pair`, commit a tick, issue quit |
| proposer | Field / NPU / BUCKET eye | offer polarity `-1/0/+1` |
| follower | BUCKET-R2, GRAV-LAB sim, a second six-gate | copy committed phase or hold |
| dream | GPU | simulate; **no vote** |

Field/Void is site identity. Polarity is walk direction. Do not swap them.

## The three hallways

Opposite pyramids. Pick **one**. Do not blur.

```
pair 0: P1 — P4
pair 1: P2 — P5
pair 2: P3 — P6
```

(`music_clock.py` numbers pyramids 1..6. GRAV-LAB M4_WALK used 0..5. Same three
lines. This protocol uses 1-based ids so HEX-SPLIT receipts stay readable.)

Changing `m4_pair` mid-lap without Gate-7 commit is a protocol fault.

## Generators

| name | step mod 12 | meaning |
|---|---|---|
| hold | 0 | polarity 0. phase frozen |
| chromatic | +1 | neighbor slot. diagnostic only |
| fourth | +5 | reverse weave |
| tritone | +6 | same pyramid, Express ↔ Compress |
| fifth | +7 | weave between pyramids (default bar clock) |

Default shared generator for BUCKET bars: **+7**. Chromatic is the falsifier walk.

## One tick

```
if polarity == 0 or hold:
    phase stays
else:
    phase' = (phase + polarity * generator) mod 12
```

A 12-walk is one lap. A 24-walk is two laps = 4π sheet (`q` vs `-q`).
`lap` is `0` or `1`. Dropping the sheet is a protocol fault.

## Packet

JSON. One object per committed tick or hold. `proto`: `one-wave-clock/1`.

Fields: `src`, `seq`, `phase`, `polarity`, `generator`, `m4_pair`, `lap`, `hold`, `gate7`, `tonic`, `slot`.

`gate7` ∈ `propose` | `commit` | `hold` | `quit`.

Only `commit` moves a follower’s phase. `propose` is gossip. `quit` forces polarity 0 on every ring that hears it.

## Sync states (follower)

LISTEN, LOCK, HOLD, DRIFT, QUIT.

Lock rule: predicted phase from last commit using the committed generator equals the new packet phase, and `m4_pair` is unchanged.

Drift rule: do **not** chromatic-slew toward the coordinator. Hold, or snap on the next `commit` after a `hold`. Slew-by-1 pretends the fifths generator is optional.

## Dual six-gate

Two rings, one M4. Opposite polarity at full drive → Gate-7 `quit`.
NPU may propose. CPU commits. GPU does not vote.

## Hold law (same belt as GCAC)

- `|drive| < dead` → polarity 0, `gate7=hold`
- opposed rings → `quit` even if drive is large
- M4 may route a proposal. M4 may not override quit.

`1(0)1` is the written hold.

## Falsify this protocol

- Phase advances on polarity 0 or `hold=true`.
- `m4_pair` changes without `gate7=commit`.
- Follower slews chromatically to catch a fifths coordinator.
- Mirror implemented as swapping Field/Void.
- 2π and 4π land on the same `lap` bit.
- GPU / dream packet accepted as `commit`.

## Benches

- HEX-SPLIT owns `clock.json` + this protocol + `clock_sync.py`.
- BUCKET-R2 follows: one slot per earned bar. No speak on hold.
- GCAC supplies the ternary polarity bit.
- GRAV-LAB `M4_WALK.md` is the hallway essay this wire implements.
