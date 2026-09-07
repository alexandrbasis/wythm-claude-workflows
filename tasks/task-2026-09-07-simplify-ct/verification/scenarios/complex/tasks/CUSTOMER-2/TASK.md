# Introduce full_name without breaking old clients

Objective: replace customer display_name with full_name across storage and API while old clients continue working.
Stage / status: plan ready for review; proposed phase creation awaits approval (2026-09-07).

## Agreed requirements
- Keep existing clients working during migration: display_name remains supported for a compatibility window.
- Preserve tenant isolation and all existing names.
- Backfill full_name from display_name without destructive column removal in this task.
- Provide safe rollback and verify mixed old/new data and clients.
- The user requests a proposed two-phase delivery structure: first establish compatible storage/service behavior, then add the new consumer. Phase creation has not yet been approved.

## Decisions
Retention of the old field is settled; removal belongs to a separate future task.

## Active plan

[ct-plan.md](ct-plan.md)

## Progress and next action

The plan is grounded in the existing schema, the tenant-scoped read lookup, and the fixture's `make test` command. The two-phase structure is proposed but no phase folders were created. Approve or reject that structure; if approved, create the phase records and hand Phase 1 to `/si` under separate implementation authorization.
