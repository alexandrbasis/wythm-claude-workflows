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

> **Announcement**: Begin with: "I'm using the **nf** skill for feature discovery."

## Quick start
`/nf add streak freeze` → interview (design exploration → deep-dive → grill → validate) →
`tasks/task-YYYY-MM-DD-streak-freeze/discovery-streak-freeze.md` → next: `/vp` or `/ct`.

## Objective
Turn a rough feature idea into a clear, standalone discovery document — the entry point for
anyone who later visualizes (`/vp`), plans (`/ct`), or implements (`/si`) the feature.

## Guidelines
- Use `AskUserQuestion` for any unresolved clarification — structured options keep the interview auditable.
- If behavior is unclear (UX flow, edge cases, error handling, states), ask the user to define it rather than inferring — downstream `/vp` and `/ct` trust this doc as source of truth, so silent assumptions compound.
- Ask non-obvious, thought-provoking questions; challenge confident-but-underspecified answers by naming the gap ("You said X — does that cover case Y?").
- Offer alternatives, shortcuts, and "go deeper" paths. Continue until the feature is fully understood.
- Keep the discovery template in mind throughout — gather exactly what's needed to fill it clearly.

**Context management.** This workflow runs long. On a compaction / context refresh: re-read already-created task files and the discovery template, then resume from the last unanswered section — do not restart. Don't stop early over token-budget worries; the parent harness handles compaction.

## Workflow

### Argument Validation
If no `[feature-description]` is provided, `AskUserQuestion`: "What feature would you like to explore?" (include a free-text option). Derive the feature-name slug from the answer.

### Step 0 — Load Output Shape & Upstream Context
Read `.claude/docs/templates/discovery-template.md` first — it is the **output contract** (defines what the final doc contains). Don't duplicate its structure here; use the template as the source of truth for final shape.
Then load only matching upstream context, if present:
- `product-docs/PRD/PRD-*[feature-name]*.md` and `product-docs/JTBD/JTBD-*[feature-name]*.md` — product-level "what & why"; reference them in the discovery doc.
- `product-docs/UBIQUITOUS_LANGUAGE.md` — use its terms verbatim; flag conflicts with user wording immediately. If missing or new terms surface, plan to invoke `/ubiquitous-language` at the Step 4 → 5 transition.

### Step 1 — Context Gathering & Design Exploration
When the feature will change or extend this project's code, invoke the `design-exploration` skill to ground discovery in the real codebase. Ask it for: key codebase findings & current fit, viable design directions, constraints, and risk flags. For a greenfield or product-only feature, record that no codebase fit was available and focus on the user's context. Prefer fit / options / constraints / risks over implementation decomposition.
**Checkpoint** — `AskUserQuestion`: "Does this direction look right?" → "Continue with this approach" / "Explore a different direction" / "I have corrections".

### Step 2 — External Research (if needed)
- **Quick lookups**: Exa MCP when the user asserts an external factual claim you can't verify from the codebase or prior turns. Skip for internal behavior (design-exploration covers it) or subjective preference.
- **In-depth**: spawn `comprehensive-researcher` only when the answer materially affects direction, scope, key requirements, or constraints. Ask for a concise **decision memo** (findings, implications for shape/scope, risks, unresolved unknowns) — not a broad report.

### Step 3 — Deep-Dive Questions
Drive the conversation toward the template sections with **non-obvious** questions. **Read `references/interview-guide.md` now** — it holds the full question bank (Overview, Usage Context, Chosen Direction, How It Works, Scope, Requirements, and Post-Action / Cross-Surface behavior).
Stop when every template section has either a user-confirmed answer or an explicit `[NEEDS CLARIFICATION: ...]` marker — don't re-confirm. For sections that need speculation, ask once, accept "skip / TBD", and mark the unresolved question. The draft needn't be perfect before writing — the grill round catches real gaps.

### Step 4 — "Grill Me" Challenge Round
Invoke the `/grill-me` skill to pressure-test design and clarity. Before invoking, summarize: feature name/description, why it exists, chosen direction, how it works, in / out scope, key requirements, known risks.
After grilling: incorporate findings; tighten wording, scope boundaries, hidden assumptions, missing states / edge cases.
**Update glossary** (before writing): if new terms, synonym conflicts, or sharpened terms surfaced, invoke `/ubiquitous-language` to update `product-docs/UBIQUITOUS_LANGUAGE.md` so downstream `/vp`, `/ct`, `/si` inherit the vocabulary.
**Checkpoint** — `AskUserQuestion`: "Proceed to discovery document" / "Revisit design based on findings" / "Cut scope based on grill findings".

### Completion Check
One pass (not a loop): verify each has a ≥ 1-sentence answer or an explicit marker — what is it? why exist? how works? in scope? out of scope? what constraints shape it? If ≤ 2 are weak, flag inline and proceed. If > 2 are missing, run one more question round; then write only with explicit markers for unresolved items, never blank required sections.

### Step 5 — Discovery Document Writing
1. Re-read `.claude/docs/templates/discovery-template.md` (long interviews drift; re-reading prevents section/heading mismatches that `/vp` and `/ct` parsers depend on).
2. Create `tasks/task-YYYY-MM-DD-[feature-name]/` and write `discovery-[feature-name].md` by filling the template with resolved decisions, flows, scope, requirements, and constraints. (Writing the file creates the task directory.)
3. If any required section is blank, continue discovery instead of finalizing; preserve explicit `[NEEDS CLARIFICATION: ...]` markers when the user accepted an unresolved question.
4. Present a summary for confirmation.

### Step 6 — Cross-AI Validation
Run cross-AI validation per `.claude/docs/templates/cross-ai-protocol.md` — it is the single source of truth for the **configured validator set**, availability fallback, comparison table, and verdict format. Initialize each validator's CLI skill **sequentially first** (they mutate runtime state), then **dispatch all reviews in parallel** in a single turn.
- **FOCUS**: review as senior product analyst — entry-point readability, completeness, consistency, flow clarity, scope boundaries, feasibility, and hidden ambiguities that would confuse `/vp` or `/ct`.
- **FILE_REFS**: `discovery-[feature-name].md` + relevant codebase paths.
- **OUTPUT**: append "Cross-AI Validation: PASSED/FAILED" with consolidated verdict.

On failure → `AskUserQuestion`: "Revise discovery doc" / "Override and proceed" / "Abandon feature". **Skip** if no CLI available or the user opts out.

## Output
`tasks/task-YYYY-MM-DD-[feature-name]/discovery-[feature-name].md`

## Handoff — Next Steps
```
Discovery complete for [feature-name]:
- Document: tasks/task-YYYY-MM-DD-[feature-name]/discovery-[feature-name].md

Next steps:
→ Visualize the design: /vp [feature-name]
→ Skip to tech planning: /ct [feature-name]
```
