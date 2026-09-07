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

## Quick start
`/ct streak-freeze` → confirm scope (GATE 0) → discover inputs & explore the codebase (GATE 1–2) →
resolve ambiguity (GATE 3) → update the active plan (GATE 4) →
review + split evaluation (GATE 5–6) → next: `/si [task-dir]`.

## Shared task context
Resolve the repository, task and linked artifacts with
[`../setup/references/task-context.md`](../setup/references/task-context.md) before the gates.
Reuse an explicit plan or task entrypoint; create the minimum `TASK.md` only when no matching
record exists. Update the record with the active plan, decisions, verification evidence and next
action before handing off to `/si`.

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
Use the gates in order, but skip branches whose evidence is already present in the resolved task.
Each active gate has an exit criterion.

### GATE 0 — Confirm the task is ready for technical planning
- If no argument is provided, use the shared resolver to reuse the task established in the
  conversation, issue or branch. Ask only when no candidate exists or more than one remains plausible.
- Route away if not ready: still fuzzy/exploratory → `/nf` or `/brainstorm`; missing product framing
  (goals, business rules, success metrics) → `/product`; ready to build → continue.
- Ask enough to name: objective, primary actor/system touchpoint, success criteria,
  boundaries/out-of-scope, dependencies/constraints/non-negotiables.
- Exclude time estimates — this doc is a technical contract, not a schedule.
- **Exit:** the task is one clear implementation objective with known boundaries.

### GATE 1 — Discover source material and prior art
Search the resolved task and its linked repository inputs instead of assuming a repo layout. Use
the repository's configured conventions and run independent searches together when supported:
- Discovery: `**/discovery-*.md`
- Product: `**/JTBD-*.md`, `**/PRD*.md`, `**/*requirements*.md`
- Architecture: `**/ADR*.md`, `**/*architecture*.md`, `**/*decision*.md`
- Existing plans: `**/tech-decomposition-*.md`, `**/*implementation-plan*.md`

Read the closest artifacts and extract: canonical task/feature name, requirements & success criteria,
constraints/blockers, open questions (`[NEEDS CLARIFICATION: ...]`), reusable plan patterns.
- **Glossary**: if `product-docs/UBIQUITOUS_LANGUAGE.md` exists, read it and use its canonical terms
  verbatim (module names, behaviors, acceptance criteria). Flag conflicts rather than inheriting drift.
- **Architecture vocab**: load `.claude/skills/architecture-language/LANGUAGE.md` before describing
  module changes. Use its terms for architectural guarantees, while retaining established project
  terms such as `service` or `API` when they name real project concepts; state the mapping when it
  matters.
- **Output location**: prefer the resolved task's existing plan entrypoint and repo convention;
  otherwise use `tasks/task-YYYY-MM-DD-[feature-name]/tech-decomposition-[feature-name].md` beside
  the minimum `TASK.md`.
- **Exit:** you know which inputs are authoritative and where the output doc lives.

### GATE 1.5 — Requirements quality & scope check
Review inputs like "unit tests for English" — validate the requirements themselves, not just their
feasibility, across: **Completeness** (major scenarios covered?), **Clarity** (one interpretation
only?), **Consistency** (docs/constraints don't contradict?), **Measurability** (success objectively
verifiable?), **Coverage** (errors, boundaries, permissions, edge cases defined?), **Gap** (what
behavior is still missing?).

If important gaps exist: summarize the material tagged checklist items and present with `AskUserQuestion` —
**Fix requirements first** (return to source docs) or **Proceed with explicit decisions/blockers**
(resolve what's resolvable, capture anything still blocking). Don't hide requirement gaps inside
implementation steps.
- **Exit:** gaps are resolved or explicitly captured as decisions/blockers.

### GATE 2 — Explore the codebase
Run the smallest scoped codebase pass that can ground the plan. When the host provides workers and
the mandates are independent, fan out in one batch; otherwise perform the same passes directly and
record the fallback. Cover as needed:
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

If the host cannot dispatch that role, perform the same three passes directly and record that fallback.
Return a short findings summary: existing patterns, likely files/dirs, integration points, constraints.
- **Exit:** the plan can be grounded in real codebase evidence, not guesses.

### GATE 3 — Resolve ambiguity before decomposition
Identify gray areas: multi-interpretation requirements, missing acceptance criteria/edge cases,
technical choices with multiple valid approaches, unclear current-vs-future boundaries. For each:
resolve from docs/code, ask the user when product/implementation judgment is needed, or mark as
blocker/prerequisite.
- **Glossary updates**: if a new domain term appears or needs sharpening, load it through
  `/ubiquitous-language`; write `product-docs/UBIQUITOUS_LANGUAGE.md` only when the caller authorized
  the update, then link the result so `/si` and reviewers inherit it.
- Record non-trivial choices in the decomposition as a decision table (`# | Question | Decision |
  Rationale`).
- **Scope guardrail**: this gate clarifies HOW to implement what's already in scope — it does not
  expand the task. A new capability becomes a follow-up, not a fold-in.
- **Exit:** all meaningful ambiguities are resolved or marked as blockers. If an unresolved one would
  materially change implementation, the task is not ready for decomposition.

### GATE 4 — Write the technical decomposition
1. If a separate technical plan is needed, read `.claude/docs/templates/technical-decomposition-template.md`
   and follow **`references/decomposition-guide.md`** for its structure. If the resolved task is
   small and its `TASK.md` already has an equivalent objective, acceptance/verification, decisions
   and implementation steps, extend that record instead of creating boilerplate.

Core rules to honor while writing:
- Define verification before implementation steps. A separate decomposition uses the template's
  **Test Plan**; a compact task may use equivalent acceptance and verification sections.
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

Choose review depth from evidence and risk, not a numeric step count:

| Risk signal | Evidence | Review |
|------------|----------|--------|
| Low | single bounded behavior, local change, clear tests | self-check or `plan-reviewer` when available |
| Material | multiple modules, migrations, permissions, or unclear contracts | `plan-reviewer` + plan-capable architecture pass |
| High | cross-system/irreversible change or unresolved critical risk | above + optional cross-AI validation |

Use reviewers that accept a plan and its supporting context. The repository's
`senior-architecture-reviewer` is defined for completed implementations and git-history checks;
do not dispatch it for this gate unless its input contract explicitly supports plan-only review. If
no plan-capable architecture reviewer is configured, perform that pass from the decomposition and
record the fallback; do not fabricate implementation evidence.

> Reviewers follow a coverage-then-filter pattern: surface every issue with severity and confidence,
> then filter in a separate pass. Keep low-confidence items labeled until verification; do not
> pre-filter during discovery.

For high-risk plans, use `.claude/docs/templates/cross-ai-protocol.md` if available. `/analyze` is
the traceability pass for source specs; run it once after the plan exists when traceability matters.
Use tracker sync only when requested and supported. If a review capability is unavailable, record
the skipped check and continue only when the remaining evidence supports the risk decision.
- **Exit:** the plan is specific, scoped, and reviewable enough to evaluate splitting.

### GATE 6 — Task splitting evaluation
Invoke the `task-splitter` agent only when the reviewed plan shows a safe functional or prerequisite
split; provide the resolved task-directory path and active plan path. It either:
- recommends **NO SPLIT** — keep the parent doc active and proceed to handoff, or
- creates `splitting-decision.md` — present the recommendation with `AskUserQuestion`.

If the user approves splitting: invoke `task-decomposer` with the task directory to create phase folders
and phase tech-decomposition docs aligned to the template, retain the parent as reference, update
`splitting-decision.md`, and hand off using the phase docs. If declined: keep the parent doc active and
proceed.
- **Exit:** the task is confirmed as a single implementation unit or decomposed into approved phases.

## Output
Create `tech-decomposition-[feature-name].md` only when the task's existing entrypoint cannot carry
the required technical detail or an existing consumer requires that file. Otherwise update the
resolved `TASK.md`/plan entrypoint. After GATE 6 the active output is the selected parent plan or
phase-specific docs created by `task-decomposer`; link it from the task record.

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
- Small changes: keep the resolved task record lean with objective, acceptance/verification,
  decisions and concrete steps; create a separate decomposition only when its detail or consumer
  requires it.
- Large features: keep one parent objective and split only when execution would otherwise be unsafe or
  vague.
- The decomposition core stays lightweight, but the required review path and the `task-splitter` /
  `task-decomposer` workflow are part of the standard completion path.
