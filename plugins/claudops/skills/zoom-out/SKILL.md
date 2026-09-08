---
name: zoom-out
description: Step up one layer of abstraction and produce a map of the relevant modules and their callers — used when you
  (or the agent) are stuck in one file and losing the bigger picture. Use when user says "zoom out", "give me a map", "I'm
  lost in this code", or "what calls this".
disable-model-invocation: true
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/zoom-out/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/zoom-out/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.
> **Invocation guard:** use this as a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients may not enforce Claude Code host-level invocation restrictions.

# Zoom Out

> **Upstream**: Adapted from [mattpocock/skills/zoom-out](https://github.com/mattpocock/skills/blob/main/zoom-out/SKILL.md).

Step out of the current file. Go up one layer of abstraction. Produce a compact map of:

- The **modules** in this area (use `architecture-language/LANGUAGE.md` vocabulary)
- Their **callers** — who reaches into this code and from where
- Their **dependencies** — what this code reaches into

Do not propose changes. Do not deep-dive into any one module. The point is to recover bearings, not to solve a problem.

If this supports an active task, use [`../setup/references/task-context.md`](../setup/references/task-context.md)
to read the selected task's relevant links. Do not create a task or artifact for a standalone map.

If `product-docs/UBIQUITOUS_LANGUAGE.md` exists, name modules using its terms when possible.
