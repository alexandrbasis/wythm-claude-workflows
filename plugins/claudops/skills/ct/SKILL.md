---
name: ct
description: Plan implementation for a sufficiently clear feature or scoped task, including after /nf or /product. Use for
  'create task', 'plan implementation', or 'technical decomposition'. Save a concise, executable plan in the existing task;
  use /nf for unresolved feature discovery and /si for implementation.
argument-hint:
- task-path | feature-name
allowed-tools: Task, Skill, AskUserQuestion, Read, Glob, Grep, Edit, Write, Bash
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/ct/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/ct/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Plan implementation

Turn the agreed outcome into a plan that a fresh implementer can use. The normal
output is a short section of the existing task record. Depth follows the work,
not a fixed document schema.

## 1. Read the task and relevant code

Resolve the task with [shared task context](../setup/references/task-context.md).
Read its agreed scope, decisions and relevant linked discovery, product or prototype
artifacts. Reuse an existing plan; create the minimum record when no task exists.

Inspect the affected code, closest existing pattern and test/command sources. Reuse
upstream findings that still match the current code and requirements; investigate only
missing or changed evidence. Product documents and a separate discovery interview are
not prerequisites when the requested behavior and boundaries are already clear.

## 2. Choose the approach and resolve material gaps

Choose routine technical details from repository patterns and constraints. Record
consequential choices with a short reason. Ask the user only when an unresolved choice
materially changes behavior, scope, an external contract, or the safety/reversibility
of the work and cannot be settled from the supplied decisions or repository evidence.

Keep settled answers settled. Raise new product ideas as follow-ups. Save a genuine
blocker and its impact; continue independent planning where possible, but mark the
plan ready only when the missing decision no longer blocks implementation. Use /nf
when the objective needs actual discovery, not merely because a template field is empty.

## 3. Save the smallest executable plan

Define verification before deriving the steps, following the project's testing strategy.
Update the task's existing plan section with:

- **Changes:** the chosen approach and affected files/modules, linked to the agreed outcome.
- **Steps:** concrete actions in dependency order; identify new files as proposed paths.
- **Verification:** how each required behavior will be checked, using the project's
  actual commands and working directories. Distinguish planned checks from executed results.
- **Risks and decisions:** only material constraints, unresolved blockers and trade-offs.

Reuse acceptance criteria and source IDs where they exist. Connect requirements to
steps and checks in this one plan; plain-language references are enough. A separate
REQ/TEST matrix or Given/When/Then catalogue is useful only when it makes complex
coverage easier to assess. Preserve existing documents and their terminology.

For migrations, permissions, cross-system contracts, difficult coverage or phased
delivery, read [detailed planning](references/decomposition-guide.md) and add the
applicable detail. A separate decomposition is warranted when it needs independent
review, no longer fits the task record clearly, or an existing consumer requires it.
The detailed template is optional for other tasks.

## 4. Check readiness and hand off

Make one final check: the plan covers the agreed outcome, follows inspected code,
orders dependencies correctly, has suitable verification, and exposes real blockers.
Correct gaps in place. Independent review and splitting follow the detailed guide
only when justified by risk or explicitly requested; a routine plan needs neither.

Update the task's existing current status and next action in place; retain old states
only as dated history. Link the active plan section or file. Report the plan location
and any material open decision. Hand a ready plan to
`/si [task-path]`; continue implementation when that scope is already authorized. Planning readiness
does not claim that tests ran or that a prototype, split or implementation was approved.
