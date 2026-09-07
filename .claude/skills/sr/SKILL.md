---
name: sr
description: >-
  Use when asked to review code before merge or review a PR, branch, commit
  range, task path, or current working tree. Trigger on requests like
  'review PR', 'review my changes', 'review this branch', 'is this ready to
  merge', or other pre-merge review requests. Supports task/spec-aware review
  when task docs exist. NOT for addressing review comments (use /prc).
argument-hint: [task-path | PR-url | branch | range | deep | no-arg auto-detect]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - TodoWrite
  - Skill
  - Agent
---

# Start Review

> **Announcement**: Begin with: "I'm using the **sr** skill for universal code review."

Universal review entrypoint for task paths, PRs, branches, explicit ranges, and local working-tree drafts. Resolve the review target first, then only run checks supported by the evidence you actually have.

Before resolving the target, resolve one task context with `../setup/references/task-context.md`. Reuse
the explicit task or linked active task; otherwise create the minimum record in the configured task
root. A PR title/description is review context only and never becomes an invented specification.
Link the review artifact, immutable snapshot, verification results, findings, and one next action
from that record. Existing conversation authorization remains authoritative for writes. If this is a
read-only review, return a proposed path rather than
creating a task file.

## When to Use
- Pre-merge code review
- "review this PR"
- "review this branch"
- "review my changes"
- "is this ready to merge?"
- Task review when a task directory or spec exists

## When NOT to Use
- Addressing review comments -> `/prc`
- General codebase exploration -> `/code-analysis`
- Implementation-plan review -> `/rip`

## STEP 1: Resolve Review Target

- Resolve the task context and record the target reference before dispatching reviewers.
- Task path -> `task`
- PR URL or PR number -> `pr`
- Explicit git range -> `range`
- Branch name -> `branch`
- No arguments:
  1. If staged, unstaged, or untracked changes exist -> `working-tree`
  2. Else if current branch differs from resolved base -> `branch`
  3. Else ask what to review

## STEP 2: Detect Capabilities

Record these fields before dispatching reviewers:
- `has_task_doc`
- `has_spec`
- `has_committed_snapshot`
- `can_run_verification`
- `review_scope`

Rules:
- `task` mode may use task docs and spec compliance
- `pr`, `branch`, and `range` modes do not require task docs
- `working-tree` mode never requires a clean tree
- set `has_committed_snapshot = false` for `working-tree`; set it from resolved SHAs for committed modes
- Never claim spec compliance when no spec artifact exists
- PR descriptions or issue text do not count as spec unless the user explicitly says to treat them as the review baseline
- Cross-AI validation and Linear syncing are optional follow-ups, not default gates

## STEP 3: Resolve Base and Diff Context

Prefer base in this order:
1. PR base branch
2. Task-documented base branch
3. Current branch upstream
4. `main`
5. `master`

Compute diff context once and share it with all reviewers:
- `changed_files`
- `full_diff`
- `review_mode`
- `base_ref`
- `head_ref`
- `has_spec`

Diff rules:
- `task`, `pr`, `branch`, `range`: use committed diff from the resolved base or explicit range
- `working-tree`: use staged plus unstaged local diff, include untracked files in `changed_files`, set `base_ref = HEAD`, and set `head_ref = working-tree`
- Exclude generated files and lockfiles unless the user explicitly wants them reviewed

Do NOT force `main...HEAD` onto every review mode.

## STEP 4: Choose Scope

Use `quick` only when ALL are true:
- `<= 3` changed files
- `<= 50` diff lines
- no auth, migrations, infra, build-system, or shared framework changes

Otherwise use `full`.

**Deep (thermo) scope (`/sr deep`):** opt-in structural-quality tier. `deep` runs everything `full`
does **plus** the `structural-quality-reviewer` (STEP 5.3). It is never auto-selected — only the user
invokes it via `/sr deep`.

**Auto-suggest deep:** after resolving scope, if the diff crosses any structural threshold — a changed
file `> 1000` lines, `> 15` changed files, `> 600` changed lines, or a module rename/move — and the user
did not request `deep`, add a one-line recommendation to the review output (alongside the STEP 10 QA
recommendation): `Deep structural review recommended: <trigger>. Run /sr deep.` This is a recommendation,
not a blocker — continue with `full`.

**Full-feature scope option (`--scope=feature`):** When reviewing Phase N of a multi-phase task and the task directory contains earlier phases, optionally include the full feature diff (all phases from the earliest base commit to HEAD). Flag files changed in earlier phases but not in the current phase as **integration surface** — these are where cross-phase bugs hide. Use this when the current phase integrates with prior phases or when the task doc mentions cross-phase dependencies.

## STEP 5: Review Pipeline

`deep` is a superset of `full`: apply every `full`-scope rule below, then add the structural pass (5.3).

### 5.1 Optional Spec Gate

Run `spec-compliance-reviewer` only when `has_spec = true`.

If no spec exists, write:
`Skipped - no task/spec artifact available.`

### 5.2 Core Reviewers

Always run:
- `security-code-reviewer`
- `code-quality-reviewer`

Run `senior-architecture-reviewer` when:
- scope is `full`, or
- boundaries or dependencies changed, or
- new modules, services, or interfaces were introduced

### 5.3 Extended Reviewers

In `full` scope, also run:
- `test-coverage-reviewer`
- `documentation-accuracy-reviewer`
- `performance-reviewer`

In `deep` scope, additionally run `structural-quality-reviewer` — a whole-module structural audit
(details in its agent file). It writes to `<!-- SECTION:structural-quality -->`. Never run it in `quick`
or `full`.

### 5.4 Targeted Review Passes & Pattern Propagation

Orchestrator-owned inline checks (not subagents) plus a sibling-scan procedure. The trigger table and
per-pass checklists — error-path, integration-seams, cross-surface entity — and the pattern-propagation
procedure live in **`references/review-passes.md`**. Read it now when the diff matches any trigger, run
the matching pass, and add findings to `key-findings`.

For every skipped reviewer, write a one-line reason in that section. If the host cannot dispatch
the selected reviewers in one batch, run the same selected passes sequentially and preserve their
scope; do not silently reduce coverage.

When pattern propagation finds occurrences outside the diff, report them as contextual,
non-gating evidence unless the current change amplifies or newly exposes the pattern. Keep changed
file findings primary and do not expand the verdict to unrelated pre-existing defects.

## STEP 6: Verification Policy

Verification is evidence, not a prerequisite for starting review.

- `task`: prefer verification commands from the task doc; otherwise run narrow package checks
- `pr`, `branch`, `range`: run the smallest repo-appropriate checks for touched packages when safe
- `working-tree`: run only safe local checks; do NOT block review on a dirty tree

If verification is skipped or partial, record it. Missing verification is not passing verification.

## STEP 7: Prepare review artifact

There is one review artifact per target, independent of whether the target is a task, PR, branch,
range, or working tree. Resolve the path in this order:

1. Reuse an existing review path linked from the selected task record.
2. Otherwise use `<resolved-task-root>/code-review-[target].md`, sanitizing `/` and spaces in the
   target. This keeps non-task reviews with the same durable task context instead of creating a
   competing `.claude/reviews` tree.
3. If an existing legacy review file is found, preserve it in place and link that path; never rename
   it merely to fit this convention.

For a read-only review, report the proposed or linked path and skip all artifact writes in this step
and later steps. For a writable re-review, retain the prior revision and evidence; append a new
revision block or update only the new revision after findings are ready. Do not clear the old review
before a replacement exists, and do not create a second file for the same target.

If no writable artifact exists, create it from `.claude/docs/templates/code-review-template.md` under
the resolved task root.

## STEP 8: Dispatch Agents

Pass the common target context to every reviewer and request an inline structured finding/result.

Dispatch **all agents selected in STEP 5 in a single turn** when the host supports independent
parallel calls; otherwise run the same selected passes sequentially without reducing coverage.
Reviewers return findings; the single orchestrator writes the shared `cr_file_path` after all results
arrive. Disjoint `<!-- SECTION:xxx -->` markers are layout, not a concurrency guarantee.

If an agent fails or times out, the orchestrator writes a fallback note into its section:
`*Review skipped — [agent-name] did not complete.*`

Once every dispatched agent has finished, proceed to STEP 9.

## STEP 9: Write Verdict

If the request is read-only, return the inline findings, observed verification, and proposed or
linked artifact path, then stop. Do not write the review file or task record.

The orchestrator writes the remaining sections that agents do not own:

- `review-context` — fill from STEP 2 capabilities
- `summary` — synthesize a 2-5 sentence note from agent findings
- `verdict` — one of the verdicts below
- `key-findings` — consolidate actionable findings from all agents. Include every CRITICAL and MAJOR regardless of confidence. For MINOR/INFO, include items marked `confidence: high`; drop or collapse `confidence: low` MINOR/INFO into a single "Other low-confidence notes" bullet. Order by severity, then confidence. **Structural `[OPPORTUNITY]` findings** (deep scope) go in a dedicated "Structural Opportunities" sub-block — they surface prominently but do NOT count toward the verdict; route them to `/prc` or a follow-up task.
- `coverage` — record what was reviewed and what was skipped
- `verification` — record commands run and results
- `metadata` — changed files, diff source, reviewers invoked

Use the **Edit tool** to append the new orchestrator revision or update its own markers in
`cr_file_path`. Do NOT overwrite the entire file — prior revisions and reviewer results remain
evidence.

After writing the verdict, link the review artifact and observed result from the resolved task record,
including the next action. One orchestrator owns the shared review file; reviewer agents return findings and never rely on
parallel writes being safe merely because markers are disjoint.

Verdicts:
- `DRAFT REVIEW`: working-tree review or no immutable snapshot
- `APPROVED`: committed snapshot, sufficient coverage, `0 critical`, `0 major`
- `APPROVED WITH NOTES`: committed snapshot, `0 critical`, `0 major`, but verification or coverage is partial
- `NEEDS FIXES`: any critical or major finding (including structural CRITICAL/MAJOR from deep scope; `[OPPORTUNITY]` findings never trigger this)

Never return `APPROVED` for an uncommitted working-tree draft.

## STEP 10: QA Gate Recommendation

After the verdict is written, check whether the diff affects user-facing rendering — any file that produces DOM output, styling, or routing state. Use this list as a seed, not a limit: `.svelte`, `.tsx`, `.jsx`, `.vue`, `.html`, `.astro`, `.mdx`, CSS/SCSS, component stories, route files. When in doubt, treat it as UI. If it qualifies, append a **QA recommendation** to the review file:

> **QA recommended**: This review includes UI changes. Static code review cannot catch runtime layout, navigation, or user-flow issues. Consider running browser-based QA (manual or automated) before merging.

This is a recommendation, not a blocker. It surfaces the gap between "code looks correct" and "feature works correctly."

## Operating Reminders

Three gates are worth re-stating because mis-handling them corrupts the review file:

- One review artifact per target — reuse the linked/legacy path and retain prior revisions (see STEP 7).
- Pass the same target context to every dispatched reviewer; only the orchestrator writes
  `cr_file_path` after results arrive (see STEP 8).
- Use Edit, not Write, on `cr_file_path` while preserving all reviewer results (see STEP 9).

## Red Flags

- Writing a verdict without having read the actual changed code.
- Approving with zero findings and zero stated verification.
- Claiming spec compliance when no spec/task artifact exists.
- Every finding tagged the same severity (all critical, or all nits).
- Reviewing only the literal diff when the change clearly integrates with earlier phases.

## Related Skills

| Need | Use |
|------|-----|
| Address review feedback | `/prc` |
| Formal tracked implementation | `/si` |
| Explore code before reviewing | `/code-analysis` |
