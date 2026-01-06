from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.referee import load_board_from_game  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Display a game position from ledger.md as ASCII / Unicode, optionally write SVG.")
    p.add_argument("--game", required=True, help="Game id under games/<id>/ledger.md")
    p.add_argument("--unicode", action="store_true", help="Use Unicode chess piece symbols")
    p.add_argument("--svg", default="", help="Optional path to write an SVG board image")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    board, _ = load_board_from_game(args.game)

    print(f"Game: {args.game}")
    print(f"FEN: {board.fen()}")
    print(f"Turn: {'White' if board.turn else 'Black'}")
    print("")

    if args.unicode:
        # Ranks 8..1 with files a..h (white perspective)
        print(board.unicode(empty_square="·"))
    else:
        # python-chess string is 8..1
        print(str(board))

    if args.svg:
        try:
            import chess.svg  # type: ignore
        except Exception as e:
            raise SystemExit(f"ERROR: SVG support unavailable: {e}")
        svg_text = chess.svg.board(board=board)
        out = Path(args.svg)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(svg_text, encoding="utf-8")
        print("")
        print(f"Wrote SVG: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


