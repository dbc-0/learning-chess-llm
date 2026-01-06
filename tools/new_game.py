from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.ledger_io import board_to_new_ledger_text  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Create a new game ledger/thinklog from a FEN (default startpos).")
    p.add_argument("--game", required=True, help="Game id to create under games/<id>/")
    p.add_argument("--fen", default="", help="Optional FEN (default = standard start position)")
    p.add_argument("--force", action="store_true", help="Overwrite existing games/<id>/ledger.md and thinklog.md")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    game_dir = Path("games") / args.game
    game_dir.mkdir(parents=True, exist_ok=True)

    ledger_path = game_dir / "ledger.md"
    thinklog_path = game_dir / "thinklog.md"

    if not args.force and (ledger_path.exists() or thinklog_path.exists()):
        raise SystemExit(f"ERROR: {game_dir} already exists. Use --force to overwrite.")

    board = chess.Board(args.fen) if args.fen else chess.Board()
    ledger_path.write_text(board_to_new_ledger_text(game_id=args.game, board=board, last_updated=str(date.today())))
    thinklog_path.write_text(
        "# Thinklog (append-only)\n\n"
        "## Trace policy\n"
        "- This file is the inspectable decision trace for move selection.\n"
        "- Use the required sections from AGENTS.md for each move.\n\n"
        "---\n"
    )

    print(f"Created games/{args.game}/ledger.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


