---
name: cursor-cli
description: Run Cursor CLI for one-shot cross-AI code review when a Cursor perspective is explicitly wanted. Invoke ONLY
  when the user asks ('cursor review', 'ask cursor', 'run cursor'), or another skill explicitly delegates to Cursor. Do not
  invoke it implicitly for a generic review. Not for interactive conversations.
allowed-tools: Bash Read
compatibility: Portable clients may not enforce Claude Code invocation guards or project setup behavior.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/cursor-cli/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/cursor-cli/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Cursor CLI

> **Announcement**: Begin with: "I'm using the **cursor-cli** skill for cross-AI validation with Cursor."

Use this wrapper for a one-shot Cursor review or approach validation. Read the
shared lifecycle in `../codex-cli/references/cross-ai-run.md` first.

## Provider adapter

1. Check `command -v agent`, then `agent --version`. Read `agent --help` when
   syntax, output, trust, mode, or model behavior is unclear. The binary name
   is provider-specific; do not substitute an unrelated `cursor` executable.
2. Use the locally supported print/one-shot mode. Select a model only when the
   caller or provider configuration supplies one; otherwise omit the override.
   This skill does not pin `composer-2` or any other model.
3. Select a read-only/ask or plan mode only if local help confirms its spelling.
   Do not use force, yolo, cloud-write, or MCP-approval bypass flags for a
   review unless the caller explicitly requests that behavior.
4. Capture and read the provider's documented output, then return the shared
   receipt. The result is evidence and does not authorize edits or publication.

If `agent` is missing or outdated for the requested capability, report the
prerequisite and stop. Installation or update is a separate user action; never
run a remote installer or modify Cursor settings implicitly.

## Prompt requirements

Include the repository root, task/requirements path when task-attached, changed
files or diff scope, and concrete questions. Cursor starts without this
conversation's context. Resolve task evidence through
`../setup/references/task-context.md`; standalone calls do not create a task.

## When not to use

- The caller did not explicitly choose Cursor
- The request needs interactive refinement
- The primary review workflow already answers the request

## References

- `../codex-cli/references/cross-ai-run.md` — shared lifecycle
- `reference.md` — local-help-first provider lookup and historical notes
- `templates.md` — prompt shapes; resolve placeholders before execution
