# Tactics: post-move hanging major screen (bounded)
ID: tactics.post_move_hanging_major_screen.v1

## Purpose
Catch a very common non-capture blunder:
- “I moved a piece and now my queen/rook is hanging (attacked and not defended).”

This approximates “what control did I give up by leaving my square?” without needing full-board recomputation.

## Inputs
- `games/<game_id>/ledger.md`
- Candidate move (SAN/UCI) and the *resulting* hypothetical position (you must mentally apply the move for this screen).

## Outputs
- **PASS** or **FAIL** or **UNSURE**
  - If FAIL, name the hanging major piece and the opponent attacker(s).

## Required references
- `skills/20_tactics/attackers_defenders_of_square.md`

## Procedure (bounded)
1) In the resulting position, identify your major pieces:
   - your queen square (if present)
   - your rook squares (0–2)
2) For each such square `S`:
   - call `attackers_defenders_of_square` with `T = S`
   - if opponent attacks `S` and your defenders of `S` are zero → mark **FAIL**
3) If you cannot confidently apply the move to get the resulting piece placement, return **UNSURE**.

## Notes
- This is intentionally narrow (queen/rooks only) to keep it cheap.
- It complements `square_safety_screen` (which focuses on the moved piece’s destination square).


