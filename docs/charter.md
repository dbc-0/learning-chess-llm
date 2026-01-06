# Charter

## Goal
Build a chess-playing agent whose move selection is:
- driven by plain-English skills
- inspectable via an append-only reasoning log
- self-improvable through PRs that modify skill text + add regression tests

## Non-goals (v1)
- Grandmaster strength
- Perfect blindfold play without a ledger
- Unbounded search

## Core constraints
During move selection, the agent may only read/write repo text files and use grep/ripgrep.
No chess engines or chess libraries may be used to choose moves.

## What “self-improving” means here
- After failures (illegal moves, missed tactics, blunders), the agent updates skills text and adds regression tests.
- Improvements must be evidenced via held-out tests and/or a fixed benchmark suite.

## Success metrics (ordered)
1) Illegal-move rate approaches zero
2) Missed-check rate approaches zero
3) Simple blunder rate (hanging queen/rook) approaches zero
4) Tactical puzzle score improves
5) Game results against a fixed ladder improve