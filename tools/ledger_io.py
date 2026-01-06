from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import chess


class LedgerError(RuntimeError):
    pass


_SIDE_RE = re.compile(r"^SIDE_TO_MOVE:\s*(White|Black)\s*$")
_CASTLING_RE = re.compile(r"^CASTLING:\s*White=([KQ-]+)\s+Black=([kq-]+)\s*$")
_EP_RE = re.compile(r"^EN_PASSANT:\s*([a-h][36]|-)\s*$")
_HALF_RE = re.compile(r"^HALFMOVE_CLOCK:\s*(\d+)\s*$")
_FULL_RE = re.compile(r"^FULLMOVE_NUMBER:\s*(\d+)\s*$")


@dataclass(frozen=True)
class LedgerState:
    side_to_move: str  # "White" | "Black"
    castling: str  # FEN castling rights string, e.g. "KQkq" or "-"
    en_passant: str  # square like "e3" or "-"
    halfmove_clock: int
    fullmove_number: int
    pieces_white: list[str]
    pieces_black: list[str]


def read_ledger_text(ledger_path: str) -> str:
    p = Path(ledger_path)
    if not p.exists():
        raise FileNotFoundError(f"Ledger not found: {ledger_path}")
    return p.read_text()


def parse_ledger(ledger_text: str) -> LedgerState:
    side_to_move: str | None = None
    castling: str | None = None
    en_passant: str | None = None
    halfmove_clock: int | None = None
    fullmove_number: int | None = None
    pieces_white: list[str] | None = None
    pieces_black: list[str] | None = None

    lines = [ln.rstrip("\n") for ln in ledger_text.splitlines()]
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = _SIDE_RE.match(ln)
        if m:
            side_to_move = m.group(1)
            i += 1
            continue
        m = _CASTLING_RE.match(ln)
        if m:
            w, b = m.group(1), m.group(2)
            fen = ""
            if w != "-":
                fen += w.replace("-", "")
            if b != "-":
                fen += b.replace("-", "")
            castling = fen if fen else "-"
            i += 1
            continue
        m = _EP_RE.match(ln)
        if m:
            en_passant = m.group(1)
            i += 1
            continue
        m = _HALF_RE.match(ln)
        if m:
            halfmove_clock = int(m.group(1))
            i += 1
            continue
        m = _FULL_RE.match(ln)
        if m:
            fullmove_number = int(m.group(1))
            i += 1
            continue

        # Parse PIECES block explicitly so we don't confuse it with CAPTURED.
        if ln.strip() == "PIECES:":
            i += 1
            while i < len(lines):
                cur = lines[i]
                if cur.strip() == "CAPTURED:" or cur.startswith("## "):
                    break
                if cur.strip().startswith("White:"):
                    pieces_white = _parse_piece_list_line(cur)
                elif cur.strip().startswith("Black:"):
                    pieces_black = _parse_piece_list_line(cur)
                i += 1
            continue

        i += 1

    missing = [
        name
        for name, val in [
            ("SIDE_TO_MOVE", side_to_move),
            ("CASTLING", castling),
            ("EN_PASSANT", en_passant),
            ("HALFMOVE_CLOCK", halfmove_clock),
            ("FULLMOVE_NUMBER", fullmove_number),
            ("PIECES White", pieces_white),
            ("PIECES Black", pieces_black),
        ]
        if val is None
    ]
    if missing:
        raise LedgerError(f"Ledger missing required fields: {', '.join(missing)}")

    return LedgerState(
        side_to_move=side_to_move,  # type: ignore[arg-type]
        castling=castling,  # type: ignore[arg-type]
        en_passant=en_passant,  # type: ignore[arg-type]
        halfmove_clock=halfmove_clock,  # type: ignore[arg-type]
        fullmove_number=fullmove_number,  # type: ignore[arg-type]
        pieces_white=pieces_white,  # type: ignore[arg-type]
        pieces_black=pieces_black,  # type: ignore[arg-type]
    )


def ledger_to_board(state: LedgerState) -> chess.Board:
    board = chess.Board(None)  # empty
    _place_pieces(board, state.pieces_white, is_white=True)
    _place_pieces(board, state.pieces_black, is_white=False)

    board.turn = state.side_to_move == "White"
    board.castling_rights = _castling_to_rights(state.castling)
    board.ep_square = chess.parse_square(state.en_passant) if state.en_passant != "-" else None
    board.halfmove_clock = state.halfmove_clock
    board.fullmove_number = state.fullmove_number
    return board


def board_to_ledger_text(
    *,
    game_id: str,
    previous_ledger_text: str,
    board: chess.Board,
    last_updated: str,
    last_move_san: str | None,
    last_move_uci: str | None,
) -> str:
    # We keep the overall ledger structure, but refresh STATE/PIECES and append move to history line.
    pieces_w, pieces_b = _board_piece_tokens(board)
    side = "White" if board.turn else "Black"
    castling = _rights_to_castling(board.castling_rights)
    ep = chess.square_name(board.ep_square) if board.ep_square is not None else "-"

    out_lines: list[str] = []
    lines = [ln.rstrip("\n") for ln in previous_ledger_text.splitlines()]
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("GAME_ID:"):
            out_lines.append(f"GAME_ID: {game_id}")
            i += 1
            continue
        if ln.startswith("LAST_UPDATED:"):
            out_lines.append(f"LAST_UPDATED: {last_updated}")
            i += 1
            continue
        if ln.startswith("SIDE_TO_MOVE:"):
            out_lines.append(f"SIDE_TO_MOVE: {side}")
            i += 1
            continue
        if ln.startswith("CASTLING:"):
            # preserve format "White=.. Black=.."
            w = "".join([c for c in castling if c in "KQ"]) or "-"
            b = "".join([c for c in castling if c in "kq"]) or "-"
            out_lines.append(f"CASTLING: White={w} Black={b}")
            i += 1
            continue
        if ln.startswith("EN_PASSANT:"):
            out_lines.append(f"EN_PASSANT: {ep}")
            i += 1
            continue
        if ln.startswith("HALFMOVE_CLOCK:"):
            out_lines.append(f"HALFMOVE_CLOCK: {board.halfmove_clock}")
            i += 1
            continue
        if ln.startswith("FULLMOVE_NUMBER:"):
            out_lines.append(f"FULLMOVE_NUMBER: {board.fullmove_number}")
            i += 1
            continue

        # Refresh pieces under PIECES: block (two following lines)
        if ln.strip() == "PIECES:":
            out_lines.append(ln)
            # consume following lines until next section header or until we've replaced White/Black lines
            i += 1
            replaced_w = False
            replaced_b = False
            while i < len(lines):
                cur = lines[i]
                if cur.strip() == "CAPTURED:" or cur.startswith("## "):
                    break
                if cur.strip().startswith("White:"):
                    out_lines.append("  White: " + " ".join(pieces_w) if pieces_w else "  White: -")
                    replaced_w = True
                elif cur.strip().startswith("Black:"):
                    out_lines.append("  Black: " + " ".join(pieces_b) if pieces_b else "  Black: -")
                    replaced_b = True
                else:
                    # keep other formatting lines
                    out_lines.append(cur)
                i += 1
            if not replaced_w:
                out_lines.append("  White: " + " ".join(pieces_w) if pieces_w else "  White: -")
            if not replaced_b:
                out_lines.append("  Black: " + " ".join(pieces_b) if pieces_b else "  Black: -")
            continue

        if ln.strip() == "## MOVE_HISTORY":
            out_lines.append(ln)
            i += 1
            # keep existing history lines, but append a new line with our move in a simple format
            while i < len(lines) and not lines[i].startswith("## "):
                out_lines.append(lines[i])
                i += 1
            if last_move_san or last_move_uci:
                san = last_move_san or "-"
                uci = last_move_uci or "-"
                out_lines.append(f"- {san} ({uci})")
            continue

        out_lines.append(ln)
        i += 1

    # If no MOVE_HISTORY section existed, add one.
    if "## MOVE_HISTORY" not in previous_ledger_text:
        out_lines += ["", "## MOVE_HISTORY"]
        if last_move_san or last_move_uci:
            san = last_move_san or "-"
            uci = last_move_uci or "-"
            out_lines.append(f"- {san} ({uci})")

    return "\n".join(out_lines).rstrip() + "\n"


def board_to_new_ledger_text(*, game_id: str, board: chess.Board, last_updated: str) -> str:
    """
    Create a brand-new ledger.md text from a python-chess Board.
    This is used by harness utilities (puzzles, custom start positions).
    """
    pieces_w, pieces_b = _board_piece_tokens(board)
    side = "White" if board.turn else "Black"
    castling = _rights_to_castling(int(board.castling_rights))
    w = "".join([c for c in castling if c in "KQ"]) or "-"
    b = "".join([c for c in castling if c in "kq"]) or "-"
    ep = chess.square_name(board.ep_square) if board.ep_square is not None else "-"

    return (
        "# Game Ledger\n\n"
        f"GAME_ID: {game_id}\n"
        f"LAST_UPDATED: {last_updated}\n\n"
        "## STATE\n"
        f"SIDE_TO_MOVE: {side}\n"
        f"CASTLING: White={w} Black={b}\n"
        f"EN_PASSANT: {ep}\n"
        f"HALFMOVE_CLOCK: {board.halfmove_clock}\n"
        f"FULLMOVE_NUMBER: {board.fullmove_number}\n\n"
        "PIECES:\n"
        f"  White: {' '.join(pieces_w) if pieces_w else '-'}\n"
        f"  Black: {' '.join(pieces_b) if pieces_b else '-'}\n\n"
        "CAPTURED:\n"
        "  White: -\n"
        "  Black: -\n\n"
        "## MOVE_HISTORY\n"
        "1. ...\n"
    )


def _parse_piece_list_line(line: str) -> list[str]:
    # Accept "White:" or "Black:" with optional indent
    _, rhs = line.split(":", 1)
    tokens = [t.strip() for t in rhs.strip().split() if t.strip() and t.strip() != "-"]
    return tokens


def _place_pieces(board: chess.Board, tokens: list[str], *, is_white: bool) -> None:
    for tok in tokens:
        if len(tok) < 3:
            raise LedgerError(f"Bad piece token: {tok!r}")
        p = tok[0]
        sq = tok[1:]
        if p not in "KQRBNP":
            raise LedgerError(f"Bad piece token: {tok!r}")
        if sq not in chess.SQUARE_NAMES:
            raise LedgerError(f"Bad square in token: {tok!r}")
        symbol = p if is_white else p.lower()
        piece = chess.Piece.from_symbol(symbol)
        board.set_piece_at(chess.parse_square(sq), piece)


def _castling_to_rights(castling: str) -> int:
    if castling == "-":
        return 0
    rights = 0
    if "K" in castling:
        rights |= int(chess.BB_H1)
    if "Q" in castling:
        rights |= int(chess.BB_A1)
    if "k" in castling:
        rights |= int(chess.BB_H8)
    if "q" in castling:
        rights |= int(chess.BB_A8)
    return rights


def _rights_to_castling(rights: int) -> str:
    # python-chess encodes castling rights as rook-square bitboards.
    out = ""
    if rights & int(chess.BB_H1):
        out += "K"
    if rights & int(chess.BB_A1):
        out += "Q"
    if rights & int(chess.BB_H8):
        out += "k"
    if rights & int(chess.BB_A8):
        out += "q"
    return out or "-"


def _board_piece_tokens(board: chess.Board) -> tuple[list[str], list[str]]:
    def tokens_for(color: chess.Color) -> list[str]:
        toks: list[str] = []
        for piece_type, letter in [
            (chess.KING, "K"),
            (chess.QUEEN, "Q"),
            (chess.ROOK, "R"),
            (chess.BISHOP, "B"),
            (chess.KNIGHT, "N"),
            (chess.PAWN, "P"),
        ]:
            squares = list(board.pieces(piece_type, color))
            squares.sort()
            for sq in squares:
                toks.append(letter + chess.square_name(sq))
        return toks

    return tokens_for(chess.WHITE), tokens_for(chess.BLACK)


