# Thinklog (append-only)

---

## Move 13 (White) — Attempted move REFUTED (illegal)

### Snapshot
(Position at the moment of the attempted move; from `games/llm_vs_engine_harness_002/ledger.md`)
SIDE_TO_MOVE: White
FEN (from harness): `r1b1k2r/p1q2p1p/2pp2p1/4p3/3QPBn1/2N5/PPP2PPP/R3R1K1 w kq - 0 13`

### Candidate considered
- Attempted: `Qxg4`
- Intended claim: “queen captures the knight on g4”

### Verification (why it failed)
This failed `skills/10_movegen/verify_move_claim.md` at the **movement geometry + between-squares** step:
- Queen source: `d4`
- Target: `g4`
- Geometry requirement (queen rook-like move): `g4` must be on an E/W ray from `d4`.
  - The E ray from `d4` is: `e4 f4 g4 h4`
- Between squares for `d4 -> g4`: `e4`, `f4`
- Occupancy check from the position:
  - `f4` is occupied by a white bishop (`Bf4`)
- Therefore the queen’s path is **blocked** and `Qxg4` is **illegal**.

### Root cause
I attempted a capture without completing the required “ray contains target + between squares empty” proof for a slider move.
