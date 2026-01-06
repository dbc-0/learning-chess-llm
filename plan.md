# Plan: Skills‑augmented LLM Chess (LLM-only move selection, engine-backed testing)

## Goals
- **Play “decent” chess using only repo text skills + ledger + thinklog** during move selection (no chess code, no engines, no chess libs).
- **Confirm/score moves with an engine** in a separate harness/referee layer that is *not available* to the LLM during move selection.
- **Train/evaluate basics with puzzles** (known solutions) without letting the LLM “cheat” by reading answers from the repo.
- **Flesh out skills** from the current high-level orchestrator into leaf skills and geometry “lookup” micro-skills.

## Non-negotiable constraints (from repo rules)
- During move selection, the agent may only:
  - read plain text skills in this repo
  - read the current `games/<game_id>/ledger.md` and logs
  - use repo text search (grep/ripgrep)
- Forbidden during move selection:
  - engines (Stockfish/Leela/etc)
  - chess libraries (e.g. python-chess) and any legality generator
  - external chess APIs/databases
- Per move:
  - output exactly **one** move (SAN preferred; UCI allowed)
  - append to `thinklog.md` (append-only)
  - update `ledger.md` **only** to reflect the move played

## Architecture additions (separation of concerns)

### A) “Move selection” (LLM-only; existing)
- Entrypoint skill: `skills/00_orchestrator/play_move.md`
- Inputs: `games/<game_id>/ledger.md` (+ optional non-engine meta like “playing a human”)
- Outputs:
  - one move (SAN/UCI)
  - updated ledger + appended thinklog

### B) “Referee / harness” (engine + legality + scoring; outside move selection)
Purpose: run games, enforce legality, generate opponent moves, and optionally score the LLM’s move quality.

Key property: **the LLM never sees engine output while choosing its move.**

Proposed components:
- `tools/` (scripts):
  - `tools/play_match.py` (or similar): runs a game loop
  - `tools/referee.py`: validates a proposed move against the current position, applies it, and can ask engine for opponent move
  - `tools/score_move.py`: post-hoc evaluation (centipawn loss, mate distance, etc.) *after* the move is locked in the ledger
- `engines/`:
  - local engine binary path confirming (Stockfish) via config only
  - **never** called from any skill markdown
- `config/engine.json`:
  - engine path, skill level, time control

Referee responsibilities:
- **Read** a position (from ledger or FEN snapshot)
- **Verify legality** of the LLM move (using chess code/libs) and either:
  - accept + apply it to a canonical internal state, or
  - reject + request a “repair attempt” (bounded) with clear error reasons
- **Write back** updated `ledger.md` (or generate a ledger update patch)
- **Generate opponent move** via engine and apply it (then update ledger again)
- **Optionally** write `games/<game_id>/engine_log.md` containing engine PV/eval for analysis
  - Important: this file must not be visible to the LLM when it is selecting a move (see “information hiding” below).

## Information hiding (preventing “engine/puzzle answer leakage”)
You have two separate “threat models”:

### 1) Interactive chat vs human (no engine)
- Simple: never run referee/engine; only use `ledger.md` + skills.

### 2) Automated harness vs engine / puzzle suite (engine allowed to harness)
You must prevent the move-selection prompt from accessing:
- engine outputs (PV/eval/best move)
- puzzle solutions

Practical approach for this repo:
- **Keep hidden data outside the repo / outside searchable paths** for the move-selection run.
  - Store solutions and engine logs in a directory the LLM cannot read/grep.
- If you must keep files locally alongside the repo, put them under a path that is:
  - excluded by `.gitignore` and the tooling used by the agent environment (or stored completely outside the project directory).

Concrete proposal:
- `puzzles/public/`: positions + metadata only (no answers)
- `puzzles/private/`: solutions (ignored, stored locally only)
- `games/<game_id>/engine_private/`: engine logs (ignored, stored locally only)

Referee reads from `puzzles/private/` and writes to `engine_private/`, but the LLM move-selection runtime does not.

Fallback (if strict hiding isn’t possible in a given environment):
- Accept that the LLM can “cheat” via grep and treat puzzle mode as a *development tool* rather than a robust benchmark.
- Still keep a clean separation in the code so we can later run “sealed” evaluations.

## Puzzle support (Lichess puzzles)

### Data formats to support
- Lichess puzzle export formats commonly include:
  - **FEN** for the starting position
  - **moves** / solution line (UCI), often multi-move
  - rating/themes metadata

We should support a minimal internal representation:
- `puzzles/public/<set_name>.jsonl` entries containing:
  - `puzzle_id`
  - `fen`
  - `side_to_move`
  - `goal` (e.g., “mate”, “win material”) if available
  - `rating`, `themes` (optional)
- `puzzles/private/<set_name>.jsonl` entries containing:
  - `puzzle_id`
  - `solution_uci` (array of moves)
  - `solution_san` (optional convenience)

### Puzzle runner behavior
- Converts FEN → a fresh `games/puzzle_<id>/ledger.md` snapshot.
- Invokes the LLM-only orchestrator to pick a move.
- Referee checks:
  - legality
  - whether the move matches the expected first move (or is within an allowed set, if multiple solutions are acceptable)
- Optionally continues for multi-move puzzles:
  - after LLM move, apply the puzzle’s “opponent reply” from the solution line,
  - then ask the LLM for the next move, etc. (bounded by solution length).

Success metrics:
- first-move accuracy by rating bucket
- full-line accuracy (for short tactical lines)
- illegal-move rate (should go to ~0 as skills improve)

## Skills roadmap (from high-level to micro-skills)

### Current state
`skills/00_orchestrator/play_move.md` already specifies:
- forcing scan (checks, captures)
- candidate set (≤ 6)
- bounded opponent forcing reply scan
- legality proof
- blunder screen
- rubric evaluation

### Skill decomposition (proposed directories)

#### 1) Orchestrators (top-level)
- `skills/00_orchestrator/play_move.md` (existing; will evolve)
- `skills/00_orchestrator/repair_state.md` (placeholder; expand to a deterministic repair protocol)

#### 2) Move generation primitives (still “LLM-only”, but explicit)
- `skills/10_movegen/enumerate_checks.md`
- `skills/10_movegen/enumerate_captures.md`
- `skills/10_movegen/enumerate_quiet_improving_moves.md` (bounded heuristics)
- `skills/10_movegen/legality_checklist.md` (king safety, blockers, occupancy, special rules)

#### 3) Geometry micro-skills (pure lookup / deterministic reasoning)
These are “human-table” style references the LLM can use without computation libraries.
- `skills/11_geometry/board_coords.md` (ranks/files, square color, adjacency)
- `skills/11_geometry/knight_moves_table.md` (from every square → destinations)
- `skills/11_geometry/king_moves_table.md`
- `skills/11_geometry/rays.md`:
  - for each square, list rook/bishop rays (ordered squares until edge)
  - queen = rook + bishop rays
- `skills/11_geometry/pawn_attacks.md` (white/black attack directions)
- `skills/11_geometry/between_squares.md` (how to verify slider blockage using rays)

#### 4) Tactical patterns & forcing logic
- `skills/20_tactics/check_types.md` (direct, discovered, double)
- `skills/20_tactics/hanging_pieces.md` (undefended/overloaded)
- `skills/20_tactics/pins_skewers_forks.md`
- `skills/20_tactics/mate_threat_screen.md` (basic mate patterns, back rank, smothered)

#### 5) Evaluation heuristics (bounded, concrete)
- `skills/30_eval/material_count.md`
- `skills/30_eval/king_safety.md`
- `skills/30_eval/development_and_activity.md`
- `skills/30_eval/pawn_structure.md`
- `skills/30_eval/blunder_screen.md` (formalize “drops queen/rook”, “allows immediate mate”, etc.)

#### 6) Ledger update / bookkeeping
- `skills/40_ledger/apply_move_to_ledger.md`:
  - update piece list
  - captures
  - castling rights / en passant
  - move history formatting
- `skills/40_ledger/invariants.md` (expanded; used by repair)

### Skill authoring principles
- **Explicit inputs/outputs**: what to read from ledger, what to produce (lists, candidates).
- **Bounded steps**: avoid open-ended search; respect max 6 candidates and 6 ply.
- **Concrete checklists**: especially for legality and blunder screening.
- **Graceful uncertainty**: mark “UNSURE” and prefer safer candidates if geometry is unclear.

## Testing strategy (make it measurable)

### 1) Text regression tests (LLM-only)
Add `tests/positions/` fixtures that include:
- a ledger snapshot
- a task (“choose a move for side to move”)
- expected properties (not necessarily a single best move):
  - “must list all checks”
  - “must list captures of X”
  - “must not output illegal move”
  - “must include legality proof fields”

### 2) Engine-backed integration tests (harness-only)
For a set of positions:
- run the agent to pick a move (no engine visible)
- referee validates and then evaluates the move quality (post-hoc)

Metrics:
- illegal move rate
- blunder rate (engine detects large eval drop)
- average centipawn loss (ACPL) on quiet positions
- puzzle accuracy by rating bucket

## Execution milestones (what we’ll build, in order)

### Milestone 1: Repo structure + minimal harness skeleton
- Add `tools/` scaffolding + config files.
- Add `tests/positions/` scaffold + one example fixture from the starting position.
- Define a clean boundary: move-selection reads only ledger/skills; harness owns engine and any chess libs.

### Milestone 2: Engine match runner
- Run “LLM vs engine” from the initial position.
- Persist game to `games/<game_id>/ledger.md` after each ply.
- Optional: engine log stored in hidden/private path.

### Milestone 3: Puzzle runner (offline dataset)
- Accept a local Lichess puzzle dump (or preprocessed jsonl).
- Create per-puzzle ledgers and run first-move evaluation.
- Enforce answer hiding via public/private split.

### Milestone 4: Skill expansion (most leverage early)
- Implement geometry micro-skills first (knight table + rays).
- Then implement enumerators for checks/captures that explicitly reference those geometry tables.
- Improve ledger update + repair procedures to reduce state drift.

### Milestone 5: Benchmarks + iteration loop
- Add a “daily benchmark” command that runs:
  - N engine plies from start
  - M puzzles across ratings
- Track metrics in a simple markdown report under `reports/` (public, no engine PV).

## Codex Remote / cloud compatibility (future-proofing)

To support a remote self-improvement loop (benchmark → propose skill PR → re-benchmark) while preserving the **LLM-only move selection** claim, use a strict two-workspace model:

- **Selection bundle workspace (LLM-only)**: contains only `skills/` + `games/<game_id>/{ledger.md,thinklog.md}` (and optionally `AGENTS.md` / `Seed.md`).  
  Generate it with `tools/make_selection_bundle.py`.
- **Harness workspace (engine allowed)**: runs `tools/` + python-chess + local UCI engines + private logs/answers.  
  Do not mount engine logs/answers into the selection bundle.

This makes local development and cloud runners (Codex Remote) follow the same boundary: the agent can iterate on skills using benchmark reports, but cannot access engine outputs while selecting a move.

## Open questions to resolve before implementation
- Which engine do you want to use by default (**Stockfish** is the usual choice)?
- Do you want the harness implemented in **Python** (simplest for UCI + PGN/FEN handling) even though move selection remains LLM-only?
- Where will you run sealed evaluations (so the LLM cannot read private solution/engine logs): locally, CI, or both?


