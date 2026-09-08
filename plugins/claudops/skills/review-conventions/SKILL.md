---
name: review-conventions
description: Internal reference skill — shared conventions for all code review agents. Not user-invocable.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/review-conventions/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/review-conventions/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Review Conventions

Shared knowledge preloaded into review agents. Apply these conventions when reviewing code.

## Project context

This reference stays generic so it can run in any repository. Read an
applicable `CLAUDOPS.md`, manifests, CI configuration, source layout, and
existing code before applying project-specific review rules. Use the project's
own language, framework, layers, test commands, and documentation locations;
leave unknowns explicit. `{{...}}` markers are historical template notation,
never runtime defaults or executable paths.

## Architecture Rules

Review boundaries and dependencies as the target project defines them. Use its
architecture vocabulary where it already has one; do not rename `service`,
`API`, `module`, or similar identifiers merely to fit this reference.

## Code Standards

- Prefer project-established type/interface conventions
- Preserve local naming and type conventions; apply language-specific rules such
  as underscore prefixes or `any` only when the repository's tooling establishes
  them.
- Secrets never logged; environment vars flow only through config providers
- Database queries use parameter binding — no dynamic SQL or string interpolation

## Review Quality Rules

Reviews run in two stages so we get recall AND precision:

1. **Find stage (this skill)** — report every issue you notice, including low-severity
   and uncertain ones. For each finding, include:
   - `severity`: CRITICAL | MAJOR | MINOR | INFO
   - `confidence`: high | medium | low
   - `location`: `file:line`
   - `suggestion`: concrete fix or next step
   Do not self-censor based on severity or confidence — a later verification pass
   will filter before anything reaches the user.

2. **Presentation** — consolidate repeats ("5 functions missing error handling" with
   a list, not 5 separate findings). Explain why each issue matters. Highlight
   positive practices alongside problems.

## Sizing & Comment Hygiene

Norms from Google's [engineering practices guide](https://google.github.io/eng-practices/):

- **Change sizing** — a reviewable change is small (~100 lines is a healthy target). If the diff is large and not mechanically generated, flag it and suggest splitting; a 1000-line PR gets a worse review, not a better one.
- **The standard is "improves code health"** — approve a change that improves the codebase even if it isn't perfect. Don't block on personal preference; block on real problems.
- **Mark non-blocking comments** — prefix advisory notes (`Nit:`, `Optional:`, `FYI:`) so the author can tell what must change from what's a suggestion. Severity inflation trains authors to ignore you.

- Primary scope: only review files in `changed_files`
- Use `full_diff` to focus on changed lines
- You may read unchanged files for context (interfaces, contracts), but don't raise
  findings against unchanged code — the author isn't touching it in this PR.
- Skip pre-existing issues unless the current changes make them worse (e.g., a bug
  that used to be in dead code is now reachable).

## Ownership Boundaries

Each agent owns specific concerns — do not duplicate other agents' work:

| Concern | Owner |
|---------|-------|
| Spec requirements match | `spec-compliance-reviewer` |
| Architecture fit, layers, module boundaries | `senior-architecture-reviewer` |
| Security, auth, injection, OWASP | `security-code-reviewer` |
| Code quality, naming, DRY, complexity | `code-quality-reviewer` |
| Test coverage and quality | `test-coverage-reviewer` |
| Documentation accuracy | `documentation-accuracy-reviewer` |
| Performance, N+1, memory | `performance-reviewer` |

If you spot something outside your scope, note it as a one-line INFO finding with
the likely owner (e.g. "possible security concern — flag for `security-code-reviewer`")
and move on.

## Project File Locations

- Architecture docs: resolve from the repository's documented location or
  changed-file references; do not assume a `docs/` subdirectory.
- Product docs (PRDs, JTBDs): `product-docs/`
- Task documents: resolve through `../setup/references/task-context.md`; preserve
  repository conventions such as `tasks/<task-dir>/tech-decomposition*.md`
- Test structure: infer from the repository's existing test layout and CI.
