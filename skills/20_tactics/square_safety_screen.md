# Tactics: square safety screen (for any move)
ID: tactics.square_safety_screen.v1

## Purpose
For a candidate move `from -> to` (capture or non-capture), screen for the most common “quiet-move blunders”:
- moving a high-value piece onto a square controlled by the opponent
- moving the king into check

This is intentionally simpler than a full tactical search. It is a fast, bounded *sanity check*.

## Inputs
- `games/<game_id>/ledger.md`
- Candidate move with:
  - piece type (P/N/B/R/Q/K) and color
  - `from` square
  - `to` square

## Outputs
- **SAFE_ENOUGH** or **DANGEROUS** or **UNSURE**
  - include a short justification based on attacker/defender counts

## Required references
- `skills/20_tactics/attackers_defenders_of_square.md`
- `skills/20_tactics/material_values.md`
- (indirectly) `skills/11_geometry/*`

## Procedure

### 1) Basic legality precheck
Run `skills/10_movegen/verify_move_claim.md` through:
- destination occupancy
- movement geometry (including between-squares for sliders)
If REFUTED/UNSURE → return **DANGEROUS/UNSURE** (do not play).

**Non-negotiable**: this screen cannot override a REFUTED/UNSURE legality result.

### 2) Compute control of destination square `to`
Call `tactics.attackers_defenders_of_square` with `T = to`.
Let:
- `A_opp = number of opponent attackers of to`
- `D_us  = number of our defenders of to`

### 3) Decide safety (bounded heuristics)
- If the moved piece is the **king**:
  - If `A_opp > 0` → **DANGEROUS** (king cannot move into check).
  - Else **SAFE_ENOUGH**.

- If the moved piece is **queen or rook**:
  - If `A_opp > 0` and `D_us == 0` → **DANGEROUS** (en prise major piece).
  - If `A_opp > D_us` and there is no forcing tactical justification (mate / winning queen / etc.) → **DANGEROUS**.
  - Else **SAFE_ENOUGH**.

- If the moved piece is **minor (bishop/knight)**:
  - If `A_opp > 0` and `D_us == 0` and the move is not a deliberate sacrifice → **DANGEROUS**.
  - Else **SAFE_ENOUGH**.

- If the moved piece is a **pawn**:
  - Usually OK even if attacked; still flag **DANGEROUS** if it obviously drops a pawn for nothing and creates immediate threats against your king (use your judgement).

### 4) Output
Include:
- attacker list summary (who attacks `to`)
- defender list summary (who defends `to`)
- the heuristic rule that triggered SAFE/DANGEROUS

## Notes
- This is about **square control**, not full exchange calculation.
- Captures should additionally use `tactics.capture_safety_screen.md` (exchange/recapture logic).


