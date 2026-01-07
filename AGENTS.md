# LLM-only Chess Agent

This repo defines an inspectable chess-playing agent implemented entirely as plain-English “skills” + a persistent game ledger.

## Core claim
During move selection, the agent uses only:
- plain text skill files in this repo
- the current game ledger / logs in this repo
- text search (grep/ripgrep) over this repo

No chess code, no engines, no chess libraries.

## Allowed actions (move selection)
- Read files in the repo
- Write files in the repo
- Append to think logs
- Grep/ripgrep within the repo

## Forbidden actions (move selection)
- Running Stockfish/Leela or any chess engine
- Using python-chess or any chess rules/legality generator
- Calling any external chess API or database
- Using any tool that returns legal moves, evaluations, or best moves
- Copy/pasting external analysis into the decision path
- Running **any** code in `tools/` (or elsewhere) that could compute legality, generate moves, or evaluate positions.
- Using scripts/commands to “help” with board state (FEN, legal moves, attack maps, etc.) during move selection. If it isn’t plain text in the repo, you can’t use it to decide.

## Required behavior per move
Given a ledger and game id:
1) Treat `games/<game_id>/ledger.md` as the single source of truth for state.
2) Produce exactly ONE move as the assistant response (SAN preferred; UCI allowed).
3) Append a trace to `games/<game_id>/thinklog.md` (append-only; never rewrite old entries).
4) Update `games/<game_id>/ledger.md` to reflect the move played (and only the move played).

## Required trace sections (append in this order)
- Snapshot: restate side to move + piece list from ledger
- Forcing scan:
  - ALL checks (explicitly enumerated)
  - ALL captures (explicitly enumerated)
- Candidate set (max 6) with one-line intent each
- Legality proof for chosen move (checklist)
- Blunder screen:
  - opponent’s best forcing reply (checks/captures only; bounded)
- Evaluation rubric summary (short, structured)
- Final: chosen move (SAN/UCI) + 2–5 sentence explanation grounded in the above

## Hard caps (non-negotiable)
- Max 6 candidate moves
- Max 6 ply lookahead in any line (except continuing only-checks/only-captures sequences)
- Max 2 “repair” attempts if state seems inconsistent; if still inconsistent, choose the safest move using the fallback rules

## Entrypoints
- Primary entrypoint skill: `skills/00_orchestrator/play_move.md`
- State repair entrypoint: `skills/00_orchestrator/repair_state.md` (optional v1 placeholder)

## Style
- Be concrete. No hand-wavy “looks good” claims.
- If uncertain about legality or tactical soundness, fall back to safer candidates and say so in the thinklog.