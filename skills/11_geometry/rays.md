# Geometry: rays (rook/bishop/queen)

For each square, list ray squares in each direction in order outward from the source square.
Use this together with `between_squares.md` to check blockers.

## Square: a1 (dark)

### Rook rays
- N: a2 a3 a4 a5 a6 a7 a8
- E: b1 c1 d1 e1 f1 g1 h1
- S: -
- W: -

### Bishop rays
- NE: b2 c3 d4 e5 f6 g7 h8
- NW: -
- SE: -
- SW: -

## Square: b1 (light)

### Rook rays
- N: b2 b3 b4 b5 b6 b7 b8
- E: c1 d1 e1 f1 g1 h1
- S: -
- W: a1

### Bishop rays
- NE: c2 d3 e4 f5 g6 h7
- NW: a2
- SE: -
- SW: -

## Square: c1 (dark)

### Rook rays
- N: c2 c3 c4 c5 c6 c7 c8
- E: d1 e1 f1 g1 h1
- S: -
- W: b1 a1

### Bishop rays
- NE: d2 e3 f4 g5 h6
- NW: b2 a3
- SE: -
- SW: -

## Square: d1 (light)

### Rook rays
- N: d2 d3 d4 d5 d6 d7 d8
- E: e1 f1 g1 h1
- S: -
- W: c1 b1 a1

### Bishop rays
- NE: e2 f3 g4 h5
- NW: c2 b3 a4
- SE: -
- SW: -

## Square: e1 (dark)

### Rook rays
- N: e2 e3 e4 e5 e6 e7 e8
- E: f1 g1 h1
- S: -
- W: d1 c1 b1 a1

### Bishop rays
- NE: f2 g3 h4
- NW: d2 c3 b4 a5
- SE: -
- SW: -

## Square: f1 (light)

### Rook rays
- N: f2 f3 f4 f5 f6 f7 f8
- E: g1 h1
- S: -
- W: e1 d1 c1 b1 a1

### Bishop rays
- NE: g2 h3
- NW: e2 d3 c4 b5 a6
- SE: -
- SW: -

## Square: g1 (dark)

### Rook rays
- N: g2 g3 g4 g5 g6 g7 g8
- E: h1
- S: -
- W: f1 e1 d1 c1 b1 a1

### Bishop rays
- NE: h2
- NW: f2 e3 d4 c5 b6 a7
- SE: -
- SW: -

## Square: h1 (light)

### Rook rays
- N: h2 h3 h4 h5 h6 h7 h8
- E: -
- S: -
- W: g1 f1 e1 d1 c1 b1 a1

### Bishop rays
- NE: -
- NW: g2 f3 e4 d5 c6 b7 a8
- SE: -
- SW: -

## Square: a2 (light)

### Rook rays
- N: a3 a4 a5 a6 a7 a8
- E: b2 c2 d2 e2 f2 g2 h2
- S: a1
- W: -

### Bishop rays
- NE: b3 c4 d5 e6 f7 g8
- NW: -
- SE: b1
- SW: -

## Square: b2 (dark)

### Rook rays
- N: b3 b4 b5 b6 b7 b8
- E: c2 d2 e2 f2 g2 h2
- S: b1
- W: a2

### Bishop rays
- NE: c3 d4 e5 f6 g7 h8
- NW: a3
- SE: c1
- SW: a1

## Square: c2 (light)

### Rook rays
- N: c3 c4 c5 c6 c7 c8
- E: d2 e2 f2 g2 h2
- S: c1
- W: b2 a2

### Bishop rays
- NE: d3 e4 f5 g6 h7
- NW: b3 a4
- SE: d1
- SW: b1

## Square: d2 (dark)

### Rook rays
- N: d3 d4 d5 d6 d7 d8
- E: e2 f2 g2 h2
- S: d1
- W: c2 b2 a2

### Bishop rays
- NE: e3 f4 g5 h6
- NW: c3 b4 a5
- SE: e1
- SW: c1

## Square: e2 (light)

### Rook rays
- N: e3 e4 e5 e6 e7 e8
- E: f2 g2 h2
- S: e1
- W: d2 c2 b2 a2

### Bishop rays
- NE: f3 g4 h5
- NW: d3 c4 b5 a6
- SE: f1
- SW: d1

## Square: f2 (dark)

### Rook rays
- N: f3 f4 f5 f6 f7 f8
- E: g2 h2
- S: f1
- W: e2 d2 c2 b2 a2

### Bishop rays
- NE: g3 h4
- NW: e3 d4 c5 b6 a7
- SE: g1
- SW: e1

## Square: g2 (light)

### Rook rays
- N: g3 g4 g5 g6 g7 g8
- E: h2
- S: g1
- W: f2 e2 d2 c2 b2 a2

### Bishop rays
- NE: h3
- NW: f3 e4 d5 c6 b7 a8
- SE: h1
- SW: f1

## Square: h2 (dark)

### Rook rays
- N: h3 h4 h5 h6 h7 h8
- E: -
- S: h1
- W: g2 f2 e2 d2 c2 b2 a2

### Bishop rays
- NE: -
- NW: g3 f4 e5 d6 c7 b8
- SE: -
- SW: g1

## Square: a3 (dark)

### Rook rays
- N: a4 a5 a6 a7 a8
- E: b3 c3 d3 e3 f3 g3 h3
- S: a2 a1
- W: -

### Bishop rays
- NE: b4 c5 d6 e7 f8
- NW: -
- SE: b2 c1
- SW: -

## Square: b3 (light)

### Rook rays
- N: b4 b5 b6 b7 b8
- E: c3 d3 e3 f3 g3 h3
- S: b2 b1
- W: a3

### Bishop rays
- NE: c4 d5 e6 f7 g8
- NW: a4
- SE: c2 d1
- SW: a2

## Square: c3 (dark)

### Rook rays
- N: c4 c5 c6 c7 c8
- E: d3 e3 f3 g3 h3
- S: c2 c1
- W: b3 a3

### Bishop rays
- NE: d4 e5 f6 g7 h8
- NW: b4 a5
- SE: d2 e1
- SW: b2 a1

## Square: d3 (light)

### Rook rays
- N: d4 d5 d6 d7 d8
- E: e3 f3 g3 h3
- S: d2 d1
- W: c3 b3 a3

### Bishop rays
- NE: e4 f5 g6 h7
- NW: c4 b5 a6
- SE: e2 f1
- SW: c2 b1

## Square: e3 (dark)

### Rook rays
- N: e4 e5 e6 e7 e8
- E: f3 g3 h3
- S: e2 e1
- W: d3 c3 b3 a3

### Bishop rays
- NE: f4 g5 h6
- NW: d4 c5 b6 a7
- SE: f2 g1
- SW: d2 c1

## Square: f3 (light)

### Rook rays
- N: f4 f5 f6 f7 f8
- E: g3 h3
- S: f2 f1
- W: e3 d3 c3 b3 a3

### Bishop rays
- NE: g4 h5
- NW: e4 d5 c6 b7 a8
- SE: g2 h1
- SW: e2 d1

## Square: g3 (dark)

### Rook rays
- N: g4 g5 g6 g7 g8
- E: h3
- S: g2 g1
- W: f3 e3 d3 c3 b3 a3

### Bishop rays
- NE: h4
- NW: f4 e5 d6 c7 b8
- SE: h2
- SW: f2 e1

## Square: h3 (light)

### Rook rays
- N: h4 h5 h6 h7 h8
- E: -
- S: h2 h1
- W: g3 f3 e3 d3 c3 b3 a3

### Bishop rays
- NE: -
- NW: g4 f5 e6 d7 c8
- SE: -
- SW: g2 f1

## Square: a4 (light)

### Rook rays
- N: a5 a6 a7 a8
- E: b4 c4 d4 e4 f4 g4 h4
- S: a3 a2 a1
- W: -

### Bishop rays
- NE: b5 c6 d7 e8
- NW: -
- SE: b3 c2 d1
- SW: -

## Square: b4 (dark)

### Rook rays
- N: b5 b6 b7 b8
- E: c4 d4 e4 f4 g4 h4
- S: b3 b2 b1
- W: a4

### Bishop rays
- NE: c5 d6 e7 f8
- NW: a5
- SE: c3 d2 e1
- SW: a3

## Square: c4 (light)

### Rook rays
- N: c5 c6 c7 c8
- E: d4 e4 f4 g4 h4
- S: c3 c2 c1
- W: b4 a4

### Bishop rays
- NE: d5 e6 f7 g8
- NW: b5 a6
- SE: d3 e2 f1
- SW: b3 a2

## Square: d4 (dark)

### Rook rays
- N: d5 d6 d7 d8
- E: e4 f4 g4 h4
- S: d3 d2 d1
- W: c4 b4 a4

### Bishop rays
- NE: e5 f6 g7 h8
- NW: c5 b6 a7
- SE: e3 f2 g1
- SW: c3 b2 a1

## Square: e4 (light)

### Rook rays
- N: e5 e6 e7 e8
- E: f4 g4 h4
- S: e3 e2 e1
- W: d4 c4 b4 a4

### Bishop rays
- NE: f5 g6 h7
- NW: d5 c6 b7 a8
- SE: f3 g2 h1
- SW: d3 c2 b1

## Square: f4 (dark)

### Rook rays
- N: f5 f6 f7 f8
- E: g4 h4
- S: f3 f2 f1
- W: e4 d4 c4 b4 a4

### Bishop rays
- NE: g5 h6
- NW: e5 d6 c7 b8
- SE: g3 h2
- SW: e3 d2 c1

## Square: g4 (light)

### Rook rays
- N: g5 g6 g7 g8
- E: h4
- S: g3 g2 g1
- W: f4 e4 d4 c4 b4 a4

### Bishop rays
- NE: h5
- NW: f5 e6 d7 c8
- SE: h3
- SW: f3 e2 d1

## Square: h4 (dark)

### Rook rays
- N: h5 h6 h7 h8
- E: -
- S: h3 h2 h1
- W: g4 f4 e4 d4 c4 b4 a4

### Bishop rays
- NE: -
- NW: g5 f6 e7 d8
- SE: -
- SW: g3 f2 e1

## Square: a5 (dark)

### Rook rays
- N: a6 a7 a8
- E: b5 c5 d5 e5 f5 g5 h5
- S: a4 a3 a2 a1
- W: -

### Bishop rays
- NE: b6 c7 d8
- NW: -
- SE: b4 c3 d2 e1
- SW: -

## Square: b5 (light)

### Rook rays
- N: b6 b7 b8
- E: c5 d5 e5 f5 g5 h5
- S: b4 b3 b2 b1
- W: a5

### Bishop rays
- NE: c6 d7 e8
- NW: a6
- SE: c4 d3 e2 f1
- SW: a4

## Square: c5 (dark)

### Rook rays
- N: c6 c7 c8
- E: d5 e5 f5 g5 h5
- S: c4 c3 c2 c1
- W: b5 a5

### Bishop rays
- NE: d6 e7 f8
- NW: b6 a7
- SE: d4 e3 f2 g1
- SW: b4 a3

## Square: d5 (light)

### Rook rays
- N: d6 d7 d8
- E: e5 f5 g5 h5
- S: d4 d3 d2 d1
- W: c5 b5 a5

### Bishop rays
- NE: e6 f7 g8
- NW: c6 b7 a8
- SE: e4 f3 g2 h1
- SW: c4 b3 a2

## Square: e5 (dark)

### Rook rays
- N: e6 e7 e8
- E: f5 g5 h5
- S: e4 e3 e2 e1
- W: d5 c5 b5 a5

### Bishop rays
- NE: f6 g7 h8
- NW: d6 c7 b8
- SE: f4 g3 h2
- SW: d4 c3 b2 a1

## Square: f5 (light)

### Rook rays
- N: f6 f7 f8
- E: g5 h5
- S: f4 f3 f2 f1
- W: e5 d5 c5 b5 a5

### Bishop rays
- NE: g6 h7
- NW: e6 d7 c8
- SE: g4 h3
- SW: e4 d3 c2 b1

## Square: g5 (dark)

### Rook rays
- N: g6 g7 g8
- E: h5
- S: g4 g3 g2 g1
- W: f5 e5 d5 c5 b5 a5

### Bishop rays
- NE: h6
- NW: f6 e7 d8
- SE: h4
- SW: f4 e3 d2 c1

## Square: h5 (light)

### Rook rays
- N: h6 h7 h8
- E: -
- S: h4 h3 h2 h1
- W: g5 f5 e5 d5 c5 b5 a5

### Bishop rays
- NE: -
- NW: g6 f7 e8
- SE: -
- SW: g4 f3 e2 d1

## Square: a6 (light)

### Rook rays
- N: a7 a8
- E: b6 c6 d6 e6 f6 g6 h6
- S: a5 a4 a3 a2 a1
- W: -

### Bishop rays
- NE: b7 c8
- NW: -
- SE: b5 c4 d3 e2 f1
- SW: -

## Square: b6 (dark)

### Rook rays
- N: b7 b8
- E: c6 d6 e6 f6 g6 h6
- S: b5 b4 b3 b2 b1
- W: a6

### Bishop rays
- NE: c7 d8
- NW: a7
- SE: c5 d4 e3 f2 g1
- SW: a5

## Square: c6 (light)

### Rook rays
- N: c7 c8
- E: d6 e6 f6 g6 h6
- S: c5 c4 c3 c2 c1
- W: b6 a6

### Bishop rays
- NE: d7 e8
- NW: b7 a8
- SE: d5 e4 f3 g2 h1
- SW: b5 a4

## Square: d6 (dark)

### Rook rays
- N: d7 d8
- E: e6 f6 g6 h6
- S: d5 d4 d3 d2 d1
- W: c6 b6 a6

### Bishop rays
- NE: e7 f8
- NW: c7 b8
- SE: e5 f4 g3 h2
- SW: c5 b4 a3

## Square: e6 (light)

### Rook rays
- N: e7 e8
- E: f6 g6 h6
- S: e5 e4 e3 e2 e1
- W: d6 c6 b6 a6

### Bishop rays
- NE: f7 g8
- NW: d7 c8
- SE: f5 g4 h3
- SW: d5 c4 b3 a2

## Square: f6 (dark)

### Rook rays
- N: f7 f8
- E: g6 h6
- S: f5 f4 f3 f2 f1
- W: e6 d6 c6 b6 a6

### Bishop rays
- NE: g7 h8
- NW: e7 d8
- SE: g5 h4
- SW: e5 d4 c3 b2 a1

## Square: g6 (light)

### Rook rays
- N: g7 g8
- E: h6
- S: g5 g4 g3 g2 g1
- W: f6 e6 d6 c6 b6 a6

### Bishop rays
- NE: h7
- NW: f7 e8
- SE: h5
- SW: f5 e4 d3 c2 b1

## Square: h6 (dark)

### Rook rays
- N: h7 h8
- E: -
- S: h5 h4 h3 h2 h1
- W: g6 f6 e6 d6 c6 b6 a6

### Bishop rays
- NE: -
- NW: g7 f8
- SE: -
- SW: g5 f4 e3 d2 c1

## Square: a7 (dark)

### Rook rays
- N: a8
- E: b7 c7 d7 e7 f7 g7 h7
- S: a6 a5 a4 a3 a2 a1
- W: -

### Bishop rays
- NE: b8
- NW: -
- SE: b6 c5 d4 e3 f2 g1
- SW: -

## Square: b7 (light)

### Rook rays
- N: b8
- E: c7 d7 e7 f7 g7 h7
- S: b6 b5 b4 b3 b2 b1
- W: a7

### Bishop rays
- NE: c8
- NW: a8
- SE: c6 d5 e4 f3 g2 h1
- SW: a6

## Square: c7 (dark)

### Rook rays
- N: c8
- E: d7 e7 f7 g7 h7
- S: c6 c5 c4 c3 c2 c1
- W: b7 a7

### Bishop rays
- NE: d8
- NW: b8
- SE: d6 e5 f4 g3 h2
- SW: b6 a5

## Square: d7 (light)

### Rook rays
- N: d8
- E: e7 f7 g7 h7
- S: d6 d5 d4 d3 d2 d1
- W: c7 b7 a7

### Bishop rays
- NE: e8
- NW: c8
- SE: e6 f5 g4 h3
- SW: c6 b5 a4

## Square: e7 (dark)

### Rook rays
- N: e8
- E: f7 g7 h7
- S: e6 e5 e4 e3 e2 e1
- W: d7 c7 b7 a7

### Bishop rays
- NE: f8
- NW: d8
- SE: f6 g5 h4
- SW: d6 c5 b4 a3

## Square: f7 (light)

### Rook rays
- N: f8
- E: g7 h7
- S: f6 f5 f4 f3 f2 f1
- W: e7 d7 c7 b7 a7

### Bishop rays
- NE: g8
- NW: e8
- SE: g6 h5
- SW: e6 d5 c4 b3 a2

## Square: g7 (dark)

### Rook rays
- N: g8
- E: h7
- S: g6 g5 g4 g3 g2 g1
- W: f7 e7 d7 c7 b7 a7

### Bishop rays
- NE: h8
- NW: f8
- SE: h6
- SW: f6 e5 d4 c3 b2 a1

## Square: h7 (light)

### Rook rays
- N: h8
- E: -
- S: h6 h5 h4 h3 h2 h1
- W: g7 f7 e7 d7 c7 b7 a7

### Bishop rays
- NE: -
- NW: g8
- SE: -
- SW: g6 f5 e4 d3 c2 b1

## Square: a8 (light)

### Rook rays
- N: -
- E: b8 c8 d8 e8 f8 g8 h8
- S: a7 a6 a5 a4 a3 a2 a1
- W: -

### Bishop rays
- NE: -
- NW: -
- SE: b7 c6 d5 e4 f3 g2 h1
- SW: -

## Square: b8 (dark)

### Rook rays
- N: -
- E: c8 d8 e8 f8 g8 h8
- S: b7 b6 b5 b4 b3 b2 b1
- W: a8

### Bishop rays
- NE: -
- NW: -
- SE: c7 d6 e5 f4 g3 h2
- SW: a7

## Square: c8 (light)

### Rook rays
- N: -
- E: d8 e8 f8 g8 h8
- S: c7 c6 c5 c4 c3 c2 c1
- W: b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: d7 e6 f5 g4 h3
- SW: b7 a6

## Square: d8 (dark)

### Rook rays
- N: -
- E: e8 f8 g8 h8
- S: d7 d6 d5 d4 d3 d2 d1
- W: c8 b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: e7 f6 g5 h4
- SW: c7 b6 a5

## Square: e8 (light)

### Rook rays
- N: -
- E: f8 g8 h8
- S: e7 e6 e5 e4 e3 e2 e1
- W: d8 c8 b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: f7 g6 h5
- SW: d7 c6 b5 a4

## Square: f8 (dark)

### Rook rays
- N: -
- E: g8 h8
- S: f7 f6 f5 f4 f3 f2 f1
- W: e8 d8 c8 b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: g7 h6
- SW: e7 d6 c5 b4 a3

## Square: g8 (light)

### Rook rays
- N: -
- E: h8
- S: g7 g6 g5 g4 g3 g2 g1
- W: f8 e8 d8 c8 b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: h7
- SW: f7 e6 d5 c4 b3 a2

## Square: h8 (dark)

### Rook rays
- N: -
- E: -
- S: h7 h6 h5 h4 h3 h2 h1
- W: g8 f8 e8 d8 c8 b8 a8

### Bishop rays
- NE: -
- NW: -
- SE: -
- SW: g7 f6 e5 d4 c3 b2 a1
