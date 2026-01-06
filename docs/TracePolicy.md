# Trace policy (inspectable reasoning)

Goal: make move selection **inspectable** and debuggable by writing the reasoning used for the move into repo text.

## What we record
We record a **decision trace** in `games/<game_id>/thinklog.md` using the required sections:
- Snapshot (state + pieces)
- Forcing scan (ALL checks, ALL captures)
- Candidate set (≤ 6)
- Legality proof (chosen move)
- Blunder screen (opponent forcing reply)
- Evaluation rubric summary
- Final (chosen move + explanation)

This trace is intended to be:
- sufficient for humans to audit “why this move”
- sufficient for future iterations of the agent to learn/adjust skills

## What we do NOT record
We do **not** rely on or attempt to preserve any hidden/internal chain-of-thought.

Instead, the **thinklog trace is the canonical reasoning artifact**. If something wasn’t written in the trace, treat it as “not checked”.

## How it is used
- During move selection, the agent may read prior `thinklog.md` entries to:
  - remember what it was trying to do
  - avoid repeating known mistakes
  - carry a plan forward
- In harness mode (LLM vs engine), the harness can sync the bundle thinklog into the canonical game thinklog so the trace remains visible after sealed move selection.


