from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.ledger_io import board_to_new_ledger_text  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create a new game ledger from a puzzle in puzzles/public/<set>.jsonl.")
    p.add_argument("--set", required=True, help="Puzzle set name (puzzles/public/<set>.jsonl)")
    p.add_argument("--puzzle-id", required=True, help="PuzzleId from Lichess puzzle DB (e.g. 00008)")
    p.add_argument("--game", required=True, help="New game id to create under games/<id>/")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    pub_path = Path("puzzles/public") / f"{args.set}.jsonl"
    if not pub_path.exists():
        raise SystemExit(f"ERROR: {pub_path} not found.")

    target = args.puzzle_id
    fen: str | None = None
    for line in pub_path.read_text().splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if str(obj.get("puzzle_id")) == target:
            fen = obj.get("fen")
            break

    if not fen:
        raise SystemExit(f"ERROR: puzzle_id {target!r} not found in {pub_path}")

    board = chess.Board(fen)
    game_dir = Path("games") / args.game
    game_dir.mkdir(parents=True, exist_ok=True)
    (game_dir / "ledger.md").write_text(
        board_to_new_ledger_text(game_id=args.game, board=board, last_updated=str(date.today()))
    )
    (game_dir / "thinklog.md").write_text("# Thinklog (append-only)\n\n---\n")
    print(f"Created games/{args.game}/ledger.md from puzzle {target} ({args.set})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


