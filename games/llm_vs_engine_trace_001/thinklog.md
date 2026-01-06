# Thinklog (append-only)

## Trace policy
- This file is the inspectable decision trace for move selection.
- Use the required sections from AGENTS.md for each move.

---

## Move 1 (White)

### Snapshot
SIDE_TO_MOVE: White
CASTLING: White=KQ Black=kq
EN_PASSANT: -
HALFMOVE_CLOCK: 0
FULLMOVE_NUMBER: 1

PIECES:
  White: Ke1 Qd1 Ra1 Rh1 Bc1 Bf1 Nb1 Ng1 Pa2 Pb2 Pc2 Pd2 Pe2 Pf2 Pg2 Ph2
  Black: Ke8 Qd8 Ra8 Rh8 Bc8 Bf8 Nb8 Ng8 Pa7 Pb7 Pc7 Pd7 Pe7 Pf7 Pg7 Ph7

### Forcing scan
Checks:
- (none from the starting position)
Captures:
- (none from the starting position)

### Candidate set (max 6)
1) e4: claim space in the center; open lines for bishop/queen.
2) d4: claim space in the center; open lines for bishop/queen.
3) Nf3: develop; control e5/d4.
4) c4: fight for d5; flexible.

### Legality proof (chosen move)
Chosen move: e4
- Piece movement rule satisfied: pawn e2 -> e4 is a two-square push from the starting rank.
- Destination occupancy rule satisfied: e3 and e4 are empty in the starting piece list.
- Path/blockers checked: e3 is empty.
- King safety preserved: moving the e-pawn does not expose own king to immediate check.
- Special rules: sets EN_PASSANT to e3.

### Blunder screen (opponent forcing reply)
Opponent checks: none immediate.
Opponent captures: none immediate.
Worst-case forcing reply considered: none (opening move).

### Evaluation rubric summary
- Material: equal.
- King safety: unchanged.
- Tactics: none immediate.
- Activity: improves by opening lines.
- Structure: central pawn presence.
- Plan: develop pieces, contest the center.

### Final
Chosen move: e4
Explanation: No forcing moves exist, so I prioritize a central pawn push that improves piece activity and control. e4 is a standard, safe way to claim space and open lines.
