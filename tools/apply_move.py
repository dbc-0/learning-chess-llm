from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess

from tools.ledger_io import LedgerError
from tools.referee import apply_move_to_game


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Apply a human/LLM move to a game ledger (legality-checked).")
    p.add_argument("--game", required=True, help="Game id under games/<id>/ledger.md")
    p.add_argument("--move", required=True, help="Move in SAN (preferred) or UCI (e2e4)")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    applied = apply_move_to_game(args.game, args.move)
    print(f"Applied: {applied.san} ({applied.uci})")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (LedgerError, chess.IllegalMoveError, chess.InvalidMoveError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        raise SystemExit(2)


