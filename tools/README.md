# Tools (referee / harness)

These scripts are **not** used during LLM move selection. They exist to:
- apply a human/LLM move to the ledger with legality checking
- optionally generate an opponent move from a local UCI engine (Stockfish or lc0)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure an engine (optional)
- Copy `config/engine.example.json` → `config/engine.json`
- Set `"path"` to your local engine binary (Stockfish or lc0)

`config/engine.json` is ignored by git so you can delete it to force **human-only** play.

## Apply a human/LLM move (no engine required)

```bash
python tools/apply_move.py --game demo --move "e4"
```

Move can be **SAN** (`"Nf3"`, `"O-O"`, `"exd5"`) or **UCI** (`"e2e4"`, `"g1f3"`).

## Let the engine play the side to move

```bash
python tools/engine_move.py --game demo
```

This reads `games/demo/ledger.md`, asks the engine for one move, applies it, and writes the updated ledger.

## Run a match loop (human/engine/external)

Examples:

```bash
# Human (White) vs Engine (Black)
python tools/run_match.py --game demo --white human --black engine
```

```bash
# "External" (White) vs Engine (Black) where external prints a move to stdout
python tools/run_match.py --game demo --white external --black engine --external-cmd 'python -c "print(\"e4\")"'
```

In the future, `--external-cmd` is where a Codex Cloud Task (or any remote agent runner) can be invoked.

## Show the board (ASCII / Unicode / SVG)

```bash
source .venv/bin/activate
python tools/show_board.py --game human_vs_stockfish_001
```

Unicode pieces:

```bash
python tools/show_board.py --game human_vs_stockfish_001 --unicode
```

Write an SVG you can open in a browser:

```bash
python tools/show_board.py --game human_vs_stockfish_001 --svg reports/board.svg
```

## Codex Remote / cloud runners: sealed selection bundle

If you want to run an automated loop where a remote agent chooses moves but **must not** see engine outputs or puzzle answers, create a “selection bundle” directory containing only allowed files:

```bash
python tools/make_selection_bundle.py --game demo --out /tmp/selection_bundle
```

In a remote setup, point the agent’s workspace root at `/tmp/selection_bundle` for move selection, while the harness (engine + python-chess) runs outside that bundle.

## LLM vs Engine with post-hoc blunder stop (review mode)

This mode runs an external move-picker (future Codex task) vs the engine, and after each LLM move:
- checks legality (when applying)
- runs engine analysis post-hoc
- stops on the first blunder (eval drop threshold)

```bash
source .venv/bin/activate
python tools/run_llm_vs_engine_review.py \
  --game review_game_001 \
  --reset \
  --llm-side white \
  --external-cmd 'python -c "print(\"e4\")"' \
  --analysis-depth 10 \
  --blunder-threshold -2.0 \
  --max-plies 40
```

Report is written to `games/<game_id>/engine_private/review.md` (gitignored).

### Capturing LLM reasoning traces (thinklog sync)
If your external move-picker appends a per-move trace to `games/<game_id>/thinklog.md` **inside the selection bundle**,
you can ask the harness to copy that appended content back into the canonical game thinklog:

```bash
python tools/run_llm_vs_engine_review.py \
  --game review_game_001 \
  --reset \
  --llm-side white \
  --external-cmd '<your-codex-task-command>' \
  --sync-thinklog
```

Notes:
- This does **not** expose engine output to the move-selection bundle.
- Engine analysis should stay in `games/<game_id>/engine_private/` (ignored).


