# Architecture

## Files and responsibilities

### 1) Skills (general, versioned)
`skills/` contains plain-English “callable” procedures with:
- explicit inputs and outputs
- bounded steps and stop conditions
- failure modes and fallbacks

Only orchestrators should “call” other skills; leaf skills are primitives.

### 2) Game ledger (single source of truth)
`games/<game_id>/ledger.md`
- canonical piece list and rights (castling, en passant)
- side to move
- move history
- captured pieces

Ledger contains state only, not analysis.

### 3) Think log (append-only)
`games/<game_id>/thinklog.md`
- per-move trace of the agent’s process
- never rewrite old entries
- must include the required trace sections from AGENTS.md

### 4) Memory (optional, later)
`memory/`
- cards: experience cards keyed by position signatures
- index: grep-friendly inverted indexes
- templates: generalized pattern templates

Memory may propose candidate ideas, but final move still must pass the same forcing scan + legality proof.

### 5) Tests (textual regression specs)
`tests/positions/`
- each file contains a ledger snapshot + task + expected output(s)
- used to justify PRs improving skills

## Move selection pipeline (high level)
1) Read ledger
2) Forcing scan: enumerate checks then captures
3) Candidate generation (max 6)
4) Quick opponent forcing reply scan (bounded)
5) Choose move by rubric + blunder screen
6) Append thinklog entry
7) Apply move to ledger

## Invariants (must hold; used to detect ledger corruption)
- exactly one white king and one black king
- no two pieces share a square
- side to move is valid
- captures reduce piece count correctly
- pawns never on rank 1 or 8
- castling rights and en passant fields are syntactically valid