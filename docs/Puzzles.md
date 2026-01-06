# Lichess puzzles: import + run

This repo supports evaluating the move-selection agent on tactical puzzles **without leaking answers** into the move-selection bundle.

## 1) Download the Lichess puzzle DB (local)
Download the Lichess puzzles CSV from the Lichess database page (it’s large):
- `https://database.lichess.org/#puzzles`

Put it somewhere local, e.g.:
- `puzzles/raw/lichess_db_puzzle.csv` (this path is gitignored)

## 2) Import into public/private sets

```bash
source .venv/bin/activate
python tools/import_lichess_puzzles.py --csv puzzles/raw/lichess_db_puzzle.csv --set lichess_sample --limit 5000
```

Outputs:
- `puzzles/public/lichess_sample.jsonl` (positions + metadata only)
- `puzzles/private/lichess_sample.jsonl` (solutions; gitignored)

## 3) Run a puzzle set with an “external move picker”

The puzzle runner creates a temporary per-puzzle ledger under `games/puzzle_runs/` (gitignored),
generates a sealed selection bundle, runs your command inside it, and scores the **first move** vs the known solution.

Example stub “agent” that always plays `e4`:

```bash
python tools/run_puzzles.py --set lichess_sample --n 50 --external-cmd 'python -c "print(\"e4\")"' --out reports/puzzles_lichess_sample.md
```

In the future, `--external-cmd` becomes your Codex Cloud Task invocation.

## 4) Load a single puzzle into a game ledger (interactive)

If you want to inspect/solve one puzzle as if it were a game state in `games/<game_id>/ledger.md`:

```bash
source .venv/bin/activate
python tools/new_game_from_puzzle.py --set lichess_sample --puzzle-id 00008 --game puzzle_00008
```

Then the move-selection agent (LLM-only) can read `games/puzzle_00008/ledger.md` and attempt a move using `skills/`.

## Why answers aren’t leaked
- The selection bundle only includes `skills/` and the per-puzzle `ledger.md`/`thinklog.md`.
- Solutions are stored in `puzzles/private/` which is gitignored and never copied into the bundle.


