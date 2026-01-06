# Orchestrator: play_move
ID: orch.play_move.v1

## Input
- `games/<game_id>/ledger.md`

## Output
- Exactly one move (SAN preferred; UCI acceptable)

## Stop conditions
- Must terminate after producing one move.
- Max 6 candidates.
- Max 6 ply lookahead (except continuing only-checks/only-captures sequences).

## Procedure
1) Read ledger and copy the "STATE" section into the thinklog snapshot.
   - The thinklog entry is the **inspectable decision trace**. If a check is not written down, treat it as not done.
   - **Non-negotiable**: any factual claim in the trace ("square is empty", "this is check", "this is defended", "path is clear") MUST be backed by a lookup/proof using `skills/11_geometry/*` and the ledger piece list. Do not guess.
2) Run opponent last-move impact scan (MUST, before your own move search):
   - Execute `skills/20_tactics/opponent_last_move_impact_scan.md` and write its outputs into the thinklog.
   - This step MUST surface any newly created attacks on your queen/rooks/king (e.g., a “block” move that also attacks your queen).
3) Run forcing scan:
   3.1 Enumerate ALL legal checks available to side to move (explicit list).
   3.2 Enumerate ALL legal captures available to side to move (explicit list).
   For every listed check/capture, include a one-line **geometry proof** referencing `skills/11_geometry/*`:
   - slider ray contains destination + between-squares empty (for bishop/rook/queen)
   - knight destination appears in knight table (for knights)
   - pawn capture destination appears in pawn attack table + destination occupied / EP (for pawns)
   If legality is uncertain for any candidate in 2.x, mark it as "UNSURE" and do not use it unless no alternatives exist.
4) Build candidate set (max 6):
   - Prefer sound forcing moves first (checks/captures).
   - If no forcing advantage, include improving moves: king safety, develop, centralize, improve worst-placed piece, create/stop threats.
   **Candidate admission gate (MUST FOLLOW)**:
   - You may only admit a move into the candidate set if it is marked **VERIFIED** by `skills/10_movegen/verify_move_claim.md`.
   - If `verify_move_claim` returns **REFUTED** or **UNSURE**, the move is NOT allowed in the candidate set.
   - Record the result as a single line per candidate: `VERIFY_MOVE_CLAIM: VERIFIED|REFUTED|UNSURE (reason)`
   Then:
   - For every candidate (capture or not), run `skills/20_tactics/square_safety_screen.md`. If it returns **DANGEROUS**, the move is rejected unless you write an explicit forcing justification (mate / winning queen / etc.).
   - Run `skills/20_tactics/post_move_hanging_major_screen.md` (bounded). If it returns **FAIL**, reject the move unless you write an explicit forcing justification.
   - If the candidate is a **capture**, also run `skills/20_tactics/capture_safety_screen.md`. If it returns **DANGEROUS**, reject the capture unless you write an explicit forcing justification.
5) For each candidate, do a bounded opponent forcing reply scan:
   - List opponent checks and captures in the resulting position (1 ply reply set only).
6) Choose final move:
   - Reject any move that fails blunder screen (drops queen/rook, allows immediate mate, loses decisive material to a forcing reply).
   - Otherwise choose by evaluation rubric (material, king safety, tactics, activity, structure).
7) Append to thinklog (required trace sections in AGENTS.md order).
   - Do not rely on “unstated” reasoning. Put the reasoning you actually used into the trace sections.
   - **Fail closed**: if you cannot produce VERIFIED proofs for key claims, pick a simpler safer move (or mark UNSURE and choose the safest legal move you can verify).
8) Apply the chosen move to ledger:
   - Update piece list, side to move, rights (castling/ep), move history, captured list.
9) Output the move only.