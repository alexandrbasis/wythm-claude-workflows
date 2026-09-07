---
name: udoc
description: >-
  Update documentation for a completed implementation and, when the repository
  uses one or the user requests it, update its changelog.
  NOT for creating new product docs (use /product).
argument-hint: [task-path]
---

# Update Documentation (UDOC)

> **Announcement**: Begin with: "I'm using the **udoc** skill for documentation update and changelog."

## Objective

Synchronize documentation with an implemented change. A changelog is a
repository convention, not a required output of every run.

## Workflow

### 1. Resolve the task

Read `../setup/references/task-context.md` and resolve an explicit path, then
the current task, then the repository's configured convention. A supplied file
outside `tasks/` remains authoritative. If no task is resolved, ask for the
task path; do not create a product task just to hold documentation work.

Validate the resolved task record or a legacy
`tech-decomposition-*.md` in its directory. Keep the task record's objective,
status, changed documentation, and observed result current when the run is
task-attached.

### 2. Discover the documentation policy

Read an applicable `CLAUDOPS.md`, repository profile, manifests, and existing
documentation before choosing paths. Update the repository's established docs
locations and format. For changelogs:

- update an existing changelog convention when the task affects it;
- use a path explicitly configured by the repository or requested by the user;
- skip changelog generation when no convention exists and the user did not ask
  for one;
- never create `docs/changelogs/` merely because this skill was invoked.

Record the decision and skipped outputs in the task evidence when applicable.

### 3. Update documentation

Use an available documentation-updater agent when the host exposes one and its
scope matches the task. A changelog-generator is optional and runs only after
the policy above selects a changelog target. If an agent is unavailable, do
the bounded work directly or report the blocked capability; the skill does not
require two agents or invent a replacement agent.

Give every worker the resolved task path, selected documentation paths, and
write scope. Read each target before editing and preserve its format. Capture
changed paths and verification output.

### 4. Commit only within the caller's authorization

Show the exact changed paths and a diff summary. Commit only when the caller
authorized that exact scope, reusing an earlier authorization for the same
operation rather than asking again. Stage explicit reported paths; do not use
`git add -A`. Push is a separate external operation and requires an explicit
request unless the caller already authorized push for this exact scope. Do not
repeat an approval question after its authorization is already recorded.

### 5. Report

Report documentation paths, changelog path or the reason it was skipped, task
evidence location, verification, and commit/push state. Distinguish completed,
unavailable, and intentionally skipped outputs.

## Failure handling

- **Task not found**: list available task locations from the configured
  convention, without assuming `tasks/`.
- **No documentation change**: report that the current docs already match or
  that no affected documentation was identified.
- **Agent unavailable**: continue directly when the scope is clear; otherwise
  report the missing capability and stop before writing broad changes.
- **Policy unknown**: preserve existing docs and skip a changelog unless the
  user explicitly selects its location.

## Success criteria

- [ ] Task resolved when the run is task-attached
- [ ] Repository documentation policy and paths were discovered
- [ ] Only affected documentation was updated
- [ ] Changelog updated only when configured or explicitly requested
- [ ] Task evidence records changed paths and verification when applicable
- [ ] Commit/push performed only within existing authorization
