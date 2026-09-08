---
name: antigravity-cli
description: Run Google Antigravity CLI (agy) for web-grounded research, cross-AI review, or validation when those capabilities
  are explicitly needed or another skill delegates to agy. One-shot only; do not select it for an ordinary review without
  an explicit provider choice.
allowed-tools:
- Bash
- Read
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/antigravity-cli/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/antigravity-cli/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Antigravity CLI

> **Announcement**: Begin with: "I'm using the **antigravity-cli** skill for cross-AI validation with Antigravity (agy)."

Use this wrapper for an explicit Antigravity second opinion or for research that
needs its provider-specific grounding. Read the shared lifecycle in
`../codex-cli/references/cross-ai-run.md` first.

## Provider adapter

1. Check `command -v agy`, then `agy --version`. Read `agy --help` before using
   print mode, output, timeout, model, or effort flags. If the binary or a
   required capability is absent, report the prerequisite and stop.
2. For an explicit Gemini run, inspect `agy models`, choose an exact currently
   listed `gemini-*` slug, and pass it as `--model`. Record the selected
   provider and model. If no model was requested, omit `--model` and retain the
   provider's configured default; an unreported default model is unverified and
   does not establish model-level independence.
3. For review or research, resolve the loaded skill directory, run from the
   target repository root, and use the runner with a fresh output directory:

   ```bash
   ANTIGRAVITY_SKILL_DIR="/absolute/path/to/loaded/antigravity-cli"
   python3 "$ANTIGRAVITY_SKILL_DIR/scripts/review.py" \
     --prompt-file /tmp/agy-prompt.md \
     --file path/to/file.py \
     --file path/to/requirements.md \
     --model '<exact slug from agy models>' \
     --effort high \
     --timeout 120 \
     --output-dir /tmp/agy-review-unique
   ```

   `ANTIGRAVITY_SKILL_DIR` must be the actual directory containing this loaded
   skill; do not resolve it from the target repository's current directory.
   `--file` is repeatable. `--effort` is optional and accepts `low`, `medium`,
   or `high`. The runner verifies and pre-reads those files, then
   inlines their contents so a denied provider file read cannot look like a
   successful review. `--model` is optional and has no runner default; omit the
   line when the configured provider default is intended. Use a new output
   directory for every attempt and do not retry implicitly.
4. Read `receipt.json`, `stdout.json`, `version.stderr.log`, `response.txt` on
   success, and `stderr.log` from the output directory. A valid completed
   review requires process exit 0, payload
   `status: SUCCESS`, a non-empty `response`, and no `denied_actions`. A
   `SUCCESS` result with an
   empty or visibly partial answer, or with any denied action, is `PARTIAL` and
   must never be reported as a passed review. Inspect and retain stderr even on
   exit 0. Return the shared receipt; the result never authorizes edits, shell
   work, or publication.

The runner invokes the supported headless shape: `agy -p --output-format json
--print-timeout <duration>`, with an explicit `--model <slug>` only when chosen
by the caller. The old `--approval-mode` and `-o` forms are incompatible with
the tested Antigravity CLI. Do not use permission-bypass flags, settings/auth
edits, or automatic model fallback.

For upstream behavior, use the official [headless CLI docs](https://antigravity.google/docs/cli/headless/),
[migration guide](https://antigravity.google/docs/cli/gcli-migration/), and
[installation guide](https://antigravity.google/docs/cli/install/). Verify local
behavior first because flags, models, and output fields can change.

## Prompt requirements

Include the repository root, task/requirements path when task-attached, files or
diff scope, and concrete questions. For web research, ask for source URLs and
separate sourced claims from repository observations. Resolve task evidence
through `../setup/references/task-context.md`; standalone calls do not create a
task. Do not put unverified `@path` references in review prompts; pass verified
files through the runner's repeatable `--file` option.

## When not to use

- The caller did not explicitly choose Antigravity or delegate to it
- A normal review or research tool already satisfies the request
- The request needs interactive refinement or file-writing work

## References

- `../codex-cli/references/cross-ai-run.md` — shared lifecycle and receipt
- `reference.md` — local-help-first flags, models, output, and migration notes
- `templates.md` — prompt shapes and runner examples
