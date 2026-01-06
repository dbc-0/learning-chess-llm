# Geometry: board coordinates

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
