# Opponent last-move impact scan (MUST, geometry-backed)

## Goal
Before you generate your own candidates, explicitly account for what the opponent’s *most recent move* changed:
- which of **your** pieces are now attacked (newly attacked vs previously attacked)
- whether you are in **check**
- what the opponent’s **forcing threats** are next ply (checks/captures only; bounded)
- what lines were **opened/closed** (discovered attacks, pins, skewers) — using geometry proofs

This prevents missing “quiet” tactical facts like *a block move that simultaneously attacks your queen*.

## Inputs
- The current `games/<id>/ledger.md` (single source of truth)
- The opponent’s last move from the ledger move history (if available)
- Geometry tables: `skills/11_geometry/*`

## Output (write into thinklog)
Provide these sections (short but explicit):

1) `OPP_LAST_MOVE: <...>`
2) `CHECK_STATUS: IN_CHECK | NOT_IN_CHECK` (with proof if in check)
3) `OUR_PIECES_UNDER_ATTACK:` list each attacked piece token + attacker token(s) + one-line micro-proof each
4) `OPP_FORCING_THREATS_NEXT:` (max 10 lines)
   - `Checks:` enumerate all opponent checks (explicitly)
   - `Captures:` enumerate all opponent captures (explicitly)
   Each item needs a geometry-backed proof (ray + empties, or table membership).
5) `LINES_OPENED_OR_CLOSED:` (max 6 lines)
   - “Opened: Bd7 now attacks a4 along d7-c6-b5-a4 (between squares empty)”
   - “Closed: ...”

## Procedure (bounded, must be geometry-backed)
0) If there is no opponent last move (start position), write `OPP_LAST_MOVE: none` and continue with (2)–(4) anyway using current board.

1) Identify opponent last move `M` from move history.

2) Determine whether you are in check **now**.
- Locate your king square `K` from the ledger piece list.
- Enumerate opponent pieces that attack `K` using geometry:
  - knights/kings/pawns via tables
  - sliders via rays + between-squares emptiness
- If any verified attacker exists, output `CHECK_STATUS: IN_CHECK` and list the attacker(s) with proof; otherwise `NOT_IN_CHECK`.

3) Enumerate your pieces under attack **now** (minimum: queen + rooks; recommended: all pieces).
- For each of your piece tokens `P@S`:
  - call the logic in `skills/20_tactics/attackers_defenders_of_square.md` conceptually for square `S`
  - list opponent attackers only if you can provide micro-proofs
- Mark anything you could not fully prove as `INCOMPLETE` (do not guess).

4) Enumerate opponent forcing threats next ply (checks/captures only; bounded).
- `Checks`: find all verified checks opponent can give on their next move (same method as above but from current position, 1 ply).
- `Captures`: find all verified captures opponent can make next (list capture moves that are geometrically possible and whose destination is occupied by your piece token).

5) Identify “lines opened/closed” by last move.
- Compare “before/after” conceptually by focusing on the moved piece and the squares it now attacks.
- At minimum:
  - list **new squares attacked by the moved piece** that matter tactically (king, queen, rooks, pinned pieces).
  - list any **discovered** ray now opened to your king/queen/rook (e.g., a pawn moved revealing a bishop/queen diagonal).
- Every line claim must be backed by ray + between-squares emptiness from the current ledger.

## Non-negotiable rules
- You MUST NOT start your candidate move selection until this scan is completed in the thinklog.
- Every “attacked/threat/check” item MUST have a geometry-backed proof. If you can’t prove it, label it `INCOMPLETE` and do not rely on it.
- Keep it bounded: threats are limited to **checks and captures only** (forcing).


