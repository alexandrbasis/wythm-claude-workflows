---
name: update-setup
description: >-
  Inspect or apply upstream claudops changes to a project's copied .claude/ workflow.
  Use for claudops update checks, selected upstream adoption, or conflicts with local
  workflow customizations. Installed plugin upgrades use the host's plugin manager.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - AskUserQuestion
---

# Update Setup

Sync local `.claude/` workflow files with upstream claudops. The skill is
upstream-driven: local-only user files are ignored unless they are explicitly tracked in
the update manifest.

## Scope and authority

- Start with the deterministic script. Do not classify diffs manually.
- A check-only request ends at the report. Before applying updates, refreshing disabled
  files or deleting removed upstream files, establish approval for the exact paths and
  operations. Reuse approval already granted for that selection. Branch creation, commit,
  push and PR creation require their own authorized scope; they are not update prerequisites.
- Never update `.claude/settings.json`, `.claude/settings.local.json`, `CLAUDE.md`,
  hook logs, `.gitkeep`, or local-only `*.local.*` files through this skill.
- Use LLM judgment only to explain conflicts and help the user choose a strategy after
  the script has produced exact statuses and diffs.

## Resolve the script and target

Resolve `scripts/update_setup.py` relative to this loaded skill, including when it is
inside a plugin. Keep the consuming repository as the working directory. Set these
shell variables to the actual resolved paths for the commands below:

```bash
CLAUDOPS_UPDATE_SCRIPT="/absolute/path/to/loaded/update-setup/scripts/update_setup.py"
CLAUDOPS_TARGET="/absolute/path/to/target-repository"
python3 "$CLAUDOPS_UPDATE_SCRIPT" --help
```

The script's `--local-root` is a global option and belongs before `scan`, `apply`, or
`verify`. Its local state belongs to the target repository; never point it at a managed
plugin cache. An installed plugin upgrade is a separate operation through the host's
plugin manager. Read the installed plugin's identifier before constructing that command.

The script writes adoption state to:

```text
.claude/skills/update-setup/claudops-upstream.lock.json
```

Tracked scope:

- `.claude/**`

Skipped scope:

- `.claude/settings.json`
- `.claude/settings.local.json`
- `.claude/hooks/logs/**`
- `.gitkeep`
- `CLAUDE.md`
- local-only `*.local.*`

## Workflow

### 1. Scan

Create a deterministic report:

```bash
python3 "$CLAUDOPS_UPDATE_SCRIPT" --local-root "$CLAUDOPS_TARGET" scan \
  --output .claudops-update-report.json
```

For local testing against an existing upstream clone:

```bash
python3 "$CLAUDOPS_UPDATE_SCRIPT" --local-root "$CLAUDOPS_TARGET" scan \
  --upstream-root /tmp/claudops-upstream-sync \
  --commit "$(git -C /tmp/claudops-upstream-sync rev-parse HEAD)" \
  --output .claudops-update-report.json
```

### 2. Present Report

Render the report:

```bash
python3 "$CLAUDOPS_UPDATE_SCRIPT" --local-root "$CLAUDOPS_TARGET" report \
  --report .claudops-update-report.json
```

Explain statuses:

- `new`: upstream file is not present locally.
- `modified`: upstream differs from local and local has no tracked conflict.
- `conflicting`: local changed since the last tracked adoption.
- `disabled`: upstream file exists, but local has `<path>.disabled`.
- `removed`: file was tracked in the manifest but is gone upstream.
- `placeholder_only`: differences are filled `{{PLACEHOLDER}}` values.
- `unchanged`: local matches upstream or the tracked adoption hash.

If only `unchanged` and `placeholder_only` entries exist, report that the setup is up to
date and stop.

### 3. Resolve the selection

Present the exact paths and operations for approval unless that selection is already
authorized. Paths are relative to `.claude/`. Convert the approved selection into JSON:

```json
{
  "update": [
    "skills/example/SKILL.md"
  ],
  "refresh_disabled": [
    "skills/disabled/SKILL.md"
  ],
  "delete": [
    "skills/removed/SKILL.md"
  ]
}
```

Rules:

- `update` may include `new` and `modified` paths.
- `refresh_disabled` may include `disabled` paths and writes `<path>.disabled`.
- `delete` may include only `removed` paths.
- Do not apply `conflicting` paths until the user chooses a conflict strategy.

### 4. Apply

After approval:

```bash
python3 "$CLAUDOPS_UPDATE_SCRIPT" --local-root "$CLAUDOPS_TARGET" apply \
  --report .claudops-update-report.json \
  --selection /path/to/selection.json
```

The apply step updates selected files and refreshes the target repository's lock manifest.
Use the source clone and local files from the reviewed scan. If either changes before
application, rerun the scan and resolve any changed selection before writing.

### 5. Verify

Run:

```bash
python3 "$CLAUDOPS_UPDATE_SCRIPT" --local-root "$CLAUDOPS_TARGET" verify
```

When changing this helper or its command contract, run the `tests/test_update_setup.py`
file adjacent to the loaded skill. A report or successful script exit alone does not
prove the selected files were adopted: read back the result counts and destination hashes.

## Conflict Handling

For `conflicting` files:

1. Show the file path and exact diff from `.claudops-update-report.json`.
2. Explain what upstream changed and what local changed.
3. Ask the user to choose one strategy:
   - replace local with upstream
   - keep local and mark skipped
   - manually merge, then update the manifest after verification

Do not silently merge conflicts.

## Post-Update Checks

After applying selected updates:

- Run `verify`.
- If new hook files were added, inspect `.claude/settings.json` and report unwired hooks
  as manual follow-up. Do not auto-edit settings.
- If updated files contain `{{PLACEHOLDER}}`, tell the user to run `/setup`.
- Summarize counts: updated, disabled refreshed, deleted, skipped, placeholders, and
  manual follow-ups.

## Edge Cases

- Clone failure: report the git error and stop.
- Missing `.claude/`: route an authorized first configuration to `setup`; it can materialize
  the bundled templates. A check-only request reports that there is no copied workflow.
- Conflicts: show the affected paths and material changes. Group related conflicts for
  review; the file count does not determine their severity.
- Binary files: the script may copy them, but conflict explanation should avoid trying to
  summarize binary content.
