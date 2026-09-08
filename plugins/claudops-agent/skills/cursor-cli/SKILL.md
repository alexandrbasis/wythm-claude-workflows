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

1. Check `command -v agent`, `agent --version`, and `agent --help`. Verify the
   binary is Cursor Agent and supports `--print`, `--mode ask`, and
   `--output-format json`. `cursor-agent` may be an installation alias; do not
   substitute the Cursor editor executable.
2. When the caller requests a particular model or an independent model family,
   inspect `agent models` and select an exact listed slug. Otherwise omit the
   model override. Cursor supports multiple providers; `auto` and an unreported
   default do not establish model-level independence. Record the requested slug
   separately from any model identity actually reported by the provider.
3. Resolve the loaded skill directory and run the adapter from the target
   repository root with Python 3.10+:

   ```bash
   CURSOR_SKILL_DIR="/absolute/path/to/loaded/cursor-cli"
   python3 "$CURSOR_SKILL_DIR/scripts/review.py" \
     --prompt-file /tmp/cursor-prompt.md \
     --file path/to/file.py \
     --timeout 120 \
     --output-dir /tmp/cursor-review-unique
   ```

   Set `CURSOR_SKILL_DIR` to the directory containing this loaded skill, not a
   path relative to the reviewed repository. `--file` is repeatable and pre-reads
   verified UTF-8 files into the prompt. The combined input limit is 96 KiB;
   narrow larger reviews explicitly. Add `--model '<exact listed slug>'` only
   when selected. Each invocation requires a fresh output directory.
4. Inspect `receipt.json`, `stdout.json`, `stderr.log`, `version.stderr.log`, and
   `response.txt` on success. A completed JSON result requires exit 0,
   `type: result`, `subtype: success`, `is_error: false`, and a non-empty string
   `result`. An error envelope, timeout, malformed output, trust rejection, or
   empty answer is incomplete. Also read the answer for blocked reads, omitted
   scope, or other visible limitations: a valid envelope alone does not prove
   the review was completed. Return the shared receipt and evidence gaps.

The adapter always uses `agent -p --mode ask --output-format json`. Print mode
alone can use write and shell tools; keep the explicit read-only mode. Workspace
trust is a separate prerequisite: the adapter preserves a trust rejection and
stops. It does not pass `--trust`, force/yolo, automatic MCP approval, or sandbox
bypass flags, retry, authenticate, update the CLI, or modify settings. Resolve
missing capabilities or trust through a separate user-authorized action.

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
- `reference.md` — native output contract, trust boundary, and official sources
- `templates.md` — prompt shapes; resolve placeholders before execution
