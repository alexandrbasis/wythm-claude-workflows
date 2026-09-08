---
name: si
description: Implement or resume a task from its existing plan and acceptance criteria, with behavior-first tests and recorded
  verification. Use for requested implementation; unresolved discovery belongs to /nf, planning to /ct, and independent review
  to /sr.
argument-hint:
- task-path | technical-plan-path
allowed-tools:
- Agent
- AskUserQuestion
- Edit
- Read
- Write
- Bash
- Glob
- Grep
- Skill
- TodoWrite
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/si/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/si/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Implement a task

Deliver the agreed outcome and leave verified progress that a person or fresh agent can
resume. A short plan in the existing task record is sufficient when the work is clear.

## 1. Read the active task and current state

Resolve the task with [shared task context](../setup/references/task-context.md), following
its active plan or selected phase. Create the minimum record only when none exists.
Read the agreed behavior, constraints, decisions, unfinished steps and relevant code/tests.
Reuse findings that still match the code; inspect what is missing or changed.

Fill structural gaps from the authorized request and repository evidence. Missing headings
or a particular decomposition filename are not blockers. Resolve questions that materially
change scope, behavior, contracts or safety before dependent implementation; continue
independent work. Use /nf or /ct only when actual discovery or planning is needed.

Inspect the working tree and preserve unrelated changes. Keep the selected checkout unless
isolation helps. Reuse authorization for the same operations and scope; implementation alone
does not authorize publication or tracker writes. Record the task as in progress using its
existing status vocabulary.

## 2. Implement in verified slices

For behavior changes, follow [TDD](../tdd/SKILL.md): observe a test fail for the intended
reason, implement that behavior, then refactor within scope. Use the agreed testing strategy
and real repository commands. Documentation, formatting and other non-behavior changes use
appropriate validation. On resume, check current code and evidence; preserve existing work
and report missing test chronology instead of rewriting history to manufacture RED.

Implement the full agreed scope in dependency order. Resolve routine technical choices from
repository patterns and domain terms. Record consequential deviations and their rationale
once in the existing task; obtain a decision for changes to agreed scope or acceptance.

For behavior that mutates application data or involves async interactions, read
[mutation and async checks](references/implementation-checklists.md). For enumerated,
visual or cross-surface requirements, read [verification recipes](references/verification-gate.md).
Read the references that apply, using their checks for the behavior the task requires.

When independent work has disjoint ownership and delegation offers a useful benefit, use
[parallelization](../parallelization/SKILL.md). Otherwise work directly. The orchestrator owns
shared task updates and verifies the combined result.

After each meaningful slice, update its existing acceptance/checklist entry with observed
evidence and the next unfinished action. If no entry exists, add a compact note in the task's
plan or progress section. Keep one mapping; existing IDs and plain-language
acceptance are both valid. Save progress before a pause so resume starts from these facts.

## 3. Verify the complete change

Remove residue introduced by this task and run applicable project checks from their owning
packages. Record command, working directory, result and the relevant revision or artifact.
Reuse evidence only while the affected code and inputs remain unchanged; rerun affected
checks after edits, cleanup or integration. A skipped or blocked check is not a pass.

Compare every agreed acceptance item with observed evidence, including required integration
or visible behavior. Code presence alone is insufficient proof of an outcome. Resolve failures
and missing required checks before claiming implementation complete; a partial result may
be handed over as a draft with its blockers named.

## 4. Save status and hand off

Update the existing current status and next action in place, with links to code, verification,
material deviations and remaining work. Keep old states as history. A separate completion
report is unnecessary when these facts already exist; a finished phase leaves its parent open
until the remaining phases are complete. Preserve links to completed phases, distinguish
pending work from the selected phase, and advance only within the authorized scope.

When review is requested or required, hand /sr the active task and actual diff/commit/PR target;
a local diff is valid input. Continue already authorized review or delivery, read back actions
you claim, and distinguish implementation, review, merge and deployment in the final result.
