---
name: codex-cli
description: Run OpenAI Codex CLI for one-shot cross-AI code review or approach validation. Invoke ONLY when the user explicitly
  asks ('second opinion', 'codex review', 'ask codex', 'run codex', 'cross-AI check'), or when another skill passes an explicit
  instruction to delegate to codex. Do not invoke proactively on general review requests. Not for interactive conversations.
allowed-tools:
- Bash
- Read
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/codex-cli/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/codex-cli/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Codex CLI

> **Announcement**: Begin with: "I'm using the **codex-cli** skill for cross-AI validation with Codex."

Use this wrapper for one-shot Codex review, approach validation, or a delegated
second opinion. Read the shared lifecycle in
`references/cross-ai-run.md` before running it.

## Provider adapter

1. Check `command -v codex`, then `codex --version`. Read `codex --help` and
   `codex exec --help` when the installed version or requested scope is unclear.
2. Use the locally supported non-interactive command and output option. Choose
   the caller's model, or omit a model override for the configured default.
   Never pass a hardcoded model from this skill.
3. Prefer the provider's least-privilege mode for review. Do not use an
   autonomous write or permission-bypass mode unless explicitly requested.
4. Capture stdout/stderr according to the installed CLI's help, read the result,
   and return the shared receipt. Historical `codex review` versus `codex exec
   review` flag differences belong in `reference.md`; verify them locally before
   use.

If `codex` is absent or needs an update, report the exact missing prerequisite
and stop. Installing or updating it is a separate user action; this skill never
runs `npm i -g`, `curl | bash`, or changes Codex settings.

## Prompt requirements

The prompt is a cold-start handoff. Include the repository root, task path when
task-attached, changed files or diff scope, requirements, and the specific
questions to answer. Ask for findings or an approach only; the result does not
authorize repository edits.

For task-attached calls, resolve `../setup/references/task-context.md` and save
the result receipt in that task's evidence area. Standalone calls return the
result without creating a task.

## When not to use

- The user asked for the primary review or implementation workflow only
- The request needs an interactive conversation
- The question is trivial or can be answered from local evidence

## References

- `references/cross-ai-run.md` — shared preflight, context, capture, and evidence lifecycle
- `reference.md` — exact flags only after checking the installed CLI; historical compatibility notes
- `templates.md` — prompt shapes, with placeholders that must be resolved before execution
