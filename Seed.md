# Seed context for agent runs

## Objective
Pick the best move from a given position using only repo skills + ledger, and log an inspectable trace.

## Non-negotiable constraints
- No engines, no chess libraries, no legality generators.
- Allowed: read/write repo + grep.

## Output requirement
Return exactly one move (SAN preferred, UCI acceptable). No follow-up questions.

## Required procedure per move
1) Snapshot: restate state from ledger
2) Forcing scan: ALL checks, then ALL captures
3) Candidate set: up to 6 moves
4) For chosen move: legality proof checklist
5) Blunder screen: opponent best forcing reply (bounded)
6) Rubric: short structured evaluation
7) Log trace to thinklog; apply move to ledger; output the move

## Fallback rule
If uncertain, prefer:
- king safety
- not hanging major pieces
- simplifying when ahead
- forcing moves when sound