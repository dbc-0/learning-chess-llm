# Thinklog (append-only)

---

## Move 28 (Black)

### Snapshot
SIDE_TO_MOVE: Black
CASTLING: White=- Black=-
EN_PASSANT: -
HALFMOVE_CLOCK: 0
FULLMOVE_NUMBER: 28

PIECES:
  White: Kh1 Qg8 Rd1 Rf1 Bc3 Ne6 Pa2 Pb2 Pg2 Ph2
  Black: Kh8 Qc4 Re4 Ng4 Pb5 Pa7 Pc7 Pg7 Ph7

Board (unicode, 8→1):
· · · · · · ♕ ♚
♟ · ♟ · · · ♟ ♟
· · · · ♘ · · ·
· ♟ · · · · · ·
· · ♛ · ♜ · ♞ ·
· · ♗ · · · · ·
♙ ♙ · · · · ♙ ♙
· · · ♖ · ♖ · ♔

### Forcing scan
Checks:
- (none; Black is currently in check)
Captures:
- 28...Kxg8 (king captures the checking queen on g8)

### Candidate set (max 6)
1) 28...Kxg8: forced response to being in check; captures attacker and exits check.

### Legality proof (chosen move)
Chosen move: 28...Kxg8
- Piece movement rule satisfied: king moves one square from h8 to g8.
- Destination occupancy rule satisfied: g8 is occupied by an enemy piece (White queen), capture is allowed.
- Path/blockers checked (if slider): not applicable (king).
- King safety preserved (own king not left in check): g8 is not attacked by any listed white piece (bishop c3 attacks h8 via diagonal, knight e6 attacks f8/g7/d8 etc., rooks d1/f1 do not attack g8, pawns do not attack g8).
- Special rules (castling/ep/promo if applicable): none.

### Blunder screen (opponent forcing reply)
Opponent checks (after 28...Kxg8):
- none obvious from piece list (white queen is gone)
Opponent captures (after 28...Kxg8):
- none forcing and immediate that obviously win major material (white pieces are far)
Worst-case forcing reply considered: White tries to win the black queen/rook with a check or tactic; none immediate spotted.

### Evaluation rubric summary
- Material: capturing the queen is decisive.
- King safety: immediate priority is to get out of check; capture does so.
- Tactics: forced; no alternative legal-looking defenses exist (no blocks possible; king has no other squares).
- Activity/structure: irrelevant compared to winning the queen.
- Plan: after winning queen, simplify safely.

### Final
Chosen move: Kxg8
Explanation: Black is in check from the queen on g8, and because the check is adjacent there is no blocking option. Capturing the checking queen with the king both resolves the check and wins decisive material, and the capture square g8 is not defended by any listed white piece.
