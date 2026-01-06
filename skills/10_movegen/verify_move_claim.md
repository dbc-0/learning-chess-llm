# Skill: verify_move_claim
ID: movegen.verify_move_claim.v1

## Purpose
Given a proposed move (and any claim about it, like “this is a check” or “this captures X”), verify that the claim is **true** using:
- the current `games/<game_id>/ledger.md` piece list
- geometry lookup tables in `skills/11_geometry/`

This is designed to prevent the most common failure modes:
- illegal captures to empty squares (e.g., pawn capture when no piece is there)
- slider moves through blockers
- “this gives check” claims that aren’t actually check

## Inputs
- `games/<game_id>/ledger.md` (STATE + PIECES)
- Proposed move in SAN or UCI (plus any stated intent/claim)

## Outputs
- One of:
  - **VERIFIED** (with a short proof checklist)
  - **REFUTED** (with the exact failing condition)
  - **UNSURE** (if you cannot complete verification from available info; prefer not to play)

## Non-negotiable rule
- You MUST NOT output **VERIFIED** unless you have actually performed the lookups listed below (ledger occupancy + geometry tables).
- Do not “assume” a square is empty/occupied; read it from the ledger piece list.

## Required references
- `skills/11_geometry/rays.md`
- `skills/11_geometry/between_squares.md`
- `skills/11_geometry/knight_moves_table.md`
- `skills/11_geometry/king_moves_table.md`
- `skills/11_geometry/pawn_attacks.md`

## Procedure

### 0) Parse the move into (piece, from, to, capture?, check?, special?)
If SAN parsing is ambiguous, convert to UCI by reasoning from the ledger (or mark **UNSURE**).

### 1) Destination occupancy (all moves)
- If the move is a **capture**:
  - Verify `to` square is occupied by an enemy piece **in the ledger** OR it is a valid en-passant capture square (ledger EN_PASSANT).
  - If `to` is empty and not EN_PASSANT → **REFUTED**.
- If the move is **not a capture**:
  - Verify `to` is not occupied by any piece in the ledger.

**Proof requirement**:
- When you claim “occupied” or “empty”, name the piece token(s) on that square from the ledger (or explicitly say “no token is on <to>” after checking the list).

### 2) Piece movement geometry

#### 2A) Knight
- Open `skills/11_geometry/knight_moves_table.md`, find `Square: <from>`.
- Verify `<to>` appears in the move list.
- If not → **REFUTED**.

#### 2B) King (non-castling)
- Open `skills/11_geometry/king_moves_table.md`, find `Square: <from>`.
- Verify `<to>` appears in the move list.
- If not → **REFUTED**.

#### 2C) Bishop / Rook / Queen (sliders)
- Open `skills/11_geometry/rays.md`, find `Square: <from>`.
- Verify `<to>` appears on an appropriate ray:
  - rook rays for rook
  - bishop rays for bishop
  - either rook or bishop rays for queen
- If not → **REFUTED**.
- Use `between_squares.md` method:
  - list the between squares (ray entries before `<to>`)
  - verify every between square is empty in the ledger
  - if any blocker exists → **REFUTED**

**Proof requirement**:
- You must list the ray direction used (e.g., `E ray from d4`) and the between squares you checked.

#### 2D) Pawn
For pawn moves you must check **direction** and **capture vs push**:
- If capture:
  - Use `skills/11_geometry/pawn_attacks.md`, find `Square: <from>`.
  - Verify `<to>` is in the correct color’s attack list (white pawn attacks go “up”, black pawn attacks go “down”).
  - Also enforce **destination occupancy rule** from step 1.
- If non-capture push:
  - Verify `<to>` is one square forward (same file, ±1 rank depending on color) and empty.
  - For a two-square push from starting rank, verify both intermediate and destination are empty and that pawn is on its starting rank.

### 3) “This gives check” claim (if claimed)
To verify “move gives check”, you must prove that after the move, the moved piece attacks the enemy king square.
- Identify enemy king square from ledger PIECES (`K...` for side).
- For the moved piece on its new square:
  - Knight: check if king square is in its knight move list.
  - Slider: check if king square is on the appropriate ray and between squares are empty.
  - Pawn: check if king square is in pawn attack list.
If not → **REFUTED** (claim is false).

### 4) King safety (minimal, bounded)
After your move, ensure you did not leave your own king in check:
- Identify your king square.
- Check for immediate slider lines that could have been opened onto your king (rook/bishop/queen rays).
- Check enemy knight attacks onto your king using knight table.
If you cannot do this confidently → **UNSURE**.

## Output format
- VERIFIED: include 3–6 bullets naming the checks you performed (destination occupancy, ray membership, between squares, etc.).
- REFUTED: state exactly which condition failed.
- UNSURE: state which lookup you were unable to complete.


