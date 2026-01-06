from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.ledger_io import board_to_new_ledger_text  # noqa: E402
from tools.make_selection_bundle import main as _make_bundle_main  # noqa: E402
from tools.referee import parse_move_any  # noqa: E402


@dataclass(frozen=True)
class Puzzle:
    puzzle_id: str
    fen: str


@dataclass(frozen=True)
class PuzzleSolution:
    puzzle_id: str
    solution_uci: list[str]


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run a puzzle set by asking an external move-picker for the first move.")
    p.add_argument("--set", required=True, help="Puzzle set name (expects puzzles/public/<set>.jsonl etc.)")
    p.add_argument("--n", type=int, default=50, help="How many puzzles to run")
    p.add_argument("--external-cmd", required=True, help="Command to run inside sealed bundle; prints 1 move to stdout")
    p.add_argument(
        "--out",
        default="reports/puzzle_run.md",
        help="Markdown report path (public, no solutions written)",
    )
    return p.parse_args()


def _load_public(set_name: str) -> list[Puzzle]:
    p = Path("puzzles/public") / f"{set_name}.jsonl"
    if not p.exists():
        raise FileNotFoundError(str(p))
    out: list[Puzzle] = []
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out.append(Puzzle(puzzle_id=obj["puzzle_id"], fen=obj["fen"]))
    return out


def _load_private(set_name: str) -> dict[str, PuzzleSolution]:
    p = Path("puzzles/private") / f"{set_name}.jsonl"
    if not p.exists():
        raise FileNotFoundError(
            f"{p} not found. Did you run tools/import_lichess_puzzles.py and keep puzzles/private locally?"
        )
    out: dict[str, PuzzleSolution] = {}
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out[obj["puzzle_id"]] = PuzzleSolution(puzzle_id=obj["puzzle_id"], solution_uci=list(obj["solution_uci"]))
    return out


def _make_bundle(game_id: str, out_dir: Path) -> None:
    argv0 = sys.argv[:]
    try:
        sys.argv = ["make_selection_bundle.py", "--game", game_id, "--out", str(out_dir)]
        _make_bundle_main()
    finally:
        sys.argv = argv0


def _run_external_in_bundle(bundle_dir: Path, cmd: str) -> str:
    proc = subprocess.run(shlex.split(cmd), cwd=str(bundle_dir), text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "External command failed.\n"
            f"cmd: {cmd}\n"
            f"cwd: {bundle_dir}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}\n"
        )
    move = (proc.stdout or "").strip().splitlines()[0].strip() if proc.stdout.strip() else ""
    if not move:
        raise RuntimeError("External command produced no move on stdout.")
    return move


def main() -> int:
    args = _parse_args()
    puzzles = _load_public(args.set)[: args.n]
    solutions = _load_private(args.set)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    correct = 0
    total = 0
    rows: list[str] = []

    run_id = f"{args.set}_{date.today().isoformat()}"

    for puz in puzzles:
        sol = solutions.get(puz.puzzle_id)
        if not sol or not sol.solution_uci:
            continue

        expected_uci = sol.solution_uci[0]

        # Create a temporary game directory in the repo, but under games/puzzle_runs/ (gitignored).
        game_id = f"puzzle_runs/{run_id}/{puz.puzzle_id}"
        game_dir = Path("games") / game_id
        game_dir.mkdir(parents=True, exist_ok=True)

        board = chess.Board(puz.fen)
        ledger_text = board_to_new_ledger_text(game_id=game_id, board=board, last_updated=str(date.today()))
        (game_dir / "ledger.md").write_text(ledger_text)
        (game_dir / "thinklog.md").write_text("# Thinklog (append-only)\n\n---\n")

        # Create sealed selection bundle and run external move picker.
        with tempfile.TemporaryDirectory(prefix="puzzle_bundle_") as tmp:
            bundle_dir = Path(tmp) / "bundle"
            _make_bundle(game_id, bundle_dir)
            picked = _run_external_in_bundle(bundle_dir, args.external_cmd)

        # Normalize picked move to UCI to compare (SAN allowed).
        try:
            mv = parse_move_any(board, picked)
            picked_uci = mv.uci()
        except Exception:
            picked_uci = f"(parse_error:{picked})"

        ok = picked_uci == expected_uci
        total += 1
        if ok:
            correct += 1
        rows.append(f"| {puz.puzzle_id} | {picked} | {picked_uci} | {expected_uci} | {'OK' if ok else 'NO'} |")

    acc = (correct / total) if total else 0.0

    report = []
    report.append(f"# Puzzle run: {run_id}")
    report.append("")
    report.append(f"- Set: `{args.set}`")
    report.append(f"- N requested: {args.n}")
    report.append(f"- N scored: {total}")
    report.append(f"- First-move accuracy: {correct}/{total} = {acc:.1%}")
    report.append("")
    report.append("## Per-puzzle results (first move)")
    report.append("| puzzle_id | picked_raw | picked_uci | expected_uci | ok |")
    report.append("|---|---|---|---|---|")
    report.extend(rows)
    Path(args.out).write_text("\n".join(report).rstrip() + "\n")

    print(f"Wrote report: {args.out}")
    print(f"Accuracy: {correct}/{total} = {acc:.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


