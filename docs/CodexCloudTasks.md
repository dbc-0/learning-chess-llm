# Codex Cloud Tasks contract (assumed) + local equivalent

You said: “assume Codex cloud tasks” and you want to run locally now with the same shape later.

This repo uses a simple **external command contract** that maps cleanly to a cloud task:

## Contract: “pick one move”
Given a **selection bundle** directory as the working directory, the task must:
- read `skills/` and `games/<game_id>/ledger.md` (and optionally update `thinklog.md` + `ledger.md` inside the bundle)
- print **exactly one move** to stdout (SAN preferred; UCI allowed)

The harness will:
- take that stdout move
- apply it to the canonical game ledger (outside the bundle) using legality checking

Locally, we simulate this via `tools/run_match.py --external-cmd ...` which runs your command with CWD set to a freshly generated bundle.

## Local smoke test

```bash
python tools/run_match.py --game demo --white external --black engine --external-cmd 'python -c "print(\"e4\")"'
```

## Important security property
The selection bundle does **not** include:
- engine configs/logs
- puzzle solutions
- harness code (python-chess) that can enumerate legal moves

So a remote move-selection agent cannot “cheat” by reading them.


