# `/ct` — Decomposition Writing Guide

Reference for **GATE 4** of the `ct` skill. Load this once you reach GATE 4 and are ready to write
`tech-decomposition-[feature-name].md`. Drive the document toward the structure of
`.claude/docs/templates/technical-decomposition-template.md` — that template is the **output
contract**; this guide is the *how-to-fill-it* detail. Use the subsets that apply; skip what doesn't.

## Output shape

- Read `.claude/docs/templates/technical-decomposition-template.md` before drafting.
- Treat it as the output contract: it defines the expected structure and level of detail; the
  decomposition should contain exactly what's needed to fill it clearly.
- Do **not** restate the template inside the document — use it as the source of truth for final shape.

## Required sections

- Linked Inputs / Context
- Primary Objective
- Must Haves
- Test Plan
- Technical Requirements
- Implementation Decisions (if any)
- Implementation Steps
- Dependencies / Risks / Blockers
- Tracking / Notes (optional)

## Planning rules

- **Entity Lifecycle** — when the task creates, updates, or deletes entities, add a
  `## Entity Lifecycle` section covering:
  - Creation entry points: where can the entity be created?
  - Persistence defaults: which fields must be set, including semantic defaults (category, type,
    order, visibility)?
  - Immediate feedback: what confirms success to the user?
  - Canonical visibility: where should the entity appear after creation?
  - Cross-surface visibility: what other pages, lists, widgets, searches, or groupings must reflect it?
  - Data normalization: should existing misclassified or orphaned entities be migrated?
- **Constraint-to-UI traceability** — for every service-layer validation rule in the spec, require a
  mapped UI element (error message, disabled/hidden option, input hint, or highlighted field). If a
  validation rule has no corresponding UI affordance, flag it as a gap.
- **`Must Haves` block** — add it immediately after the objective:
  ```markdown
  ## Must Haves
  Non-negotiable truths when this task is complete:
  - [ ] [Observable behavior 1]
  - [ ] [Interface, file, endpoint, or workflow truth 2]
  - [ ] [Constraint or invariant 3]
  ```
  These become the source of truth for goal-backward verification during implementation if that
  workflow exists.
- **Test Plan before implementation steps** — always.
- **Don't restate discovery/product docs** — if discovery or product docs exist, do not restate
  `Feature Overview`, `Why This Exists`, `How It Works`, or scope sections in full. Translate them
  into `Must Haves`, `Technical Requirements`, `Implementation Decisions`, and `Implementation Steps`.
- Include explicit **verification commands**.
- Treat `Technical Requirements` as the implementation-facing version of the source requirements.
- Use `Implementation Decisions` only for real technical choices, resolved gray areas, or explicit
  trade-offs. If none were needed, write `No additional implementation decisions required.`
- Break work into clear **steps and sub-steps** with concrete files, directories, or modules. State
  what each step changes and what it proves.
- If source requirements exist, assign `REQ-XXX` IDs and tag the relevant steps. If no formal
  requirements doc exists, still write explicit requirement statements in plain language.
- Add optional **wave annotations** only when steps are genuinely independent.
- Reference constraints or architecture decisions that shaped the plan.
- Leave `Issue ID`, `Branch / PR`, `Split status`, and `Completion Summary` blank or omitted unless
  prior workflow steps produced real values — those fields are owned by later skills (`/si`, tracker
  integration) and must reflect reality.
- **Exclude time estimates** — this doc is a technical contract, not a schedule; estimates expire fast
  and mislead consumers of the doc.

## Test case format (Given/When/Then)

- **Given**: preconditions already in place
- **When**: the action being exercised
- **Then**: the observable outcome that proves the behavior
- Prefer declarative behavior descriptions over click-by-click UI scripts.
