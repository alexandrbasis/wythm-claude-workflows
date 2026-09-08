---
name: parallelization
description: Parallelize genuinely independent implementation items when /si or the user asks for parallel work. Use /si directly
  for one item, dependent work, shared files, or shared mutable state.
allowed-tools:
- Agent
- AskUserQuestion
- Read
- Write
- Edit
- Bash
- Grep
- Glob
- TodoWrite
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/parallelization/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/parallelization/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Parallel Implementation Orchestrator

Use this skill only after resolving the task with `../setup/references/task-context.md`. The
orchestrator owns shared task/review records and the final combined verification.

## Decide

Parallelize only when two or more work items are independent: they have disjoint owned paths, no
ordering dependency, and no shared mutable fixtures or state. If there is one item, an overlap, or
uncertain independence, continue directly through `/si` and state the reason once. Keep a wave to a
small set, normally no more than four workers.

Before dispatch, read `git status --short`, the task entrypoint, and the expected paths for each item.
Record the dispatch base revision for every isolated worker and the pre-dispatch inventory for a
shared checkout. If relevant inputs are already dirty, do not create workers from a clean `HEAD`; use
a coordinated shared checkout or continue sequentially. Leave unrelated changes untouched.

## Dispatch

Use whatever worker and isolation capabilities the environment supports. Prefer isolated execution
when available. A shared checkout is acceptable only when each worker has disjoint owned paths and
the orchestrator coordinates all shared state. Give every worker one item, its task path, optional
criterion/context paths, owned paths, and the exact git authority it inherits. Default to no commit.
If no supported worker capability exists, continue directly through `/si`.

Dispatch independent workers up to the host's supported concurrency before waiting. With one
worker slot, execute items sequentially or directly while preserving their coverage. Adapt to the
available API and isolation mechanism. A worker returns `complete`, `failed`, or `blocked` using
the developer-agent JSON contract.

## Consolidate

For each result:

1. Inspect the reported files and the worker's status; do not trust a summary without reading the
   changed tree.
2. For an isolated worker, compare the full owned tree with its recorded dispatch base, including
   committed, staged, and unstaged tracked changes. Use a binary diff from that base plus an explicit
   untracked-file listing for added, deleted, binary, mode, and symlink changes. For a shared checkout,
   inspect the changes in place against the pre-dispatch inventory; never replay them as a patch.
3. For isolated workers, transfer every owned path from that manifest, then resolve conflicts before
   reading the destination back. Preserve ownership, file content, modes, symlinks, and binary data.
4. Read back the destination inventory and compare it with the complete manifest. After all transfers,
   validate the combined tree from the commands and working directories resolved from project
   configuration. Worker checks are evidence for the item, not combined verification.

If a commit is authorized, stage only the assigned changes; whole-path staging is suitable only
when that file's entire diff is in scope. Inspect the staged diff and name-status/stat so unrelated
dirty changes remain outside the commit. Publication requires its own authority when not already granted.

## Verification and handoff

Run the required lint, type, test, render, schema, or plugin checks for the combined tree. Apply TDD
to behavior changes; validate docs, formatting, and metadata with fit-for-purpose checks without
inventing tests. Treat configuration as behavior when it changes runtime behavior. Mark the combined
work complete only when every required check passes; record `not_applicable` with a reason where a
check does not apply, and never turn a skipped or unresolved check into `passed`.

Update the task record once after consolidation with the parallelization decision, worker evidence,
combined verification, and next action. Workers do not edit shared task documents. Preserve the
complete final file inventory and any real blocker for the next stage.

## Safety rules

- One worker owns one scoped item; no scope creep or shared task writes.
- Reuse authorization already granted for the current task/request. Workers inherit explicit scoped
  git authority from the orchestrator and do not re-ask for blanket approval.
- Default: no worker branch and no worker commit. Publication is a separate gate when not granted.
- If a worker fails or is blocked, record the cause and resolve it sequentially; do not claim the
  combined task is complete from partial results.

## Output

Report the items dispatched, each worker's status/files/evidence, transfer conflicts, combined
verification, and the next sequential action. Keep the report concise and evidence-based.
