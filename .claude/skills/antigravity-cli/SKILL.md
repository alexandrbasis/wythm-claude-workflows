---
name: antigravity-cli
description: >-
  Run Google Antigravity CLI (agy) for web-grounded research, cross-AI review,
  or validation when those capabilities are explicitly needed or another
  skill delegates to agy. One-shot only; do not select it for an ordinary
  review without an explicit provider choice.
allowed-tools:
  - Bash
  - Read
---

# Antigravity CLI

> **Announcement**: Begin with: "I'm using the **antigravity-cli** skill for cross-AI validation with Antigravity (agy)."

Use this wrapper for an explicit Antigravity second opinion or for research that
needs its provider-specific grounding. Read the shared lifecycle in
`../codex-cli/references/cross-ai-run.md` first.

## Provider adapter

1. Check `command -v agy`, then `agy --version`. Read `agy --help` before using
   print mode, timeout, path injection, web, or output flags.
2. Use the locally supported non-interactive mode and output capture. Do not
   pass a model override unless local help and the caller explicitly require
   one; configured provider routing is the default.
3. Use `@path` or the provider's equivalent only after confirming each path
   exists. Use the least-privilege mode available for review/research; never
   pass permission-bypass or write flags unless explicitly requested.
4. Read the captured result, check exit status, and return the shared receipt.
   The result does not authorize edits, shell work, or publication.

If `agy` is absent or lacks a needed mode, report the prerequisite and stop.
Installation, update, sign-in, and settings changes are separate user actions;
this skill never runs a remote installer or mutates provider settings.

## Prompt requirements

Include the repository root, task/requirements path when task-attached, files or
diff scope, and concrete questions. For web research, ask for source URLs and
separate sourced claims from repository observations. Resolve task evidence
through `../setup/references/task-context.md`; standalone calls do not create a
task.

## When not to use

- The caller did not explicitly choose Antigravity or delegate to it
- A normal review or research tool already satisfies the request
- The request needs interactive refinement or file-writing work

## References

- `../codex-cli/references/cross-ai-run.md` — shared lifecycle
- `reference.md` — local-help-first provider lookup and historical notes
- `templates.md` — prompt shapes; resolve placeholders before execution
