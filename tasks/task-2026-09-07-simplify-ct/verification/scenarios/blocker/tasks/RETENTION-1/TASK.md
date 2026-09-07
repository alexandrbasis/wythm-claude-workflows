# Automatic customer-data retention

Objective: add a daily job that permanently deletes expired customer records.
Stage / status: planning blocked (2026-09-07).

## Known scope
Use the existing expiration selector in cleanup.py. Dry-run must be supported and automated deletion must remain disabled until configuration is complete.

## Open product decision
The retention period has not been decided. No source currently specifies how long customer records may be kept.

## Active plan

[ct-plan.md](ct-plan.md)

## Progress and next action

Planning is blocked at the material product decision: the retention period determines the deletion cutoff and irreversible deletion scope. Answer the retention-period question, record the decision here, then rerun `/ct`; the plan is not ready for `/si`.
