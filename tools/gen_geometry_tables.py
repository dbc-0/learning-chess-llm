from __future__ import annotations

from pathlib import Path

FILES = "abcdefgh"
RANKS = "12345678"


def sq(file_idx: int, rank_idx: int) -> str:
    return f"{FILES[file_idx]}{RANKS[rank_idx]}"


def in_bounds(f: int, r: int) -> bool:
    return 0 <= f < 8 and 0 <= r < 8


def ray_from(f: int, r: int, df: int, dr: int) -> list[str]:
    out: list[str] = []
    cf, cr = f + df, r + dr
    while in_bounds(cf, cr):
        out.append(sq(cf, cr))
        cf += df
        cr += dr
    return out


def knight_moves(f: int, r: int) -> list[str]:
    deltas = [
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
        (-2, 1),
        (-1, 2),
    ]
    out = []
    for df, dr in deltas:
        cf, cr = f + df, r + dr
        if in_bounds(cf, cr):
            out.append(sq(cf, cr))
    return sorted(out)


def king_moves(f: int, r: int) -> list[str]:
    out = []
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            cf, cr = f + df, r + dr
            if in_bounds(cf, cr):
                out.append(sq(cf, cr))
    return sorted(out)


def pawn_attacks_white(f: int, r: int) -> list[str]:
    out = []
    for df in (-1, 1):
        cf, cr = f + df, r + 1
        if in_bounds(cf, cr):
            out.append(sq(cf, cr))
    return sorted(out)


def pawn_attacks_black(f: int, r: int) -> list[str]:
    out = []
    for df in (-1, 1):
        cf, cr = f + df, r - 1
        if in_bounds(cf, cr):
            out.append(sq(cf, cr))
    return sorted(out)


def square_color(f: int, r: int) -> str:
    # a1 is dark. If (file+rank) is even -> dark.
    return "dark" if (f + r) % 2 == 0 else "light"


def write_board_coords(out_dir: Path) -> None:
    text = """# Geometry: board coordinates

## Coordinates
- Files: a b c d e f g h (left-to-right from White's perspective)
- Ranks: 1 2 3 4 5 6 7 8 (bottom-to-top from White's perspective)
- Squares are file+rank, e.g. `e4`.

## Square color
- `a1` is **dark**.
- Rule: a square is **dark** iff (file_index + rank_index) is even, with `a=0..h=7`, `1=0..8=7`.

## Direction conventions (from White's perspective)
- North: +rank (toward 8)
- South: -rank (toward 1)
- East: +file (toward h)
- West: -file (toward a)

## Diagonals
- NE: +file, +rank
- NW: -file, +rank
- SE: +file, -rank
- SW: -file, -rank
"""
    (out_dir / "board_coords.md").write_text(text, encoding="utf-8")


def write_between_squares(out_dir: Path) -> None:
    text = """# Geometry: between-squares method (for sliders)

Use this to verify bishop/rook/queen moves and attacks using `rays.md`.

## Definitions
- **Ray list**: an ordered list of squares from the source square outward in one direction until the edge.
- **Between squares**: the squares strictly between source and destination on that ray.

## Method
To prove a slider move `S -> D` is geometrically valid:
1) Open `skills/11_geometry/rays.md` and find `Square: S`.
2) Look for a ray list that contains `D`.
   - If `D` is not present on any appropriate ray (rook rays for rook, bishop rays for bishop, either for queen), the move is impossible.
3) The **between squares** are the entries in that ray list **before** `D`.
4) Verify every between-square is empty using the ledger piece list.

## Examples (conceptual)
- If the NE ray from `c4` is `d5 e6 f7 g8`, then:
  - `c4 -> f7` has between squares `d5 e6`.
- If the E ray from `a1` is `b1 c1 d1 e1 f1 g1 h1`, then:
  - `a1 -> e1` has between squares `b1 c1 d1`.
"""
    (out_dir / "between_squares.md").write_text(text, encoding="utf-8")


def write_rays(out_dir: Path) -> None:
    lines: list[str] = []
    lines.append("# Geometry: rays (rook/bishop/queen)")
    lines.append("")
    lines.append("For each square, list ray squares in each direction in order outward from the source square.")
    lines.append("Use this together with `between_squares.md` to check blockers.")
    lines.append("")

    for r in range(8):
        for f in range(8):
            s = sq(f, r)
            lines.append(f"## Square: {s} ({square_color(f, r)})")
            lines.append("")
            lines.append("### Rook rays")
            lines.append(f"- N: {' '.join(ray_from(f, r, 0, 1)) or '-'}")
            lines.append(f"- E: {' '.join(ray_from(f, r, 1, 0)) or '-'}")
            lines.append(f"- S: {' '.join(ray_from(f, r, 0, -1)) or '-'}")
            lines.append(f"- W: {' '.join(ray_from(f, r, -1, 0)) or '-'}")
            lines.append("")
            lines.append("### Bishop rays")
            lines.append(f"- NE: {' '.join(ray_from(f, r, 1, 1)) or '-'}")
            lines.append(f"- NW: {' '.join(ray_from(f, r, -1, 1)) or '-'}")
            lines.append(f"- SE: {' '.join(ray_from(f, r, 1, -1)) or '-'}")
            lines.append(f"- SW: {' '.join(ray_from(f, r, -1, -1)) or '-'}")
            lines.append("")

    (out_dir / "rays.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_knight_table(out_dir: Path) -> None:
    lines: list[str] = []
    lines.append("# Geometry: knight moves table")
    lines.append("")
    lines.append("For each square, list all destination squares a knight can move to.")
    lines.append("")
    for r in range(8):
        for f in range(8):
            s = sq(f, r)
            moves = knight_moves(f, r)
            lines.append(f"## Square: {s}")
            lines.append(f"- Moves: {' '.join(moves) if moves else '-'}")
            lines.append("")
    (out_dir / "knight_moves_table.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_king_table(out_dir: Path) -> None:
    lines: list[str] = []
    lines.append("# Geometry: king moves table")
    lines.append("")
    lines.append("For each square, list all destination squares a king can move to (ignores check legality).")
    lines.append("")
    for r in range(8):
        for f in range(8):
            s = sq(f, r)
            moves = king_moves(f, r)
            lines.append(f"## Square: {s}")
            lines.append(f"- Moves: {' '.join(moves) if moves else '-'}")
            lines.append("")
    (out_dir / "king_moves_table.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_pawn_attacks(out_dir: Path) -> None:
    lines: list[str] = []
    lines.append("# Geometry: pawn attacks")
    lines.append("")
    lines.append("For each square, list the squares attacked by a pawn *on that square* (ignores occupancy).")
    lines.append("")
    for r in range(8):
        for f in range(8):
            s = sq(f, r)
            wa = pawn_attacks_white(f, r)
            ba = pawn_attacks_black(f, r)
            lines.append(f"## Square: {s}")
            lines.append(f"- White pawn attacks: {' '.join(wa) if wa else '-'}")
            lines.append(f"- Black pawn attacks: {' '.join(ba) if ba else '-'}")
            lines.append("")
    (out_dir / "pawn_attacks.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    out_dir = Path("skills/11_geometry")
    out_dir.mkdir(parents=True, exist_ok=True)
    write_board_coords(out_dir)
    write_between_squares(out_dir)
    write_rays(out_dir)
    write_knight_table(out_dir)
    write_king_table(out_dir)
    write_pawn_attacks(out_dir)
    print(f"Wrote geometry tables under {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


