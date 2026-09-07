# Product list CSV export

Objective: Define a greenfield export that lets an authorized operator download the current filtered product list as a UTF-8 CSV with the agreed product columns and empty-list behavior.
Stage / status: Discovery complete; ready for technical planning. Product implementation has not started.

## Context and decisions
- The repository README identifies this as a greenfield inventory product with no implementation yet.
- The supplied requirements are the product authority for this discovery.
- The selected direction is export of the operator's current filtered list, including the agreed columns and excluding user-hidden columns.
- The explicit product behavior is treated as settled. Open entry-point, authorization wiring, CSV serialization, and delivery details are deferred to technical planning.
- External research and cross-AI validation are intentionally skipped for this draft at the user's request.
- No product blockers remain. The supplied requirements settle the output columns and the rule that any user-hidden column is omitted.

## Artifacts
- [Discovery: product list CSV export](discovery-product-list-csv-export.md)

## Progress and next action
Discovery requirements and scope are documented. Next: resolve the listed technical-planning details during `/ct`.
