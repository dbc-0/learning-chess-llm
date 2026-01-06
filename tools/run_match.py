from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.ledger_io import LedgerError  # noqa: E402
from tools.make_selection_bundle import main as _make_bundle_main  # noqa: E402
from tools.referee import apply_engine_move_to_game, apply_move_to_game, load_board_from_game  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Run a local match loop, alternating sides, applying each move to games/<id>/ledger.md.\n"
            "Sides can be: human | engine | external\n"
            "external = run a command inside a sealed selection bundle and read the move from stdout."
        )
    )
    p.add_argument("--game", required=True, help="Game id under games/<id>/ledger.md")
    p.add_argument("--white", choices=["human", "engine", "external"], default="human")
    p.add_argument("--black", choices=["human", "engine", "external"], default="engine")
    p.add_argument("--engine-config", default="config/engine.json", help="Engine config path for engine sides")
    p.add_argument(
        "--external-cmd",
        default=None,
        help=(
            "Command to run for an 'external' side. It will be run with CWD set to the selection bundle.\n"
            "It must print exactly one move (SAN or UCI) to stdout.\n"
            "Example: --external-cmd 'python -c \"print(\\\"e4\\\")\"'"
        ),
    )
    p.add_argument("--max-plies", type=int, default=60, help="Stop after N half-moves (plies)")
    return p.parse_args()


def _make_selection_bundle(game_id: str, out_dir: Path) -> None:
    # Reuse the script implementation by calling it as a module entry.
    argv0 = sys.argv[:]
    try:
        sys.argv = ["make_selection_bundle.py", "--game", game_id, "--out", str(out_dir)]
        _make_bundle_main()
    finally:
        sys.argv = argv0


def _external_pick_move(game_id: str, cmd: str) -> str:
    with tempfile.TemporaryDirectory(prefix="selection_bundle_") as tmp:
        bundle_dir = Path(tmp) / "bundle"
        _make_selection_bundle(game_id, bundle_dir)

        proc = subprocess.run(
            shlex.split(cmd),
            cwd=str(bundle_dir),
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                "External move command failed.\n"
                f"cmd: {cmd}\n"
                f"cwd: {bundle_dir}\n"
                f"stdout:\n{proc.stdout}\n"
                f"stderr:\n{proc.stderr}\n"
            )
        move = (proc.stdout or "").strip().splitlines()[0].strip() if proc.stdout.strip() else ""
        if not move:
            raise RuntimeError(f"External move command produced no stdout move. cmd={cmd!r}")
        return move


def _side_kind(turn: chess.Color, white: str, black: str) -> str:
    return white if turn == chess.WHITE else black


def main() -> int:
    args = _parse_args()

    if (args.white == "external" or args.black == "external") and not args.external_cmd:
        raise SystemExit("ERROR: --external-cmd is required when using an external side.")

    for ply in range(1, args.max_plies + 1):
        board, _ = load_board_from_game(args.game)
        side = _side_kind(board.turn, args.white, args.black)
        to_move = "White" if board.turn else "Black"
        print(f"\nPly {ply}: {to_move} to move | FEN: {board.fen()}")

        if board.is_game_over(claim_draw=True):
            print(f"Game over: {board.result(claim_draw=True)}")
            return 0

        if side == "engine":
            applied = apply_engine_move_to_game(args.game, config_path=args.engine_config)
            print(f"{to_move} (engine) played: {applied.san} ({applied.uci})")
            continue

        if side == "human":
            move_str = input(f"{to_move} (human) move (SAN or UCI): ").strip()
            applied = apply_move_to_game(args.game, move_str)
            print(f"{to_move} (human) played: {applied.san} ({applied.uci})")
            continue

        if side == "external":
            move_str = _external_pick_move(args.game, args.external_cmd)
            applied = apply_move_to_game(args.game, move_str)
            print(f"{to_move} (external) played: {applied.san} ({applied.uci})")
            continue

        raise RuntimeError(f"Unknown side kind: {side}")

    print(f"Reached max plies: {args.max_plies}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (LedgerError, chess.IllegalMoveError, chess.InvalidMoveError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        raise SystemExit(2)


