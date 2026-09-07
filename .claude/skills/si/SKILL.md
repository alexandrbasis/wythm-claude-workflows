---
name: si
description: >-
  Implement or resume a ready task, from a compact task record or a technical decomposition,
  with behavior-first tests and durable verification. Use for requested implementation;
  discovery belongs to /nf, planning to /ct, and independent review to /sr.
argument-hint: [task-directory | tech-decomposition-path]
allowed-tools: [Agent, AskUserQuestion, Edit, Read, Write, Bash, Glob, Grep, Skill, TodoWrite]
---

# Implement a task

Deliver the requested behavior and leave enough verified task state for review or the
next session. A compact task and a formal decomposition use the same implementation
contract; scale documentation and delegation to the work.

## 1. Resolve the task and readiness

Read [shared task context](../setup/references/task-context.md). Reuse the explicit or
established task and follow its active phase/plan pointers. If none exists, create the
minimum record before starting. Preserve the repository's filenames and status vocabulary.

Read the objective, acceptance criteria, constraints, relevant decisions, planned changes
and verification approach. Equivalent sections in any language satisfy this contract.
Populate missing structural information from the authorized request and repository
evidence; do not stop merely because a particular heading or `tech-decomposition-*.md`
is absent. A known, bounded fix can keep its short plan in the existing task record.

When behavior or scope is materially unresolved, save the question/blocker and resolve
it before dependent implementation. Use `/nf` or `/ct` when actual discovery or planning
is needed. A task status or a PR description alone does not invent an approved spec.

## 2. Establish the change boundary

Inspect the relevant code, tests, project instructions and working-tree state. Record
which files/packages the work affects and how to verify the outcome. Preserve unrelated
user changes. Use an isolated branch/worktree when warranted and authorized; an already
selected working directory does not need another checkout by default.

Reuse authorization for the same operation and scope. Commit, push, PR, merge and
tracker writes follow their actual authorization boundary; an implementation request
alone does not authorize publication. Do not manufacture test/implementation commit
history or reset shared work to recreate a test-first sequence.

## 3. Implement and retain evidence

Follow [TDD](../tdd/SKILL.md) for behavior changes: one failing behavior test, verify the
failure's cause, implement, then refactor within scope. Use the agreed test strategy;
documentation, formatting and other non-behavior changes use appropriate validation
without artificial tests. Existing project testing requirements remain in force.

Keep one acceptance-to-evidence mapping in the task's existing checklist or test plan.
Reuse requirement IDs and existing verification rows; do not generate parallel REQ,
TEST and VC ledgers for the same facts. Each required behavior must have an observed
test, check or artifact before it is marked complete.

Read [verification recipes](references/verification-gate.md) for exact-count, enumerated,
visual or other brittle requirements. Read [implementation checklists](references/implementation-checklists.md)
when changes involve entity mutations, async interactions or material deviations from the
plan. Preserve post-action visibility, error handling and data/state consistency checks
where they apply. Use the repository's canonical domain terms.

Implement the full agreed scope. After a meaningful completed step, update its evidence,
actual progress and next action. Record material deviations and their rationale once;
new product scope requires a decision, not silent expansion. Save progress before a long
pause and resume from those files after compaction.

For independently useful work with disjoint ownership, read [parallelization](../parallelization/SKILL.md).
Use supported workers only when delegation helps; otherwise work directly. Pass the task,
owned paths, constraints and expected result to each worker. One orchestrator consolidates
shared documents and verifies the combined result.

## 4. Verify completion

Remove temporary instrumentation, dead imports and other residue introduced by this task.
Run the checks required by the change and project policy from their owning package;
resolve commands from configuration or CI. Record command, working directory, outcome
and relevant revision/artifact. Reuse valid evidence for unchanged code; rerun affected
checks after subsequent edits. A skipped or blocked check is not a pass.

Check every acceptance item against evidence, including enumerated fields/options and
cross-surface behavior where specified. Missing required evidence prevents claiming
implementation complete. A partial result may be reviewed as a draft with its gaps named.
For non-trivial decisions, try to find a counterexample before handoff; unresolved
substantive findings remain blockers or explicitly accepted limitations.

## 5. Hand off the actual result

Update the task's implementation status and link code/verification evidence, deviations
and known follow-ups. A separate completion document is unnecessary when the task already
contains these facts. Completing a phase does not complete its parent feature.

When independent review is requested or required, hand `/sr` the active task and actual
review target. A local diff is valid review input; a pushed branch or PR is not a
prerequisite. Perform commits, push or PR creation only within their granted scope and
read back any action you claim. End with the result and the next action, distinguishing
implemented, reviewed, merged and deployed states.
