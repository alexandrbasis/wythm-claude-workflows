---
name: coding-conventions
description: Internal reference skill — coding standards and patterns for developer agents. Not user-invocable.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/coding-conventions/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/coding-conventions/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Coding Conventions

Shared knowledge preloaded into developer agents. Follow these when implementing features.

## Project context

This is a portable reference, not a generated project profile. Before making a
project-specific choice, read an applicable `CLAUDOPS.md` and inspect the
repository's manifests, source layout, CI configuration, and existing code.
Use the project's own framework, language, layers, test runner, and commands;
unknown values stay explicit until evidence is available. Do not treat
`{{...}}` markers as commands or fill them with guesses. Preserve existing
local conventions when no profile is present.

## Code Style

- Match the project's existing type/interface conventions — new code should look
  like it was written by the same person as the surrounding code.
- Preserve the project's type and naming conventions. Apply language-specific
  rules (including `any`, underscore prefixes, or equivalent) only when the
  language tooling or local style establishes them.
- Route secrets through config providers only — never hardcoded, never logged
  (logs ship to observability tools; hardcoded secrets leak via git history).
- Keep DTOs aligned with API schemas and the tech-decomposition's acceptance
  criteria — these are the contract downstream consumers rely on.
- Use parameter binding for database queries (not string interpolation) to prevent
  SQL injection.

## Testing

- **TDD**: RED → GREEN → REFACTOR — vertical slices only (one RED→GREEN per behavior). Canonical: `.claude/skills/tdd/SKILL.md`.
- Discover test, lint, and type-check commands from the project manifest, CI,
  profile, or documented scripts. If a check has no supported command, report
  it as unavailable rather than executing a placeholder.
- Find test files from the repository's actual layout and naming patterns.
- Arrange-Act-Assert pattern, descriptive test names
- Proper mocking of data-access layer in unit tests

## Implementation Rules

- Start by reading the task document — it's the source of truth for what to build,
  and implementation choices should flow from it rather than from prior assumptions.
- Resolve the task through `../setup/references/task-context.md` when this is a
  task-attached run; standalone implementation guidance does not create a synthetic task.
- Write the minimum code that makes the tests pass and the acceptance criteria
  hold. Don't add features, abstractions, or cleanup that weren't asked for.
- Bug fixes don't need surrounding refactors — fix the bug, leave the rest.
- Skip defensive error handling for scenarios that can't actually happen in this
  codebase's flow.
- Match existing codebase patterns — new code should look like it belongs.
- No git writes unless explicitly approved by orchestrator

## Engineering Principles

Named heuristics worth applying by name (mostly from *Software Engineering at Google* and Ousterhout's *A Philosophy of Software Design*):

- **Chesterton's Fence** — don't remove or rewrite code whose purpose you don't understand. Find out why it's there first; "it looks unnecessary" is not a reason.
- **Code is a liability** — every line is maintenance surface, not an asset. The best change is often less code; prefer deleting over adding.
- **Hyrum's Law** — with enough users, every observable behavior of an interface will be depended on. "It's just an implementation detail" doesn't make a change safe — treat observable behavior as the contract.
- **Deep modules** — hide substantial functionality behind a narrow, simple interface. Many shallow pass-through layers add complexity without earning it.
