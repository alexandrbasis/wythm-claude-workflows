---
name: analyze
description: >-
  Compare a task's discovery or product requirements with its tech decomposition and
  report traceability gaps. Use when asked to 'analyze consistency', 'check alignment',
  'verify spec matches plan', 'traceability check', 'spec drift', 'are my docs aligned',
  or after /ct completes to verify the plan covers the requirements. `/ct` may invoke this
  check when traceability is material; otherwise it remains an explicit read-only command.
  NOT for code review (use /sr), NOT for code analysis (use /code-analysis),
  NOT for debugging (use /dbg).
argument-hint: [task-directory]
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Analyze: Cross-Artifact Consistency Check

## Purpose

Verify that the active plan OUTPUT of `/ct` is aligned with the source requirements (discovery/JTBD/PRD
docs or clearly separated requirement sections in the task record). Catch drift between what was
specified and what was planned before implementation begins.

**This skill is read-only.** It reads and reports — no file writes, no agents, no code changes.

Resolve the task and linked artifacts with
[`../setup/references/task-context.md`](../setup/references/task-context.md). Inspect only the
selected task's entrypoint and its linked sources; do not select a task by recency alone.

---

## Step 1: Locate Artifacts

Find the task directory and its documents:

1. **If argument provided**: resolve it through the shared task contract, then inspect the matching
   task/plan.
2. **If no argument**: reuse the task established in the conversation, issue or branch; ask only
   when no candidate exists or more than one remains plausible.

**Required inputs** (at least one distinguishable source of requirements + one active plan):

| Type | Files to look for |
|------|-------------------|
| **Spec** (input) | `discovery-*.md`, `JTBD-*.md` in the task directory; linked PRD/JTBD paths, conventionally `product-docs/PRD/` and `product-docs/JTBD/`; or clearly labeled requirements, scope and acceptance sections in the selected task entrypoint |
| **Plan** (output) | The active plan section in the selected task entrypoint, a separate technical-plan document, or `tech-decomposition-*.md` / `phase-*/tech-decomposition-*.md` when those exist |

**If no distinguishable source requirements are present**: Report "No spec documents or source
requirements found — cannot verify alignment." Verdict: `SKIPPED`.

**If no active plan is present**: Report "No active plan found — run /ct first." Verdict: `SKIPPED`.

When requirements and plan sections share one `TASK.md`, use the headings, links or explicit labels
to distinguish source requirements/acceptance from the plan's changes, steps and verification. Do not
require a second document or a fixed `tech-decomposition-[feature].md` filename.

When an argument identifies a task, prefer documents matching that task and feature name;
do not load unrelated PRDs or JTBDs merely because they exist elsewhere in the repository.

---

## Step 2: Extract Requirements

Read the source documents and clearly labeled source sections in the selected task entrypoint. Extract
a numbered list of requirements:

- From **discovery docs**: walk every top-level heading. Extract requirements from `How It Works`, `In Scope`, `Key Requirements`, `Constraints` (and their older equivalents: Functional/Non-Functional Requirements, UI/UX Specifications, acceptance scenarios). For any heading you are unsure about, include it in a `[UNCERTAIN-SOURCE]` note rather than skipping.
- From **JTBD docs**: Core Needs, Desired Outcomes
- From **PRD docs**: Functional Requirements, User Stories, Acceptance Criteria
- From a **task entrypoint**: source requirements, agreed scope, acceptance criteria and constraints
  when they are distinguishable from the active plan sections

Preserve existing requirement IDs. When a source has no IDs, use analysis-local labels such as
`REQ-A1` for the matrix; do not require the plan to add generated IDs or traceability tags.

**Also extract** any `[NEEDS CLARIFICATION: ...]` markers and explicitly unresolved blockers or
open decisions written in plain language, including the plan's risks and decisions. Classify each
before assigning severity: an unresolved choice about behavior, scope, an external contract or safety is material and
blocks alignment; a routine technical choice may remain a planning detail and does not automatically
block the verdict.

---

## Step 3: Extract Test Cases

Read the active plan's verification, acceptance-to-check mapping, test or command sections wherever
they appear. Extract behavior tests, integration checks and suitable manual checks with their
Given/When/Then definitions when present. A `Test Plan` heading is optional.

Preserve existing test IDs and names. When a check has no ID, use an analysis-local label such as
`CHECK-1`; do not require generated `TEST-XXX` identifiers.

---

## Step 4: Extract Implementation Steps

Read the active plan's implementation steps or equivalent change list wherever recorded. Extract all
steps and sub-steps, including their affected files/modules and dependencies.

Note existing source tags when present, but also map steps by semantic coverage of the source
requirements. Missing tags are not a gap by themselves.

---

## Step 5: Build Traceability Matrix

Map the three dimensions:

```
Source requirement (existing ID or analysis-local label) → Verification check → Implementation step
```

For each requirement, determine:
- Does at least one suitable verification check cover this requirement's observable behavior?
- Does at least one implementation step fulfill this requirement, or is the reason it is planning-only
  clear?

For each implementation step, determine:
- Does it trace back to a requirement, either by an existing tag or by covering one or more sub-clauses
  semantically? If it only covers part of a requirement, flag the uncovered portion as a separate
  `[UNCOVERED]` finding for that sub-clause.
- If it changes behavior, does it have suitable verification? Routine technical steps may be covered
  by the plan's broader checks and do not each need a separate test case.

---

## Step 6: Flag Gaps (coverage pass)

Report every gap you find, including low-signal ones. Do not suppress findings based on severity at this stage — a separate verification step will filter. Annotate each finding with a tag and a severity guess:

| Tag | Meaning | Default severity |
|-----|---------|----------|
| `[UNCOVERED]` | Required behavior has no suitable verification or only part of it is verified | Major |
| `[UNTESTED]` | A behavior-changing step has no suitable verification | Minor |
| `[SCOPE CREEP]` | A behavior-changing step maps to no source requirement; routine technical planning detail is not scope creep | Major |
| `[CONFLICT]` | Requirement contradicts a tech decision or another requirement | Critical |
| `[UNRESOLVED]` | Material behavior, scope, contract or safety decision remains unresolved | Critical |
| `[PLANNING DETAIL]` | Routine technical choice is marked for follow-up but does not change required behavior | Minor |

## Step 6a: Verdict (filter pass)

Apply severity gating only when computing the final verdict, not when collecting findings.
An unresolved material decision blocks `ALIGNED`; a routine technical choice may be reported as
`[PLANNING DETAIL]` without blocking the analysis.

---

## Step 7: Report & Verdict

Present the report to the user:

```markdown
## Consistency Analysis: [Task Name]

### Traceability Matrix

| Source | Description | Verification | Step | Status |
|--------|-------------|--------------|------|--------|
| REQ-001 or REQ-A1 | [brief] | CHECK-1 or named check | Step 1.1 | Covered |
| REQ-002 or REQ-A2 | [brief] | — | Step 2.1 | [UNCOVERED] |
| REQ-003 or REQ-A3 | [brief] | CHECK-3 or named check | — | [UNCOVERED] |
| — | — | — | Step 3.1 | [SCOPE CREEP] |

### Findings

- [UNCOVERED] REQ-A2 "User can delete session" — no suitable verification covers this requirement
- [SCOPE CREEP] Step 3.1 "Add caching layer" — no requirement references caching

### Verdict: ALIGNED | GAPS FOUND ([N] issues)

**Critical**: [count] | **Major**: [count] | **Minor**: [count]
```

**Verdict rules**:
- **ALIGNED**: 0 Critical, 0 Major gaps
- **GAPS FOUND**: Any Critical or Major gaps exist

**If GAPS FOUND**: Ask user via `AskUserQuestion`:
- **Fix gaps** — go back and update the active plan
- **Acknowledge and proceed** — gaps are intentional or will be addressed later
- **Re-run /nf** — spec docs need revision first

Complete the read-only matrix, findings, counts, and verdict before asking this question.
The user's choice is a follow-up decision; it does not authorize this skill to edit the
specification or plan.

---

## Related Skills

| Need | Use |
|------|-----|
| Create the tech decomposition | `/ct` |
| Feature discovery | `/nf` |
| Code review (post-implementation) | `/sr` |
| Implementation | `/si` |
