---
name: quick
description: Apply a small change with known scope or a diagnosed bug fix using a compact task record. Use for quick fixes,
  configuration edits and bounded refactors; use /ct when the work needs unresolved design or coordinated implementation planning.
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep
- AskUserQuestion
- Skill
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/si-quick/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/si-quick/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Quick implementation

Use the [implementation contract](../si/SKILL.md) in compact mode. This entrypoint keeps
its short invocation; task resolution, TDD, evidence and authorization have one owner.

Resolve or create the task using [shared task context](../setup/references/task-context.md).
An existing task folder is valid input. Keep the objective, scope, short plan, relevant
checks and next action in its existing record; a new task needs only `TASK.md`.

Choose quick mode when the behavior and approach are known and the change is bounded.
File count alone does not decide complexity. If a formal plan already describes the
work, follow it. If new product decisions or coordinated dependencies appear, capture
them and use `/nf` or `/ct` for the missing work before proceeding.

Implement with the tests/validation appropriate to the change and record the observed
result in the same task. Preserve unrelated files and user edits. The requested fix can
finish locally without a commit or PR; perform later actions only when authorized.
Independent review remains available through `/sr` using the compact record.
