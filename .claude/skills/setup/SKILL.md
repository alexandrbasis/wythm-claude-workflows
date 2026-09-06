---
name: setup
description: >-
  Configure claudops for a specific repository after copying the workflow or installing
  the plugin. Use for first setup, requested reconfiguration, or unresolved project
  placeholders in claudops files.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - AskUserQuestion
  - Agent
  - TodoWrite
---

# Configure claudops for a project

Configure the requested repository's workflow using values evidenced in that repository
and confirmed by the user. A plugin is a read-only template source; project configuration
belongs in the target repository's `.claude/` directory.

## 1. Establish the target and existing configuration

Resolve the requested repository and workspace in a monorepo. Inspect existing `.claude/`
files before preparing changes. For a re-run, determine whether the request means specific
values or a full reconfiguration; ask only when that scope is unclear. Preserve local
content outside the selected configuration regions.

When loaded from a plugin and project templates are missing, use the script adjacent to
this loaded skill, `scripts/bootstrap_project.py`. Resolve its absolute path from the
skill location; keep the target repository as the working directory:

```bash
python3 "/absolute/path/to/loaded/setup/scripts/bootstrap_project.py" --project "/absolute/project"
```

Review its `add` and `preserved` lists. An authorized first setup includes copying these
missing workflow templates; run the same command with `--apply` and read back the result.
The script preserves existing files and excludes settings, secrets and runtime state.
It does not configure or activate hooks. If existing files are older or customized,
use `update-setup` for those changes rather than overwriting them during bootstrap.

With a copied `.claude/` installation, configure the existing local files directly.
Completion: the target is explicit and the local files to configure are identified.

## 2. Detect and confirm values

Read [discovery outputs](references/discovery.md) for the categories relevant to this
setup: stack, paths, commands, architecture and any additional project-specific category.
Use independent scouts when that improves coverage; a small repository can be inspected
directly. Cite the source for each detected value and label unknowns. Obtain command
values from project configuration instead of guessing a language's usual defaults.

Present one reviewable set covering every detected category, including uncertainty and
current-versus-proposed values on reconfiguration. Confirm the values together; request
corrections for unresolved decisions. Values already approved for this scope remain
approved. Do not invent values for unknown placeholders.

Completion: each value to substitute has evidence and confirmation; unresolved values
are recorded separately.

## 3. Configure local workflow files

Apply the confirmed values through the authorized set without repeated per-file or
per-batch approval. Fill `coding-conventions/SKILL.md` and `review-conventions/SKILL.md`
first, then relevant skill and agent Markdown. Before each file, give a compact path and
substitution summary. Preserve user-authored text outside the selected regions.

Search for actual `{{UPPERCASE_VARIABLE}}` occurrences rather than any double brace.
Replace only confirmed variables. For multi-line layers and rules, use the confirmed
architecture; if none exists, say that no project-specific architecture rule is configured.
Keep unknown placeholders intact with a follow-up list. Documentation examples explaining
placeholder syntax are not unresolved project settings.

For hook configuration, read [hook values and activation](references/hooks.md). Configure
only hooks applicable to the detected stack. Validate Python literals and shell quoting.
Show the exact `.claude/settings.json` JSON diff, preserving every existing setting and
matcher, and obtain approval before activation. A previously approved exact diff may be
applied directly. Copying templates does not approve auto-commit or other hook side effects.

When a concrete architecture is confirmed, update
`code-analysis/references/project-checks.md` with checks for the detected source paths.
For disabling skills, list candidate names and reasons, let the user select the exact set,
then show the final set for confirmation. Rename only that set's `SKILL.md` files to
`SKILL.md.disabled`; keep every other skill enabled. Absence of a tool alone does not
approve disabling its skill.

## 4. Verify the destination

Read back changed local files and verify substitutions against the confirmed values.
Check remaining project placeholders across skills, agents and hooks. Parse any modified
JSON; syntax-check changed Python/shell hooks before activation. Confirm each configured
hook path exists and each selected matcher references the intended file. Report hooks as
active only when the settings read-back proves they are wired; runtime success needs an
actual invocation.

Finish with the configured repository, file counts, unresolved values, disabled skills,
and verified hook state. Distinguish copied, configured, wired and exercised components.
If a Claude session needs to reload newly materialized agents, say so; do not start an
unrequested implementation or review workflow just to test setup.
