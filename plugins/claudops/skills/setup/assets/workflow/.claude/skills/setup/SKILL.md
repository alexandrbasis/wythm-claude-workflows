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

# Configure claudops for a repository

Make the workflow usable in the selected repository. The installed plugin supplies
instructions and resources; repository configuration records only local choices.
A task can start without setup when its context is already discoverable.

## Establish the project

Read [shared context](references/task-context.md) for repository/resource resolution.
Resolve the target workspace and inspect project instructions, an existing `CLAUDOPS.md`,
task directories and command configuration. On reconfiguration, compare current and
requested values. Preserve unrelated local content and disabled skills.

Use [discovery categories](references/discovery.md) only for missing relevant context.
Determine task-root conventions, command sources and unusual architecture or release
constraints from evidence. Ask once for material unresolved choices; reuse decisions
already supplied by the user. Do not make routine detected values into a new approval gate.

## Configure the minimum

Prefer the repository's existing configuration home. If none exists and durable choices
are needed, write `CLAUDOPS.md` at the repository root. Keep it short:

```markdown
# Claudops project context
Task root: tasks/  <!-- replace with the actual established convention -->
Workspaces: <relevant package roots, when needed>
Command sources: <package configuration / CI paths; non-obvious invocations if needed>
Project constraints: <rules that cannot be discovered from the files above>
```

Record only actual values; omit irrelevant fields. Link existing instructions rather
than duplicate them. Fill a task record using the shared contract when setup supports
an active task. Setup itself does not require a product discovery document.

Plugin mode does not copy all skills into the project. Read explicit local skill
customizations if present; the installed defaults cover other capabilities. Resolve
unfilled legacy command placeholders from actual project sources for the current task;
unknown values block only dependent work. A missing `.claude/` directory is not a blocker.

## Optional copied-workflow maintenance

Use this branch only when the user requests a repository-owned copy of the workflow,
or reconfiguration of an existing copied installation. The script adjacent to this
skill, `scripts/bootstrap_project.py`, previews missing templates:

```bash
python3 "/absolute/path/to/loaded/setup/scripts/bootstrap_project.py" --project "/absolute/project"
```

Inspect `add` and `preserved`, then apply with `--apply` within the authorized scope.
It preserves existing files and disabled markers and excludes settings, secrets and
runtime state. Use `update-setup` for existing customized files. Substitute only
confirmed legacy `{{UPPERCASE_VARIABLE}}` values in the selected local files; retain
unknowns and report the dependent capabilities. Plugin resources remain unchanged.

For requested hooks, read [activation guidance](references/hooks.md). Show the exact
settings diff and obtain approval before activating side effects, unless that exact
scope is already approved. Validate changed scripts and preserve existing matchers.
Disable skills only when the user selects that set; tool absence does not authorize it.

## Verify and finish

Read back configured files, verify referenced paths and commands against their sources,
and report unresolved decisions. Parse modified configuration and syntax-check modified
hook scripts. Distinguish configured, copied, wired and exercised components. Runtime
success requires an actual relevant invocation; do not start another workflow solely to
claim setup succeeded. The result is the configured project and any active task's next step.
