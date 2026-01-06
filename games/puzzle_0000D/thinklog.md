# Thinklog (append-only)

---

## Move 27 (White)

### Snapshot
SIDE_TO_MOVE: White
CASTLING: White=- Black=-
EN_PASSANT: -
HALFMOVE_CLOCK: 2
FULLMOVE_NUMBER: 27

PIECES:
  White: Kg1 Qd3 Rd1 Nf3 Pa2 Pf2 Pg2 Ph2 Pb3
  Black: Kg8 Qb6 Rf8 Bf6 Pa6 Pb7 Pf7 Pg7 Ph7

### Forcing scan
Checks:
- 27.Qxh7+ (queen d3->h7 captures pawn and gives check)
Captures:
- 27.Qxh7+ (as above)

### Candidate set (max 6)
1) 27.Qxh7+: forcing check, but likely sacrifices the queen if ...Kxh7 is legal.
2) 27.Qd7: improve queen activity; pressure f7/b7; aim for Qxf7+ ideas.
3) 27.Qd6: offer queen trade / activate; keep pressure on kingside.
4) 27.Ng5: improve knight toward checks on f7/h7 (no immediate check).

### Legality proof (chosen move)
Chosen move: 27.Qd7
- Piece movement rule satisfied: queen moves from d3 to d7 along the d-file.
- Destination occupancy rule satisfied: d7 is empty.
- Path/blockers checked (if slider): d4, d5, d6 are empty per piece list.
- King safety preserved (own king not left in check): moving the queen off d3 does not expose Kg1 to a new immediate line attack (f2 pawn blocks the b6->g1 diagonal).
- Special rules (castling/ep/promo if applicable): none.

### Blunder screen (opponent forcing reply)
Opponent checks (after 27.Qd7):
- 27...Qxf2+ (queen b6->f2 captures pawn on f2 and gives check on Kg1)
Opponent captures (after 27.Qd7):
- 27...Qxf2+ (as above)
Worst-case forcing reply considered: 27...Qxf2+; note Kg1 can likely capture back (Kxf2) if the square is safe.

### Evaluation rubric summary
- Material: roughly even; goal is to convert activity into a concrete advantage.
- King safety: white king is relatively safe behind pawns; avoid allowing a sudden queen check with decisive follow-up.
- Tactics: no obvious immediate win found without deeper calculation; avoid unsound queen sacrifice on h7.
- Activity: Qd7 activates the queen to the 7th rank and hits f7/b7 while coordinating with Rd1.
- Structure: secondary.
- Plan: increase pressure and look for a tactical break like Qxf7+ if it becomes available safely.

### Final
Chosen move: Qd7
Explanation: I saw only one immediate check (Qxh7+) but it looked like a likely queen sacrifice with unclear compensation. Qd7 is a “forceful improving” move that increases pressure on f7 and b7 and keeps threats alive while staying safe against Black’s only obvious forcing reply (…Qxf2+).
