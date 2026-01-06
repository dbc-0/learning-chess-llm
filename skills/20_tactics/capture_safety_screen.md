# Tactics: capture safety screen (SEE-lite)
ID: tactics.capture_safety_screen.v1

## Purpose
Given a candidate **capture** `X x T` (piece from `from` captures on target square `T`), decide if it is a likely blunder:
- “Does this hang my capturing piece to a simple recapture?”
- “Is the exchange obviously unfavorable (e.g., queen for knight)?”

This is the missing step that would have rejected `Qxc2??` when `...Bxc2` wins the queen.

## Inputs
- `games/<game_id>/ledger.md`
- Candidate capture (SAN/UCI) with:
  - capturing piece type/value
  - `from` square
  - target square `T`

## Outputs
- One of:
  - **SAFE_ENOUGH** (no obvious losing recapture found)
  - **DANGEROUS** (explain the recapture and why the exchange is bad)
  - **UNSURE** (if you can’t enumerate defenders/recaptures confidently)

## Required references
- `skills/20_tactics/material_values.md`
- `skills/20_tactics/attackers_defenders_of_square.md`
- `skills/11_geometry/*` (indirectly via the attackers/defenders skill)

## Procedure (bounded)

### 1) Verify the capture itself is geometrically valid
Use `skills/10_movegen/verify_move_claim.md` through:
- destination occupancy
- movement geometry (and between-squares for sliders)
If REFUTED/UNSURE → do not play it.

### 2) Enumerate defenders of `T` (opponent attackers of `T`)
Call `tactics.attackers_defenders_of_square` for target `T`.
Let `Defenders(T)` be the list of opponent pieces that attack `T`.

### 3) Immediate recapture screen (no deep search)
If `Defenders(T)` is empty → **SAFE_ENOUGH** (still watch for tactics).
If not empty:
- Identify the **cheapest defender** (by material value) that can recapture on `T`.
- Compare values:
  - If your capturing piece value is much larger than the captured piece AND the defender can recapture cleanly → **DANGEROUS**.
  - Always treat “queen/rook captured for minor/pawn” as **DANGEROUS** unless you have a forcing tactical justification (mate, winning queen back, etc.).

### 4) One-step SEE-lite (optional, only if needed)
If the capture looks close:
- Consider the line: `XxT` then opponent `YxT` (cheapest recapture).
- If you can recapture `Y` with a cheaper piece and come out ahead, mark **SAFE_ENOUGH**.
- Otherwise **DANGEROUS**.

## Output format
- SAFE_ENOUGH: “Defenders empty OR exchange seems favorable; no obvious recapture wins major piece.”
- DANGEROUS: name the defender and the exchange (e.g., “Q takes N on c2, but ...Bxc2 wins the queen: 9 for 3”).
- UNSURE: specify which lookup/step failed.


