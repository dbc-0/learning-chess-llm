# Geometry: between-squares method (for sliders)

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
