# Tactics: attackers & defenders of a square (lookup-based)
ID: tactics.attackers_defenders_of_square.v1

## Purpose
Given a target square `T` and a ledger state, list:
- **attackers** of `T` for White
- **attackers** of `T` for Black

This is used to avoid tactical blunders like capturing a piece on `T` with a high-value piece when `T` is defended.

## Inputs
- `games/<game_id>/ledger.md` (PIECES list is required)
- Target square `T` (e.g. `c2`)

## Output
- `White attacks T`: explicit list of piece tokens that attack `T`
- `Black attacks T`: explicit list of piece tokens that attack `T`
- For each listed attacker, include a **micro-proof** referencing geometry tables:
  - knight: `knight_moves_table.md` entry contains `T`
  - pawn: `pawn_attacks.md` entry contains `T`
  - king: `king_moves_table.md` entry contains `T`
  - slider: in `rays.md`, `T` appears on a ray from the piece square AND all between-squares are empty in the ledger

## Required references
- `skills/11_geometry/rays.md`
- `skills/11_geometry/between_squares.md`
- `skills/11_geometry/knight_moves_table.md`
- `skills/11_geometry/king_moves_table.md`
- `skills/11_geometry/pawn_attacks.md`

## Procedure (bounded)
1) Extract occupied squares from the ledger piece list (both sides).
2) For each piece token on the board, test whether it attacks `T`:
   - **Knight**: lookup its square in `knight_moves_table.md`.
   - **Bishop/Rook/Queen**:
     - lookup its square in `rays.md`.
     - find if `T` is on the correct ray.
     - list between-squares (ray prefix before `T`) and verify each is empty.
   - **Pawn**: lookup its square in `pawn_attacks.md` for the correct color.
   - **King**: lookup its square in `king_moves_table.md`.
3) Output the two attacker lists with proofs.

## Non-negotiable rule
- You MUST NOT list a piece as an attacker unless you can provide the micro-proof (ray + empty between squares, or table membership).
- If you cannot complete the proof, omit the attacker and mark the result **INCOMPLETE**.

## Notes / pitfalls
- This is about **attack geometry**, not whether moving that piece is legal (pins, leaving king in check).
- Still extremely useful for “is this capture safe?” checks.


