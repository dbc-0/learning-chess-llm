from __future__ import annotations

import argparse
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

from tools.engine_eval_move import _score_to_white_pov_pawns  # noqa: E402
from tools.make_selection_bundle import main as _make_bundle_main  # noqa: E402
from tools.referee import apply_engine_move_to_game, apply_move_to_game, load_board_from_game  # noqa: E402
from tools.uci_engine import UCIEngine, load_engine_config  # noqa: E402
from tools.new_game import main as _new_game_main  # noqa: E402


@dataclass(frozen=True)
class ReviewResult:
    ply: int
    fen_before: str
    picked_raw: str
    picked_uci: str
    engine_best_uci: str
    score_before: str | None
    score_after: str | None
    delta_pawns: float | None
    blunder: bool


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Run LLM vs Engine with post-hoc engine review after each LLM move.\n"
            "LLM move is obtained by running --external-cmd inside a sealed selection bundle.\n"
            "Stops at first detected blunder (eval drop threshold) or max plies."
        )
    )
    p.add_argument("--game", required=True, help="Game id under games/<id>/ledger.md")
    p.add_argument("--reset", action="store_true", help="(Re)create the game from the standard start position before running")
    p.add_argument("--llm-side", choices=["white", "black"], required=True)
    p.add_argument("--external-cmd", required=True, help="Command that prints exactly one move (SAN/UCI) to stdout")
    p.add_argument("--engine-config", default="config/engine.json")
    p.add_argument("--analysis-depth", type=int, default=10, help="Engine depth for review")
    p.add_argument("--blunder-threshold", type=float, default=-2.0, help="Stop if (after-before) <= threshold pawns")
    p.add_argument("--max-plies", type=int, default=60)
    p.add_argument(
        "--sync-thinklog",
        action="store_true",
        help=(
            "If set, copy the appended portion of games/<game>/thinklog.md from the selection bundle "
            "back into the canonical games/<game>/thinklog.md after each LLM move. "
            "This requires the external move-picker to append a trace in the bundle."
        ),
    )
    return p.parse_args()


def _make_bundle(game_id: str, out_dir: Path) -> None:
    argv0 = sys.argv[:]
    try:
        sys.argv = ["make_selection_bundle.py", "--game", game_id, "--out", str(out_dir)]
        _make_bundle_main()
    finally:
        sys.argv = argv0


def _run_external(cwd: Path, cmd: str) -> str:
    proc = subprocess.run(shlex.split(cmd), cwd=str(cwd), text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "External command failed.\n"
            f"cmd: {cmd}\n"
            f"cwd: {cwd}\n"
            f"stdout:\n{proc.stdout}\n"
            f"stderr:\n{proc.stderr}\n"
        )
    move = (proc.stdout or "").strip().splitlines()[0].strip() if proc.stdout.strip() else ""
    if not move:
        raise RuntimeError("External command produced no move on stdout.")
    return move


def _sync_thinklog_from_bundle(*, game_id: str, bundle_dir: Path) -> None:
    """
    Append any new content written to the bundle thinklog into the canonical thinklog.
    We do a simple 'append delta' sync: if canonical text is a prefix of bundle text, replace canonical with bundle.
    """
    canonical = Path("games") / game_id / "thinklog.md"
    bundle = bundle_dir / "games" / game_id / "thinklog.md"
    if not canonical.exists() or not bundle.exists():
        return

    canon_txt = canonical.read_text(encoding="utf-8")
    bundle_txt = bundle.read_text(encoding="utf-8")
    if bundle_txt.startswith(canon_txt) and bundle_txt != canon_txt:
        canonical.write_text(bundle_txt, encoding="utf-8")


def _engine_best_and_score(eng: UCIEngine, fen: str, depth: int) -> tuple[str, str | None]:
    info = eng.analyze_from_fen(fen, go=_mk_go(depth))
    return info["bestmove"], info.get("score")


def _mk_go(depth: int):
    from tools.uci_engine import UCIGo

    return UCIGo(depth=depth, movetime_ms=None)


def main() -> int:
    args = _parse_args()

    if args.reset:
        argv0 = sys.argv[:]
        try:
            sys.argv = ["new_game.py", "--game", args.game, "--force"]
            _new_game_main()
        finally:
            sys.argv = argv0

    llm_color = chess.WHITE if args.llm_side == "white" else chess.BLACK

    eng_path, uci_options, _go_unused = load_engine_config(args.engine_config)
    with UCIEngine(eng_path, uci_options=uci_options) as eng:
        results: list[ReviewResult] = []

        for ply in range(1, args.max_plies + 1):
            board, _ = load_board_from_game(args.game)
            if board.is_game_over(claim_draw=True):
                break

            if board.turn != llm_color:
                apply_engine_move_to_game(args.game, config_path=args.engine_config)
                continue

            fen_before = board.fen()
            engine_best, score_before = _engine_best_and_score(eng, fen_before, args.analysis_depth)

            # Run LLM selection in a sealed bundle located in a temporary directory,
            # so it can't accidentally see any engine logs or other repo files.
            with tempfile.TemporaryDirectory(prefix="selection_bundle_") as tmp:
                bundle_dir = Path(tmp) / "bundle"
                _make_bundle(args.game, bundle_dir)
                picked_raw = _run_external(bundle_dir, args.external_cmd)
                if args.sync_thinklog:
                    _sync_thinklog_from_bundle(game_id=args.game, bundle_dir=bundle_dir)

            # Apply the move to the real game ledger (legality checked via python-chess).
            applied = apply_move_to_game(args.game, picked_raw)
            picked_uci = applied.uci

            # Evaluate after move
            board_after, _ = load_board_from_game(args.game)
            score_after = _engine_best_and_score(eng, board_after.fen(), args.analysis_depth)[1]

            delta = None
            s1w = _score_to_white_pov_pawns(score_before, fen_turn_white=chess.Board(fen_before).turn)
            s2w = _score_to_white_pov_pawns(score_after, fen_turn_white=chess.Board(board_after.fen()).turn)
            if s1w is not None and s2w is not None:
                delta = s2w - s1w

            blunder = (delta is not None) and (delta <= args.blunder_threshold)
            results.append(
                ReviewResult(
                    ply=ply,
                    fen_before=fen_before,
                    picked_raw=picked_raw,
                    picked_uci=picked_uci,
                    engine_best_uci=engine_best,
                    score_before=score_before,
                    score_after=score_after,
                    delta_pawns=delta,
                    blunder=blunder,
                )
            )

            if blunder:
                break

            # Opponent reply
            apply_engine_move_to_game(args.game, config_path=args.engine_config)

    # Write report under engine_private
    out_dir = Path("games") / args.game / "engine_private"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "review.md"

    lines: list[str] = []
    lines.append(f"# LLM vs Engine review — {date.today().isoformat()}")
    lines.append("")
    lines.append(f"- game: `{args.game}`")
    lines.append(f"- llm_side: `{args.llm_side}`")
    lines.append(f"- analysis_depth: {args.analysis_depth}")
    lines.append(f"- blunder_threshold: {args.blunder_threshold:+.2f} pawns (delta after-before)")
    lines.append("")
    lines.append("## Per LLM move")
    lines.append("| ply | picked_raw | picked_uci | engine_best_uci | score_before | score_after | delta_pawns | blunder |")
    lines.append("|---:|---|---|---|---|---|---:|---|")
    for r in results:
        dp = "" if r.delta_pawns is None else f"{r.delta_pawns:+.2f}"
        lines.append(
            f"| {r.ply} | `{r.picked_raw}` | `{r.picked_uci}` | `{r.engine_best_uci}` | "
            f"`{r.score_before}` | `{r.score_after}` | {dp} | {'YES' if r.blunder else 'no'} |"
        )
    lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n")
    print(f"Wrote review report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


