# Modes of play (human, LLM, engine)

This repo supports three practical modes. The key distinction is whether we are in:
- **LLM-only move selection** (skills + ledger + thinklog only), or
- **harness/referee mode** (python-chess + optional engine) used to enforce legality, apply moves to the ledger, and optionally generate an opponent move / score.

## Mode A: Human vs LLM (chat mode)
- **Primary use**: normal play in this chat interface.
- **Engine use**: **never**.
- **Harness use**: optional.

How it works:
- The human types a move in chat.
- The LLM responds with exactly one move and updates:
  - `games/<game_id>/ledger.md` (state only)
  - `games/<game_id>/thinklog.md` (append-only trace)

Optional strictness:
- If you want strict legality checking for the **human’s** move and a guaranteed-correct ledger update, you can apply the human move with:
  - `python tools/apply_move.py --game <game_id> --move "<SAN-or-UCI>"`

## Mode B: LLM vs Engine (training / evaluation)
- **Primary use**: automated play to measure improvement and generate learning signals.
- **Engine use**: **harness only**, never during LLM move selection.
- **Harness use**: required.

How it works (alternating loop):
1) LLM picks a move using only:
   - `skills/`
   - `games/<game_id>/ledger.md` (+ thinklog)
   - repo text search
2) Harness applies that move to the canonical ledger (legality-checked).
3) Harness asks the engine for the opponent move and applies it.

Implementation note:
- Today this is represented by `tools/run_match.py` with the LLM side configured as **`external`** (a command that prints one move to stdout from a sealed selection bundle). In the future this external command can be a Codex Cloud Task.

## Mode B2: LLM vs Engine (with post-hoc blunder detection)
If you want an automated loop that **stops on the first blunder** and produces a markdown report:
- `tools/run_llm_vs_engine_review.py`

This:
- runs the LLM move via `--external-cmd` inside a sealed selection bundle
- applies it (legality-checked)
- evaluates the position before/after with the engine (post-hoc)
- stops when eval drop crosses a threshold
and writes `games/<game_id>/engine_private/review.md` (gitignored).

## Mode C: Human vs Engine (harness smoke test / debugging)
- **Primary use**: validate the harness pipeline and engine config end-to-end.
- **Engine use**: yes (harness).
- **Harness use**: required.

Why it exists:
- Confirms your UCI config + legality checking + ledger updates are correct before plugging in the LLM.
- Useful for reproducing positions and debugging: “engine played X, now what?”

## Commands (quick reference)
- **Apply a move** (SAN or UCI) to the ledger:
  - `python tools/apply_move.py --game demo --move "e4"`
- **Have the engine play one move** for side to move:
  - `python tools/engine_move.py --game demo`
- **Run a match loop** (human/engine/external):
  - `python tools/run_match.py --game demo --white human --black engine`
  - `python tools/run_match.py --game demo --white external --black engine --external-cmd 'python -c "print(\\"e4\\")"'`


