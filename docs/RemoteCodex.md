# Codex Remote Compatibility (cloud self-improvement loop)

This repo has two kinds of computation:

1) **Move selection (LLM-only)**  
   Must only use repo text skills + the current game ledger/thinklog.

2) **Harness / referee (code + engines)**  
   Can use chess libraries + an engine to enforce legality, generate an opponent move, and score moves **after** they are chosen.

Codex Remote (or any cloud agent runner) works best if you make the separation explicit via **two workspaces**.

## Recommended “two workspace” model

### Workspace A: selection bundle (LLM-only)
Contains only:
- `skills/`
- `games/<game_id>/{ledger.md,thinklog.md}`
- optionally `AGENTS.md` / `Seed.md` / `README.md`

Create it with:

```bash
python tools/make_selection_bundle.py --game <game_id> --out /tmp/selection_bundle
```

In a remote setup, configure Codex to operate **only** in this bundle when producing the next move.

### Workspace B: harness workspace (engine allowed)
Contains:
- `tools/` (python-chess, referee scripts)
- engine config (local secret): `config/engine.json` (ignored by git)
- engine binary + (for lc0) weights (outside repo)
- optionally private logs and puzzle answers (outside selection bundle)

The harness:
- reads the canonical ledger from the “main” game workspace
- asks Codex (selection bundle) for exactly one move
- applies that move with legality checking
- optionally asks engine for opponent move and applies it
- optionally scores the LLM move post-hoc (store results outside the selection bundle)

## Why this prevents “cheating”
- The selection bundle simply does not contain:
  - engine PV/evals
  - puzzle solutions
  - engine binaries/weights
  - harness code that could compute legal moves
- Even if the agent tries to grep, those files aren’t present.

## Practical tips for running in the cloud
- **Do not commit engine paths or weights.** Keep them as secrets/artifacts in the remote runner.
- Prefer a workflow where the harness never prints engine PV/eval into logs that the LLM can read during move selection.
- If you want post-hoc analysis, write it to a private directory that is not mounted into the selection bundle.

## Suggested self-improvement loop (Codex)
1) Run a benchmark suite (engine games + puzzles) using the harness.
2) Produce a short report (metrics + example failures) for Codex.
3) Ask Codex to propose skill edits (PR-style changes).
4) Re-run benchmarks and compare deltas.

Key rule: **Codex can use harness outputs to improve skills, but must not use engine outputs to choose an in-game move.**


