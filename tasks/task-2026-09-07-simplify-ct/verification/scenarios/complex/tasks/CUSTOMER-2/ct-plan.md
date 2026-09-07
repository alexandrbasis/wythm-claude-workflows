# `/ct` result: CUSTOMER-2

Task: `TASK.md`

Stage / status: **plan ready for review; proposed phase creation awaits approval**

## Context and evidence

- The scenario `README.md` says tenant identity is part of the request context and no external services are available.
- `../../Makefile` defines the fixture test command: `make test` runs `python3 -m unittest discover -s tests -q` from the scenario root.
- `../../migrations/001_customers.sql` stores `display_name TEXT NOT NULL` with `(tenant_id, id)` as the primary key.
- `../../service.py` is a read lookup only: it returns the row selected by both `tenant_id` and `id`; that tenant predicate must remain unchanged.
- `../../tests/test_service.py` currently verifies tenant isolation.

## Changes

The compatibility window keeps `display_name` available while `full_name` becomes the canonical field for new behavior. Existing rows are backfilled, and new service/API write-normalization work will accept either client field and keep both fields available during the window. The existing `display_name` column is retained for this task.

## Proposed two-phase delivery

Phase folders are **not** created because the task only requests a proposed structure and phase creation has not been approved.

### Phase 1 — compatible storage and service behavior

1. Add a new migration (proposed path: `../../migrations/002_customer_full_name.sql`) that adds nullable `full_name` without removing `display_name`.
2. Backfill `full_name` from `display_name` for every existing row; make the operation idempotent and preserve the existing name values.
3. Add new service/API mapping and write-normalization behavior alongside the existing read-only `get_customer` lookup. Accept and return `full_name` while `display_name` remains supported; during the compatibility window, normalize either input form to both stored/output fields so old and new clients can coexist.
4. Keep the `tenant_id` and `id` selection predicate intact and add mixed-data tests for same IDs in different tenants.
5. Make rollback safe by disabling the new field mapping and routing new consumer behavior through the retained `display_name`; do not drop either column in this task.

### Phase 2 — new consumer

1. Add or update the new API consumer to read and send `full_name` as its preferred field while accepting the compatibility alias `display_name`.
2. Verify old-client requests, new-client requests, and mixed old/new rows through the same tenant-scoped service path.
3. Keep the compatibility mapping active so a phase-2 rollback can return the consumer to `display_name` without data loss.

Dependency: Phase 2 starts only after Phase 1 migration, backfill, dual-field behavior, and rollback checks pass. Removal of `display_name` is outside this task.

## Requirement-to-verification mapping

| Requirement | Planned check |
|---|---|
| Old clients remain supported | A `display_name` request/read still succeeds and returns the compatibility field after the migration. |
| New clients use `full_name` | A `full_name` request/read persists and returns the canonical value while the alias remains available. |
| Existing names are preserved | Migration test asserts every pre-existing `display_name` is copied to `full_name` unchanged. |
| Tenant isolation remains intact | `tests/test_service.py` continues to reject a matching `id` from another tenant, including mixed-field rows. |
| Safe rollback | Disable the new mapping or route the consumer to `display_name`; assert no column removal and no name loss. |

## Verification

Planned, not executed: run `make test` from `verification/scenarios/complex` after implementation; add migration/compatibility cases to the discovered test suite so backfill, old/new clients, mixed data, tenant isolation, and rollback are covered. No implementation or test changes were made by this planning run.

## Risks and decisions

- The schema currently requires `display_name`; adding `full_name` as nullable and backfilling before new consumption avoids breaking existing rows and avoids destructive removal.
- New write-normalization work can drift if it updates only one field; the compatibility layer must keep both fields aligned during the window.
- Tenant isolation is an existing safety property and must remain part of every new read/write path.
- No separate API consumer file exists in this fixture; phase 2 should attach to the consumer that calls the existing service seam rather than inventing an external integration.

## Proposed question (not asked in this synthetic run)

Approve creating the two phase folders and their linked phase plans before implementation begins? The plan is complete, but phase artifacts remain intentionally uncreated until that decision is made.

## Next action

Approve or reject the proposed two-phase structure; if approved, create the phase records and hand Phase 1 to `/si` under separate implementation authorization.
