from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Import Lichess puzzles CSV into public/private JSONL files.")
    p.add_argument("--csv", required=True, help="Path to lichess_db_puzzle.csv (downloaded locally)")
    p.add_argument("--set", required=True, help="Output set name (used for filenames)")
    p.add_argument("--limit", type=int, default=0, help="Optional limit (0 = no limit)")
    return p.parse_args()


def _ensure_dirs() -> tuple[Path, Path]:
    pub = Path("puzzles/public")
    prv = Path("puzzles/private")
    pub.mkdir(parents=True, exist_ok=True)
    prv.mkdir(parents=True, exist_ok=True)
    return pub, prv


def _row_to_fields(row: dict[str, str] | list[str]) -> tuple[str, str, str, str, str]:
    """
    Returns: puzzle_id, fen, moves_uci_line, rating, themes, game_url

    Lichess puzzle DB (typical) header:
    PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl
    """
    if isinstance(row, dict):
        pid = row.get("PuzzleId") or row.get("puzzleId") or row.get("id")
        fen = row.get("FEN") or row.get("fen")
        moves = row.get("Moves") or row.get("moves")
        rating = row.get("Rating") or row.get("rating") or ""
        themes = row.get("Themes") or row.get("themes") or ""
        url = row.get("GameUrl") or row.get("gameUrl") or row.get("url") or ""
    else:
        # Fixed indices for the common schema
        # 0 PuzzleId, 1 FEN, 2 Moves, 3 Rating, 7 Themes, 8 GameUrl
        pid = row[0] if len(row) > 0 else None
        fen = row[1] if len(row) > 1 else None
        moves = row[2] if len(row) > 2 else None
        rating = row[3] if len(row) > 3 else ""
        themes = row[7] if len(row) > 7 else ""
        url = row[8] if len(row) > 8 else ""

    if not pid or not fen or not moves:
        raise ValueError("Row missing required fields (PuzzleId/FEN/Moves)")

    return str(pid), str(fen), str(moves), str(rating), str(themes), str(url)


def main() -> int:
    args = _parse_args()
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"ERROR: CSV not found: {csv_path}")

    pub_dir, prv_dir = _ensure_dirs()
    pub_out = pub_dir / f"{args.set}.jsonl"
    prv_out = prv_dir / f"{args.set}.jsonl"

    n = 0
    with csv_path.open(newline="", encoding="utf-8") as f, pub_out.open("w", encoding="utf-8") as pub, prv_out.open(
        "w", encoding="utf-8"
    ) as prv:
        # Detect header
        first_line = f.readline()
        f.seek(0)
        has_header = first_line.lower().startswith("puzzleid,") or first_line.lower().startswith("puzzleid;")

        if has_header:
            reader: object = csv.DictReader(f)
        else:
            reader = csv.reader(f)

        for row in reader:  # type: ignore[assignment]
            pid, fen, moves_line, rating, themes, url = _row_to_fields(row)  # type: ignore[arg-type]
            moves_uci = [m for m in moves_line.strip().split() if m]
            themes_list = [t for t in themes.strip().split() if t]

            pub_obj = {
                "puzzle_id": pid,
                "fen": fen,
                "rating": int(rating) if rating.isdigit() else rating,
                "themes": themes_list,
                "game_url": url,
            }
            prv_obj = {
                "puzzle_id": pid,
                "solution_uci": moves_uci,
            }

            pub.write(json.dumps(pub_obj) + "\n")
            prv.write(json.dumps(prv_obj) + "\n")

            n += 1
            if args.limit and n >= args.limit:
                break

    print(f"Wrote {n} puzzles to:")
    print(f"- public:  {pub_out}")
    print(f"- private: {prv_out}  (gitignored)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


