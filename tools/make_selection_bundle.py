from __future__ import annotations

import argparse
import shutil
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Create a sealed 'move-selection bundle' directory containing only files "
            "the LLM is allowed to see during move selection."
        )
    )
    p.add_argument("--game", required=True, help="Game id under games/<id>/")
    p.add_argument(
        "--out",
        required=True,
        help="Output directory (will be created; if exists, it will be deleted first)",
    )
    return p.parse_args()


def _copytree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(str(src))
    shutil.copytree(src, dst)


def main() -> int:
    args = _parse_args()
    out_dir = Path(args.out).resolve()
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Copy skills (LLM is allowed to read these during move selection)
    _copytree(Path("skills"), out_dir / "skills")

    # Copy just the one game ledger + thinklog.
    game_src = Path("games") / args.game
    game_dst = out_dir / "games" / args.game
    game_dst.mkdir(parents=True, exist_ok=True)

    for name in ["ledger.md", "thinklog.md"]:
        src = game_src / name
        if src.exists():
            shutil.copy2(src, game_dst / name)
        else:
            # thinklog may not exist yet for a new game
            if name == "ledger.md":
                raise FileNotFoundError(str(src))

    # Also include the rules-of-engagement doc so remote runs can enforce constraints.
    for root_file in ["AGENTS.md", "Seed.md", "README.md"]:
        src = Path(root_file)
        if src.exists():
            shutil.copy2(src, out_dir / root_file)

    print(f"Wrote selection bundle to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


