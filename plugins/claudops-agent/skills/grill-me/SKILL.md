---
name: grill-me
description: Use when a plan, design, or discovery document needs stress-testing for hidden assumptions, scope gaps, unresolved
  branches, or ambiguous wording; also when the user explicitly says "grill me".
compatibility: Portable clients may not enforce Claude Code invocation guards or project setup behavior.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/grill-me/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/grill-me/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Grill Me

Pressure-test a plan or design until the remaining ambiguity is explicit, bounded, and easy to communicate.

For task work, resolve the reviewed artifact with
[`../setup/references/task-context.md`](../setup/references/task-context.md). Read the linked
entrypoint and relevant sections only; return the compact decision summary to the caller, which
owns any durable task update.

## Core Behavior

- First, enumerate every candidate risk you can see across all categories
  below (scope, states/flows, assumptions, wording, decision branches) — keep
  this internal list so nothing drops silently. A later step filters to what
  is worth asking.
- Then surface one focused question at a time, ordered by what most changes
  the feature shape if answered wrong — the user must be able to answer
  without re-reading the whole thread; batched questions get half-answered
  or ignored.
- For each question, provide your recommended answer or default position.
- If a question can be answered from the codebase or docs, explore there
  instead of asking the user.
- Prefer exposing hidden assumptions over inventing extra scope — the goal
  is to sharpen an existing plan, not to bolt on new features under the
  guise of stress-testing.

## Adversarial Discipline

- When you offer a recommended answer, first spend one beat trying to **disprove** it. Confirmation is the failure mode — a default you only defended is weaker than one you tried to break.
- **Bound the loop.** If two consecutive rounds surface only minor or already-considered points, stop and report — continuing is grill theater (motion without new information), not rigor.
- For a high-stakes or irreversible decision, offer the user a **fresh-context adversarial check**: a subagent prompted to *find what's wrong*, given the artifact and its constraints — **not** your preferred answer. Handing over your conclusion biases the reviewer toward agreement. Never invoke an external CLI for this without explicit user authorization.

## When Invoked From Discovery

Scan every section of the discovery document (scope, flows, states,
constraints, out-of-scope, open questions, risks) — not only the first
section or headline. Then prioritize:

- Unclear scope boundaries
- Missing states, flows, or edge cases
- Hidden assumptions
- Ambiguous wording a new reader could misinterpret
- Decision branches that materially change the feature shape

Avoid:
- Deep implementation detail unless it changes scope, user experience, risk, or constraints
- Speculative product expansion that should instead be captured as out of scope

## Stop Condition

Stop when:
- The main branches of the decision tree are resolved or explicitly cut
- The remaining ambiguity is minor and non-blocking
- The caller can clearly document flow, scope, constraints, and risks

## Return To Caller

When the stop condition is met, finish by returning this compact summary
(so the caller — typically `/nf` or `/ct` — can paste it into the doc
without editing):

- Clarifications made
- Scope cuts or out-of-scope decisions
- Hidden assumptions uncovered
- Wording fixes or ambiguity reductions
- Remaining risks or blockers

Return this summary after the stop condition is met. Keep the review read-only unless the
caller explicitly authorizes editing the reviewed artifact; a recommendation or a completed
question round is not itself permission to change the plan.
