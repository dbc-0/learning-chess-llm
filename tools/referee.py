from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import chess

from tools.ledger_io import LedgerError, board_to_ledger_text, ledger_to_board, parse_ledger, read_ledger_text
from tools.uci_engine import UCIEngine, load_engine_config


@dataclass(frozen=True)
class AppliedMove:
    san: str
    uci: str
    fen_after: str


def _game_ledger_path(game_id: str) -> Path:
    return Path("games") / game_id / "ledger.md"


def load_board_from_game(game_id: str) -> tuple[chess.Board, str]:
    ledger_path = _game_ledger_path(game_id)
    ledger_text = read_ledger_text(str(ledger_path))
    state = parse_ledger(ledger_text)
    board = ledger_to_board(state)
    return board, ledger_text


def parse_move_any(board: chess.Board, move_str: str) -> chess.Move:
    s = move_str.strip()
    # Try UCI first if it looks like UCI.
    if len(s) in (4, 5) and s[0] in "abcdefgh" and s[2] in "abcdefgh":
        try:
            mv = chess.Move.from_uci(s)
            if mv in board.legal_moves:
                return mv
        except Exception:
            pass
    # Fallback: SAN
    return board.parse_san(s)


def apply_move_to_game(game_id: str, move_str: str) -> AppliedMove:
    board, ledger_text = load_board_from_game(game_id)
    move = parse_move_any(board, move_str)

    if move not in board.legal_moves:
        raise LedgerError(f"Illegal move for current position: {move_str!r}")

    san = board.san(move)
    uci = move.uci()
    board.push(move)

    ledger_path = _game_ledger_path(game_id)
    new_text = board_to_ledger_text(
        game_id=game_id,
        previous_ledger_text=ledger_text,
        board=board,
        last_updated=str(date.today()),
        last_move_san=san,
        last_move_uci=uci,
    )
    ledger_path.write_text(new_text)
    return AppliedMove(san=san, uci=uci, fen_after=board.fen())


def apply_engine_move_to_game(game_id: str, config_path: str = "config/engine.json") -> AppliedMove:
    board, ledger_text = load_board_from_game(game_id)
    eng_path, uci_options, go = load_engine_config(config_path)

    with UCIEngine(eng_path, uci_options=uci_options) as eng:
        best_uci = eng.bestmove_from_fen(board.fen(), go=go)

    move = chess.Move.from_uci(best_uci)
    if move not in board.legal_moves:
        raise LedgerError(f"Engine returned illegal move for current position: {best_uci}")

    san = board.san(move)
    board.push(move)

    ledger_path = _game_ledger_path(game_id)
    new_text = board_to_ledger_text(
        game_id=game_id,
        previous_ledger_text=ledger_text,
        board=board,
        last_updated=str(date.today()),
        last_move_san=san,
        last_move_uci=best_uci,
    )
    ledger_path.write_text(new_text)
    return AppliedMove(san=san, uci=best_uci, fen_after=board.fen())


