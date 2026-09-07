> Optional scaffold for a separate technical plan. A compact plan in the existing task
> record is equally valid. Keep equivalent repository headings and omit irrelevant sections.
> Resolve resources and the task through `.claude/skills/setup/references/task-context.md`.

# Technical plan: [Task name]

**Planning status:** [Draft | Ready | Blocked]
**Task record:** [Link to existing task entrypoint]
**Inputs:** [Only the discovery, requirements, prototype or decisions this plan uses]

## Outcome and approach

[Link the agreed outcome and boundaries. Explain the approach, affected modules/files,
and consequential choices with their reasons. Identify new files as proposed paths.]

## Acceptance and verification

[Use the existing acceptance list, or record the observable criteria here. Reuse source
IDs when available. Keep one mapping from required behavior to its planned check; a
table is optional. Link source requirements instead of repeating them in a second list.]

| Criterion or source reference | Planned verification |
|-------------------------------|----------------------|
| [Required behavior] | [Behavior test, integration check or suitable manual check] |

**Commands and working directories:**

```text
[Actual command from project configuration / CI, and its owning workspace]
```

These checks are planned, not evidence of execution. Cover applicable error paths,
boundaries and affected surfaces. Expand a scenario to Given/When/Then only when useful.

## Implementation steps

- [ ] [Concrete change; affected files/modules; acceptance criterion it satisfies]
- [ ] [Next change; real dependency on the previous step, if any]

[Reuse the acceptance references above. For genuinely independent work, annotate its
ownership and ordering constraints only when parallel execution is intended.]

## Material risks and decisions

[Only relevant dependencies, unresolved blockers and decisions. For migrations,
permissions or external contracts, include compatibility, failure handling and a safe
rollout/recovery approach. Entity changes include applicable defaults and visibility.]

## Phase context (when split)

**Parent / active phase:** [Links]
**Depends on / enables:** [Phase links and provided or consumed contracts]

[Each phase produces a verifiable outcome or concrete prerequisite with a real consumer.
Preserve coverage across phases; completing one phase does not complete the parent.]

> During implementation, use `/si` within the authorized scope. Update progress and actual
> verification in the task's existing record; retain this plan and its links as the input.
