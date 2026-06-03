---
name: ct
description: >-
  Use when a feature/scoped task is clear enough for technical planning —
  produces an implementation-ready technical decomposition before coding.
  Trigger: 'create task', 'technical decomposition', 'plan implementation',
  'break into implementation steps', or after /nf or /product when ready to
  plan the build. NOT for feature discovery (/nf), product docs (/product),
  brainstorming (/brainstorm), or implementation (/si).
argument-hint: [feature-name | task-name]
allowed-tools: Task, Skill, AskUserQuestion, Read, Glob, Grep, Edit, Write, Bash
---

# Create Task Command

> **Announcement**: Begin with: "I'm using the **ct** skill for technical task creation."

## Quick start
`/ct streak-freeze` → confirm scope (GATE 0) → discover inputs & explore the codebase (GATE 1–2) →
resolve ambiguity (GATE 3) → write `tech-decomposition-streak-freeze.md` (GATE 4) →
review + split evaluation (GATE 5–6) → next: `/si [task-dir]`.

## Objective
Create implementation-ready technical documentation that a developer can execute with confidence.
Work backward from expected behavior: clarify scope, inspect existing patterns, write the test plan
first, then derive implementation steps. Keep the plan concrete, traceable, and free of time estimates.

## Core principles
- **Test plan first** — define what proves the work is done before describing how to build it.
- **Clarify ambiguity before decomposition** — unresolved gray areas become bad plans.
- **Follow existing patterns** — extend proven structures before inventing new ones.
- **Protect scope** — new ideas become follow-ups, not stealth additions.
- **Discover repo conventions** — prefer searching the actual workspace over assuming fixed paths.
- **Stay executable** — name files, commands, dependencies, and completion signals explicitly.
- **Context is compacted automatically** — for long sessions, save the in-progress decomposition to
  disk as you go; don't stop early over token concerns.

## Workflow
Seven sequential gates. Each has an exit criterion — don't advance until it's met.

### GATE 0 — Confirm the task is ready for technical planning
- If no argument is provided, ask what task or feature to plan.
- Route away if not ready: still fuzzy/exploratory → `/nf` or `/brainstorm`; missing product framing
  (goals, business rules, success metrics) → `/product`; ready to build → continue.
- Ask enough to name: objective, primary actor/system touchpoint, success criteria,
  boundaries/out-of-scope, dependencies/constraints/non-negotiables.
- Exclude time estimates — this doc is a technical contract, not a schedule.
- **Exit:** the task is one clear implementation objective with known boundaries.

### GATE 1 — Discover source material and prior art
Search for inputs instead of assuming a repo layout; prefer existing doc conventions. Run these Glob
calls in one turn (they're independent):
- Discovery: `**/discovery-*.md`
- Product: `**/JTBD-*.md`, `**/PRD*.md`, `**/*requirements*.md`
- Architecture: `**/ADR*.md`, `**/*architecture*.md`, `**/*decision*.md`
- Existing plans: `**/tech-decomposition-*.md`, `**/*implementation-plan*.md`

Read the closest artifacts and extract: canonical task/feature name, requirements & success criteria,
constraints/blockers, open questions (`[NEEDS CLARIFICATION: ...]`), reusable plan patterns.
- **Glossary**: if `product-docs/UBIQUITOUS_LANGUAGE.md` exists, read it and use its canonical terms
  verbatim (module names, behaviors, acceptance criteria). Flag conflicts rather than inheriting drift.
- **Architecture vocab**: load `.claude/skills/architecture-language/LANGUAGE.md` before describing
  module changes — use **module / interface / seam / adapter / depth** exactly; don't drift into
  "component", "service", "API", or "boundary".
- **Output location**: prefer the repo's task-doc convention; else default to
  `tasks/task-YYYY-MM-DD-[feature-name]/tech-decomposition-[feature-name].md`.
- **Exit:** you know which inputs are authoritative and where the output doc lives.

### GATE 1.5 — Requirements quality & scope check
Review inputs like "unit tests for English" — validate the requirements themselves, not just their
feasibility, across: **Completeness** (major scenarios covered?), **Clarity** (one interpretation
only?), **Consistency** (docs/constraints don't contradict?), **Measurability** (success objectively
verifiable?), **Coverage** (errors, boundaries, permissions, edge cases defined?), **Gap** (what
behavior is still missing?).

If important gaps exist: summarize as 3–7 tagged checklist items and present with `AskUserQuestion` —
**Fix requirements first** (return to source docs) or **Proceed with explicit decisions/blockers**
(resolve what's resolvable, capture anything still blocking). Don't hide requirement gaps inside
implementation steps.
- **Exit:** gaps are resolved or explicitly captured as decisions/blockers.

### GATE 2 — Explore the codebase
Launch **2–3 Explore agents in a single turn** (fan out in the same batch — don't sequence), each with
a mandate:
1. **Architecture & patterns** — closest similar feature/module/workflow, relevant data models or
   persisted state, reusable shared abstractions/utilities/base patterns.
2. **Change surface** — files/dirs to modify; nearby API surfaces, contracts, background jobs, events,
   integrations; existing test files & patterns in the affected module.
3. **Risks & constraints** — likely failure modes & edge cases, config touchpoints, integration
   boundaries, dependencies that could break or need coordinated change.

If UI-heavy, also inspect: component composition patterns; state management & navigation conventions;
loading/empty/error/success/accessibility states; existing visual/system constraints. Optional: `/vp`
(or another design helper) when visual uncertainty blocks planning; include analytics coverage when the
change touches a tracked user-facing flow.

Return a short findings summary: existing patterns, likely files/dirs, integration points, constraints.
- **Exit:** the plan can be grounded in real codebase evidence, not guesses.

### GATE 3 — Resolve ambiguity before decomposition
Identify gray areas: multi-interpretation requirements, missing acceptance criteria/edge cases,
technical choices with multiple valid approaches, unclear current-vs-future boundaries. For each:
resolve from docs/code, ask the user when product/implementation judgment is needed, or mark as
blocker/prerequisite.
- **Glossary updates**: if a new domain term appears or needs sharpening, invoke `/ubiquitous-language`
  to update `product-docs/UBIQUITOUS_LANGUAGE.md` inline so `/si` and reviewers inherit it.
- Record non-trivial choices in the decomposition as a decision table (`# | Question | Decision |
  Rationale`).
- **Scope guardrail**: this gate clarifies HOW to implement what's already in scope — it does not
  expand the task. A new capability becomes a follow-up, not a fold-in.
- **Exit:** all meaningful ambiguities are resolved or marked as blockers. If an unresolved one would
  materially change implementation, the task is not ready for decomposition.

### GATE 4 — Write the technical decomposition
1. Read `.claude/docs/templates/technical-decomposition-template.md` — treat it as the **output
   contract** (defines structure & detail level; don't restate it inside the doc).
2. Follow **`references/decomposition-guide.md`** for the required sections, planning rules
   (Entity Lifecycle, Constraint-to-UI traceability, the `Must Haves` block) and the Given/When/Then
   test-case format.

Core rules to honor while writing:
- Define the **Test Plan before implementation steps**.
- Concrete files/dirs/modules per step, stating what it changes and what it proves.
- Assign `REQ-XXX` IDs when source requirements exist; otherwise write explicit plain-language
  requirements.
- Leave tracking fields (`Issue ID`, `Branch / PR`, `Split status`, `Completion Summary`) blank unless
  real — they're owned by `/si` and tracker integration.
- Exclude time estimates.
- **Exit:** a fresh developer could implement the task from the doc without a separate planning meeting.

### GATE 5 — Review and strengthen the plan
Self-check: does every must-have map to tests and steps? any scope creep? are blockers/constraints
explicit? does it follow repo patterns? is the test strategy sufficient for the change risk?

Required review by complexity:

| Complexity | Signal | Required review |
|------------|--------|-----------------|
| Simple | 1–2 focused steps | `plan-reviewer` agent |
| Medium | 3–5 steps, multiple touchpoints | `plan-reviewer` + `senior-architecture-reviewer` |
| Complex | 6+ steps, architecture/cross-system risk | `plan-reviewer` + `senior-architecture-reviewer` + cross-AI validation |

> Reviewer agents follow a coverage-then-filter pattern — surface every issue (severity + confidence),
> then filter in a separate pass. Don't instruct them to report "only important" findings; 4.7 obeys
> that literally and recall drops.

For **Complex** plans, cross-AI validation is part of the required path — follow
`.claude/docs/templates/cross-ai-protocol.md` if present. Optional adjuncts: `/analyze` when source
specs exist and traceability matters; sync a tracker issue if the project uses one. If review finds
gaps, revise (preserve known risks/blockers) and re-run the relevant review path.
- **Exit:** the plan is specific, scoped, and reviewable enough to evaluate splitting.

### GATE 6 — Task splitting evaluation
Invoke the `task-splitter` agent on the **finalized, reviewed** parent plan (provide the task-directory
path + the `tech-decomposition-[feature-name].md` path). It either:
- recommends **NO SPLIT** — keep the parent doc active and proceed to handoff, or
- creates `splitting-decision.md` — present the recommendation with `AskUserQuestion`.

If the user approves splitting: invoke `task-decomposer` with the task directory to create phase folders
and phase tech-decomposition docs aligned to the template, retain the parent as reference, update
`splitting-decision.md`, and hand off using the phase docs. If declined: keep the parent doc active and
proceed.
- **Exit:** the task is confirmed as a single implementation unit or decomposed into approved phases.

## Output
Create `tech-decomposition-[feature-name].md` in the repo's existing task-doc convention, or in the
fallback task directory if none exists. After GATE 6 the active output is either the parent
`tech-decomposition-[feature-name].md` or the phase-specific docs created by `task-decomposer`.

## Handoff
After the gates complete, present a concise summary:

```text
Task ready for implementation:
- Task: [task name]
- Doc: [path to active tech-decomposition or phase docs]
- Key decisions: [resolved / open]
- Traceability: [used / not applicable]
- Split status: [no split | split recommended but declined | phases created]
- Tracking: [optional issue link]

Next steps:
-> Start implementation: /si [task-directory or doc path]
```

## Flexibility notes
- Small changes: keep the doc lean but still include `Must Haves`, `Test Plan`, and concrete steps.
- Large features: keep one parent objective and split only when execution would otherwise be unsafe or
  vague.
- The decomposition core stays lightweight, but the required review path and the `task-splitter` /
  `task-decomposer` workflow are part of the standard completion path.
