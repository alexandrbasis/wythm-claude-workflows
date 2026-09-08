---
name: architecture-language
description: Canonical architectural vocabulary — module, interface, seam, adapter, depth, leverage, locality. Use when reviewing
  architecture, deepening shallow modules, designing interfaces, or evaluating refactor candidates. NOT a domain glossary
  (use /ubiquitous-language for that). Use as a standalone skill only when explicitly requested by the user; automatic selection
  is not authorization. Portable clients may not enforce this host-level restriction.
metadata:
  claude_disable_model_invocation: 'true'
  invocation_guard: explicit-only; portable clients may not enforce Claude Code host-level invocation restrictions
compatibility: Portable clients may not enforce Claude Code invocation guards or project setup behavior.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/architecture-language/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/architecture-language/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.
> **Invocation guard:** use this as a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients may not enforce Claude Code host-level invocation restrictions.

# Architecture Language

Shared vocabulary for architectural reasoning. Prefer these terms when the distinction is
material, but preserve the target project's established domain and technical names; do
not rename existing `service`, `API`, `component` or `boundary` identifiers merely to
match this glossary.

The full glossary lives in [LANGUAGE.md](LANGUAGE.md). Load it when:

- Reviewing architecture (`senior-architecture-reviewer`, `code-analysis`)
- Hunting deepening opportunities (`improve-codebase-architecture`)
- Designing interfaces or evaluating module shape
- TDD planning where module depth affects test surface

## Why this exists

A codebase full of shallow modules is hard for both humans and AI to navigate. The vocabulary in `LANGUAGE.md` makes the distinction between *deep* and *shallow* sayable, which is the prerequisite for fixing it.

When reviewing or planning, use the precise term when it clarifies the architectural
relationship — for example **seam**, **interface**, or **adapter** — while keeping the
project's existing terminology in code and task artifacts.

When the architectural conversation advances a task, resolve its durable record through
`../setup/references/task-context.md` and link decisions there. A standalone vocabulary
lookup does not create a task artifact.

## Upstream

The vocabulary and principles are adapted from Matt Pocock's `improve-codebase-architecture/LANGUAGE.md` ([github.com/mattpocock/skills](https://github.com/mattpocock/skills)), which itself draws on Ousterhout (*A Philosophy of Software Design*) and Feathers (*Working Effectively with Legacy Code*).
