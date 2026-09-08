---
name: nf
description: >-
  Runs an in-depth feature-discovery interview that explores, challenges, and
  documents a new feature before planning. Use when asked to 'detail a feature',
  'explore a new feature', 'feature discovery', 'interview about feature', 'spec
  out a feature', 'design a feature', 'think through a feature', 'deep dive on a
  feature', 'discover [feature-name]', or 'what should we consider for
  [feature]'. NOT for quick brainstorming (/brainstorm), PRD/JTBD docs
  (/product), or implementation tasks (/ct).
argument-hint: [feature-description]
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Task, Skill
---

# New Feature Discovery

## Quick start
`/nf add streak freeze` → resolve and persist task → material questions → one grill →
`discovery-streak-freeze.md` in the resolved task → next: `/vp` or `/ct`.

## Shared task context
Before the interview, resolve the repository and task with
[`../setup/references/task-context.md`](../setup/references/task-context.md). Reuse an explicit or
linked task and its existing entrypoint. Create the minimum `TASK.md` only when no matching task
record exists; persist the discovery link, current status, evidence, and next action there.

## Objective
Turn a rough feature idea into a clear, standalone discovery document — the entry point for
anyone who later visualizes (`/vp`), plans (`/ct`), or implements (`/si`) the feature.

## Guidelines
- Treat explicit requirements and their direct consequences as settled. A specific
  exception already supplied by the user is not a new ambiguity to confirm.
  Apply a stated exception to its general rule. For each proposed or retained question,
  identify the decision the user has not supplied; otherwise record the resolved behavior
  and remove the obsolete question. Earlier draft markers do not override current input.
- Ask about material product choices; leave routine technical details for planning.
  Record unresolved questions with their impact, and identify which actually block the
  next stage. An unspecified implementation detail alone does not block discovery.
- Use `AskUserQuestion` for any unresolved clarification — structured options keep the interview auditable.
- If behavior is unclear (UX flow, edge cases, error handling, states), ask the user to define it rather than inferring — downstream `/vp` and `/ct` trust this doc as source of truth, so silent assumptions compound.
- Ask non-obvious, thought-provoking questions; challenge confident-but-underspecified answers by naming the gap ("You said X — does that cover case Y?").
- Offer alternatives only when they change scope or the chosen flow. Ask until the feature is
  sufficiently understood for the next stage; do not fill every optional template line by default.
- Keep the discovery template in mind throughout — gather exactly what's needed to fill it clearly.

**Context management.** This workflow runs long. On a compaction / context refresh: re-read already-created task files and the discovery template, then resume from the last unanswered section — do not restart. Don't stop early over token-budget worries; the parent harness handles compaction.

## Workflow

### Argument Validation
If no `[feature-description]` is provided, use the shared resolver to reuse the feature/task
established in the conversation, issue or branch. Ask "What feature would you like to explore?"
only when no candidate exists or more than one remains plausible; then derive the slug.

### Step 0 — Load Output Shape & Upstream Context
Read `.claude/docs/templates/discovery-template.md` first — it is the **output contract** (defines what the final doc contains). Don't duplicate its structure here; use the template as the source of truth for final shape.
Then load only matching upstream context, if present:
- `product-docs/PRD/PRD-*[feature-name]*.md` and `product-docs/JTBD/JTBD-*[feature-name]*.md` — product-level "what & why"; reference them in the discovery doc.
- `product-docs/UBIQUITOUS_LANGUAGE.md` — use its terms verbatim; flag conflicts with user wording immediately. If missing or new terms surface, propose canonical wording and update only after explicit authorization.

### Step 1 — Context Gathering & Design Exploration
Resolve or create the minimum task record now and save the feature objective, current status and
initial context before the interview. When the feature changes code, invoke `design-exploration`
only if codebase evidence affects the direction; otherwise record the product-level context. Ask
for correction only when the findings change scope or the chosen approach.

### Step 2 — External Research (if needed)
- **Quick lookups**: Exa MCP when the user asserts an external factual claim you can't verify from the codebase or prior turns. Skip for internal behavior (design-exploration covers it) or subjective preference.
- **In-depth**: spawn `comprehensive-researcher` only when the answer materially affects direction, scope, key requirements, or constraints. Ask for a concise **decision memo** (findings, implications for shape/scope, risks, unresolved unknowns) — not a broad report.

### Step 3 — Deep-Dive Questions
Drive the conversation toward the material template sections with **non-obvious** questions. Read
`references/interview-guide.md` as a question bank, selecting only questions that can change scope,
flow, acceptance or constraints. Ask once per material ambiguity, accept `skip / TBD`, and record
`[NEEDS CLARIFICATION: ...]`; do not re-confirm settled answers.

### Step 4 — "Grill Me" Challenge Round
Invoke the `/grill-me` skill to pressure-test design and clarity. Before invoking, summarize: feature name/description, why it exists, chosen direction, how it works, in / out scope, key requirements, known risks.
After grilling: incorporate findings; tighten wording, scope boundaries, hidden assumptions, missing states / edge cases.
**Glossary** (before writing): if new terms, synonym conflicts, or sharpened terms surfaced, load
`/ubiquitous-language`; update `product-docs/UBIQUITOUS_LANGUAGE.md` only when that update is
authorized, otherwise record the proposed canonical terms in the task context for a later update.
Record the grill summary, decisions and next action in the task context before writing.

### Completion Check
One pass (not a loop): verify each has a ≥ 1-sentence answer or an explicit marker — what is it? why exist? how works? in scope? out of scope? what constraints shape it? If ≤ 2 are weak, flag inline and proceed. If > 2 are missing, run one more question round; then write only with explicit markers for unresolved items, never blank required sections.

### Step 5 — Discovery Document Writing
1. Re-read `.claude/docs/templates/discovery-template.md` before writing.
2. Write `discovery-[feature-name].md` in the resolved task's existing convention. If no task entrypoint exists, use `tasks/task-YYYY-MM-DD-[feature-name]/` and create the minimum `TASK.md` first; do not create a second discovery document to fit the template.
3. If any required section is blank, continue discovery instead of finalizing; preserve explicit `[NEEDS CLARIFICATION: ...]` markers when the user accepted an unresolved question.
4. Present a summary for confirmation.

### Step 6 — Cross-AI Validation
Run cross-AI validation only when available and proportionate to the discovery risk, per
`.claude/docs/templates/cross-ai-protocol.md` — it is the single source of truth for the configured
validator set, availability fallback, comparison table, and verdict format. If a validator or
parallel worker is unavailable, record the exact skipped check; never present a skipped check as
passed.
- **FOCUS**: review as senior product analyst — entry-point readability, completeness, consistency, flow clarity, scope boundaries, feasibility, and hidden ambiguities that would confuse `/vp` or `/ct`.
- **FILE_REFS**: `discovery-[feature-name].md` + relevant codebase paths.
- **OUTPUT**: append "Cross-AI Validation: PASSED/FAILED" with consolidated verdict.

On failure → `AskUserQuestion`: "Revise discovery doc" / "Override and proceed" / "Abandon feature". **Skip** if no CLI available or the user opts out.

## Output
`discovery-[feature-name].md` in the resolved task's existing convention.

After writing, update the resolved task record with the discovery link, actual validation status,
unresolved markers and one next action. A validation skip is evidence of a skip, not a pass.

## Handoff — Next Steps
```
Discovery complete for [feature-name]:
- Document: [resolved task]/discovery-[feature-name].md

Next steps:
→ Visualize the design: /vp [feature-name]
→ Skip to tech planning: /ct [feature-name]
```
