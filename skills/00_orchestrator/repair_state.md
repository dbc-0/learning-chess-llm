# Orchestrator: repair_state
ID: orch.repair_state.v1

Purpose: Repair ledger inconsistencies by replaying move history from the initial position recorded in ledger.

v1 placeholder:
- If invariants fail, do not guess. Prefer to stop and mark ledger as needing human repair.
- Later versions may implement full replay in plain English step-by-step.