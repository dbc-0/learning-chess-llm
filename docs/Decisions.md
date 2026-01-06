# Decisions

## D001: Ledger vs Thinklog split
Ledger is state only; thinklog is analysis only. Ledger is editable; thinklog is append-only.

## D002: Forcing scan is mandatory
Every move starts with enumerating ALL checks, then ALL captures.

## D003: Caps over “unbounded thinking”
We cap candidates and lookahead depth to avoid loops and quota blowups.

## D004: Grep-only retrieval (move selection)
During move selection, only grep/ripgrep is allowed for memory retrieval. No embeddings/vector search in v1.

## D005: Legality proof required
Chosen move must include a checklist-style legality proof in thinklog.