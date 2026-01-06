from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import chess  # noqa: E402

from tools.referee import load_board_from_game, parse_move_any  # noqa: E402
from tools.uci_engine import UCIEngine, load_engine_config  # noqa: E402


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Evaluate a proposed move with a UCI engine (post-hoc).")
    p.add_argument("--game", default="", help="Game id under games/<id>/ledger.md (uses current position)")
    p.add_argument("--fen", default="", help="Evaluate from an explicit FEN instead of a game ledger")
    p.add_argument("--move", required=True, help="Move in SAN or UCI, evaluated from the current position")
    p.add_argument("--config", default="config/engine.json", help="Engine config JSON path")
    p.add_argument("--depth", type=int, default=0, help="Override analysis depth (0 = use config/go defaults)")
    p.add_argument("--movetime-ms", type=int, default=0, help="Override movetime in ms (0 = use config/go defaults)")
    p.add_argument("--out", default="", help="Optional report file to write (markdown)")
    return p.parse_args()


def _score_to_float(score: str | None) -> float | None:
    if not score:
        return None
    parts = score.split()
    if len(parts) != 2:
        return None
    kind, val = parts[0], parts[1]
    if kind == "cp":
        try:
            return float(int(val)) / 100.0
        except Exception:
            return None
    if kind == "mate":
        # arbitrary large value for mate scores; sign indicates side
        try:
            m = int(val)
            return 1000.0 if m > 0 else -1000.0
        except Exception:
            return None
    return None


def _to_white_pov(score_pawns: float, *, fen_turn_white: bool) -> float:
    """
    UCI scores are typically reported from the side-to-move's POV.
    Convert to a consistent "White POV" score (positive = good for White).
    """
    return score_pawns if fen_turn_white else -score_pawns


def _score_to_white_pov_pawns(score: str | None, *, fen_turn_white: bool) -> float | None:
    s = _score_to_float(score)
    if s is None:
        return None
    return _to_white_pov(s, fen_turn_white=fen_turn_white)


def main() -> int:
    args = _parse_args()

    if bool(args.game) == bool(args.fen):
        raise SystemExit("ERROR: provide exactly one of --game or --fen")

    if args.fen:
        board = chess.Board(args.fen)
        fen_before = board.fen()
        source_desc = f"fen `{fen_before}`"
    else:
        board, _ = load_board_from_game(args.game)
        fen_before = board.fen()
        source_desc = f"game `{args.game}`"
    move = parse_move_any(board, args.move)
    move_uci = move.uci()

    eng_path, uci_options, go = load_engine_config(args.config)
    if args.depth:
        go.depth = args.depth
        go.movetime_ms = None
    if args.movetime_ms:
        go.movetime_ms = args.movetime_ms
        go.depth = None
    with UCIEngine(eng_path, uci_options=uci_options) as eng:
        best = eng.analyze_from_fen(fen_before, go=go)
        bestmove = best["bestmove"]
        score_before = best.get("score")
        pv = best.get("pv")

        # Evaluate after playing the proposed move (from same side-to-move perspective as engine output)
        board_after = chess.Board(fen_before)
        board_after.push(move)
        after = eng.analyze_from_fen(board_after.fen(), go=go)
        score_after = after.get("score")

    # Convert both evals to White POV so deltas are meaningful.
    delta = None
    s1w = _score_to_white_pov_pawns(score_before, fen_turn_white=chess.Board(fen_before).turn)
    s2w = _score_to_white_pov_pawns(score_after, fen_turn_white=chess.Board(board_after.fen()).turn)
    if s1w is not None and s2w is not None:
        delta = s2w - s1w

    lines = []
    lines.append(f"# Engine eval (post-hoc) — {date.today().isoformat()}")
    lines.append("")
    lines.append(f"- source: {source_desc}")
    lines.append(f"- move: `{args.move}` (uci `{move_uci}`)")
    lines.append(f"- engine bestmove: `{bestmove}`")
    lines.append(f"- engine score before (raw, side-to-move POV): `{score_before}`")
    if s1w is not None:
        lines.append(f"- engine score before (White POV): `{s1w:+.2f}` pawns")
    lines.append(f"- engine score after (raw, side-to-move POV): `{score_after}`")
    if s2w is not None:
        lines.append(f"- engine score after (White POV): `{s2w:+.2f}` pawns")
    if delta is not None:
        lines.append(f"- approx delta (after - before), White POV: `{delta:+.2f}` pawns")
    if pv:
        lines.append("")
        lines.append(f"- pv (best line): `{pv}`")
    lines.append("")

    out_text = "\n".join(lines).rstrip() + "\n"
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text)
        print(f"Wrote: {out_path}")
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


