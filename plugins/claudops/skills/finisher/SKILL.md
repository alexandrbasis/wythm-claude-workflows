---
name: finisher
description: Ship an existing implementation by committing local changes, pushing an open PR, waiting for green CI, and merging
  it. Use when the user explicitly asks to 'merge the PR', 'ship it', 'merge and close', 'commit push merge', 'finalize this
  PR', or 'land this branch'. Do not trigger on generic end-of-work language without a resolved PR or branch destination.
  This flow works with or without a task directory; phase handoff details live in Gate 3. NOT for opening a new PR (use plain
  `gh pr create`). NOT for addressing review comments (use /prc). NOT for preparing a session handoff to a fresh context (use
  /ph).
argument-hint: '[task-or-phase-directory] [--no-merge]'
allowed-tools:
- Bash
- Read
- Edit
- Glob
- Grep
- AskUserQuestion
- TodoWrite
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/finisher/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/finisher/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Finisher

> **Announcement**: Begin with: "I'm using the **finisher** skill to ship this work — commit, push, wait for green CI, then merge."

## PRIMARY OBJECTIVE

Land the current implementation on the base branch with the PR cleanly merged. The skill is **universal**: it works on any branch with an open PR. There does **not** need to be a task directory, a tech-decomposition document, or a phase structure. If those things happen to exist, the skill picks them up and uses them; if not, it just ships the PR.

Before merging:

1. Commit and push any pending local changes onto the PR branch.
2. **(Conditional)** If the current work is one phase of a multi-phase task, make the upcoming phase tech-decomposition documents accurate for the implementation that just landed: add handoff notes, update stale assumptions, or explicitly record the evidence-backed reason no changes were needed. Skip silently only when this is not a split phase.
3. Wait for CI to be green. Do not merge or stop on red CI.
4. Merge the PR.

This skill is the close-out counterpart to `/si` (implement) and `/sr` (review). It assumes review has already happened and the user is ready to ship.

Resolve one task context with `../setup/references/task-context.md` before the PR gates. Reuse the
linked task or create the minimum record in the configured task root; a PR-only flow still records
the PR, CI, merge state, and next action there. Existing conversation authorization remains
authoritative, and merge remains a separate confirmation boundary.

## RELATED SKILLS

- `/sr` — Code review before merge. Run **before** this skill.
- `/prc` — Address review comments. Run before this skill if reviewers left feedback.
- `/ph` — Mid-implementation handoff to a fresh chat session. Different concern: `/ph` snapshots in-flight state for **the same task in a new chat**. This skill ships finished work to main; for split tasks it can also propagate information **between sibling phase tasks** at completion time, but that's a side concern, not the main job.
- `/udoc` — Documentation update + changelog. The user may want this run before merging; ask if relevant.

---

## GATE 1: Resolve PR (and optionally task)

### Step 1: Resolve PR (required)

```bash
git branch --show-current
gh pr view --json number,title,url,state,mergeable,baseRefName,headRefName,statusCheckRollup
```

If no PR exists for the branch, stop and ask the user whether to create one (`gh pr create`) or whether they invoked the wrong skill.

If the PR is already merged, report that and stop — the work is already shipped.

If the PR is in **CLOSED** (not merged) state, stop and ask the user how to proceed.

### Step 2: Resolve Task Context and Directory

Resolve the task context using `../setup/references/task-context.md`. The skill works with or without
a formal decomposition, but it must link the selected task record before continuing. Only enrich Gate
3 when a phase is actually resolved; record “not applicable” for a PR-only task.

1. If `$ARGUMENTS` includes a path, treat it as the task or phase directory and resolve its existing
   task entrypoint (formal decomposition or compact `TASK.md`). If the path does not exist, surface
   that to the user — they pointed somewhere specific, so do not silently ignore it. A compact task
   record is valid for PR-only close-out; only the conditional phase handoff needs formal phase docs.
2. Otherwise, look at the project root:
   - If there's no `tasks/` directory or no matching decomposition, use the minimum task record from
     the resolver and continue with PR-only flow. Do **not** invent spec claims from PR metadata.
   - Otherwise use the task-context resolver's linked active task or configured repository
     convention. If no matching task record exists, use the minimum record for PR-only evidence.
     Do not infer a specification from PR metadata. If several records remain plausible, ask once
     which task is being closed out, or accept "none" for PR-only flow.
3. If a task is resolved, capture:
   - Task name and goal
   - Whether it lives directly under `tasks/` (single task) or inside a `phase-N-*/` subfolder (one phase of a split task)
   - The parent task directory if this is a phase

**Why this matters:** The phase-handoff step in Gate 3 only fires when the resolved task is inside a
`phase-N-*/` folder. A minimum task record still indexes the PR-only evidence and next action.

### Step 3: Working Tree Snapshot

Run these in parallel:

```bash
git status --short
git diff --stat
git diff --cached --stat
git log --oneline @{u}..HEAD   # local commits not yet pushed
```

Hold this snapshot — Gate 2 commits, Gate 3 looks at completion summary, Gate 4 pushes.

---

## GATE 2: Commit Local Changes

### Step 1: Decide What Goes In

If the working tree is clean and there are no unpushed local commits, skip ahead to Gate 3 (handoff check) and Gate 4 (push is a no-op).

Otherwise, present what's pending:

- Modified/staged/untracked files (from `git status --short`)
- Diff summary (from `git diff --stat` and `--cached --stat`)
- Local-only commits (from `git log @{u}..HEAD`)

Ask the user:
- Confirm which files to include. Stage **specific files by name** — never `git add -A` or `git add .` (could pull in secrets, scratch files, or `tasks/` debug output).
- Confirm the commit message. Default to a single focused message describing the final delta; squash trivial scratch commits into the description if helpful.
- Reuse explicit push authorization already granted in the current task/session for this branch or PR
  (for example, `commit-push-merge` or `ship/merge this PR`). Ask only when the push destination or
  operation is new or unclear. Approval to commit alone does not authorize pushing.

### Step 2: Commit

Use a heredoc-style commit (the harness `Bash` tool guidance requires this for proper formatting):

```bash
git add <specific files>
git commit -m "$(cat <<'EOF'
<subject line>

<optional body>
EOF
)"
```

Do not pass `--no-verify`. If a pre-commit hook fails, **fix the underlying issue** and create a new commit — never amend or skip hooks. The hook exists for a reason.

---

## GATE 3: Phase Handoff / Next-Phase Accuracy Check (Conditional)

**Only run this gate if the current task lives inside a `phase-N-*/` folder under a parent task directory.**

For a single (non-split) task, skip directly to Gate 4.

This gate is mandatory for split phases and must be evidence-backed. Do not satisfy it by noticing that a future doc mentions the broad topic; verify that the future doc is accurate enough for the next implementer to use the actual modules, functions, contracts, caveats, and deferred work that just landed.

### Step 1: Identify Upcoming Phases

```bash
# From the parent task directory (the one containing all phase-N-*/ folders):
ls -d phase-*/ | sort
```

The current phase is `phase-K-*`. Upcoming phases are `phase-N-*` for `N > K`.

If there are no upcoming phases (this is the final phase), record that and skip to Gate 4.

### Step 2: Identify Handoff-Worthy Information

Read the current phase's tech-decomposition document, review-fix notes, code review file if present, and actual implementation diff. Then read the relevant parts of each upcoming phase document and look for things that **the upcoming phases must know but might not yet reflect**:

- **Decisions made during implementation** that diverged from the original plan (renamed module, swapped library, schema change, feature flag added).
- **Contract changes** — new exports, changed function signatures, new endpoints, changed event shapes that upcoming phases consume.
- **Deferred work** explicitly handed to a later phase ("X is stubbed; phase 3 wires it up").
- **Gotchas / surprises** discovered during implementation (test infra quirk, race condition workaround, ordering constraint).
- **New file or module locations** that upcoming phases reference.
- **Stale next-phase wording** — generic names, old flag names, assumed generated types, or requirements that no longer match the implemented contract.

Sources to mine: `Completion Summary`, `Implementation Decisions`, `Notes`, `Deferred Follow-ups`, code review findings/fixes, and the actual diff (`git diff $(git merge-base HEAD <base>)..HEAD --stat`) — sometimes decisions live in code but never made it back into the doc.

For each upcoming phase, explicitly check at least these evidence categories before deciding whether a handoff is required:

- **Actual exports and file paths**: hooks, services, ports, utilities, screens, route helpers, config keys, event names, and generated DTO aliases that upcoming phases will import or call.
- **Contract shape and naming**: function signatures, route/query params, React Query keys, DTO field names, normalized error codes, and callback/mutation return values.
- **Behavioral caveats**: temporary NoOp adapters, dependency-blocked native wiring, deferred analytics, fallback behavior, consent gating, cache invalidation, async error handling, and known local-vs-remote verification gaps.
- **Upcoming doc wording**: requirements, test cases, implementation decisions, file lists, dependencies, and risks that mention the implemented surface.

Write down the comparison result in your working notes before Gate 4:

```text
Phase handoff check:
- Current phase: phase-K-...
- Upcoming phases checked: phase-N-...
- Evidence checked: <actual files/diff/docs reviewed>
- Updates needed: <yes/no>
- If no updates: <specific reason each upcoming phase doc already matches actual implementation>
```

If the upcoming phase docs already reflect the implementation accurately, say so explicitly with the evidence summary and skip to Gate 4. Empty handoffs are honest; padding them dilutes the signal in real ones. Do not skip just because a broad topic is mentioned; verify the wording is precise enough for the next implementer to use without re-discovering current-phase results. If the wording is accurate at a high level but misses concrete names, paths, contracts, or caveats, a handoff update is required.

### Step 3: Propose Updates Per Upcoming Phase

For each upcoming phase, propose **only** the items relevant to that phase. Do not blanket-copy the same notes everywhere. Proposals may either append a handoff note or directly update stale requirements/tests/decision rows in that phase document.

Every proposed item must cite the concrete implementation evidence that triggered it: file path, exported symbol, committed diff behavior, or review-fix note. If you cannot point to implementation evidence, do not add the item.

Present the proposal as a table:

```
| Phase | Doc | Item to add | Why this phase needs it |
|-------|-----|-------------|--------------------------|
| phase-2-session-join | tech-decomposition-phase-2-session-join.md | "Profile lookup now returns `{ id, displayName }` (renamed from `name`)" | Phase 2 calls this endpoint |
| phase-3-presence | tech-decomposition-phase-3-presence.md | "Feature flag `presence_v2` controls rollout" | Phase 3 toggles behavior on this flag |
```

Use `AskUserQuestion` to confirm: approve, edit, or skip items. Only apply approved items. If the user has already given an explicit blanket instruction to enforce handoffs automatically, you may apply obvious accuracy fixes directly, but still summarize them before Gate 4.

### Step 4: Apply Updates

For each approved item, update the upcoming phase's tech-decomposition document so it is accurate for implementation. Prefer the smallest useful edit:

- Replace stale wording in existing requirements/tests/decision rows when the existing text would mislead implementation.
- Append a clearly marked handoff subsection when the information is new context rather than a correction.

For additive handoffs, use:

```markdown
### Handoff from phase-1-profile-lookup (added 2026-04-27)

- Profile lookup endpoint now returns `{ id, displayName }` (renamed from `name`)
  in commit abc1234. All consumers in this phase must use the new field.
```

Date-stamp the heading so future readers can tell when the note was added.

### Step 5: Commit Handoff / Next-Phase Updates

If any upcoming phase docs changed:

```bash
git add <specific upcoming phase tech-decomposition files>
git commit -m "docs: update upcoming phase handoff from <current-phase>"
```

Keep this commit separate from the implementation commit — it touches different files for a different reason and may need to be reverted independently.

If no upcoming phase docs changed, do not create a commit. Carry the evidence-backed "upcoming phase docs already accurate" result into the final merge confirmation and final summary.

---

## GATE 4: Push & Wait for Green CI

### Step 1: Push

Before pushing, verify that the current task/session explicitly authorizes pushing this branch or
PR. Reuse that authorization without asking again. If the request only says "finish" or leaves the
destination unclear, stop after the local commit and ask whether to push.

```bash
git push
```

If the branch has no upstream yet, set it: `git push -u origin <branch>`.

### Step 2: Wait for CI

```bash
gh pr checks --watch
```

`--watch` blocks until all checks complete. Do not stop early; do not declare success based on partial results.

If checks pass: continue to Gate 5.

If checks fail:
- Capture the failing check names and any log excerpts: `gh pr checks` (without `--watch`) shows the final state.
- **Stop and report to the user.** Do not merge. Do not declare the skill complete. The user's instruction was explicit: CI must be green before stopping.
- Offer to investigate (read failing job logs via `gh run view <run-id> --log-failed | tail -100`) but do not auto-fix without approval — a CI failure may indicate a real bug or a flaky test, and the right action depends on which.

If checks are stuck "queued" or "in_progress" for an unreasonable time, surface that too — sometimes a runner is wedged and the user needs to retrigger manually.

After a successful push and green checks, read back the remote head and PR status. The pushed commit
and the checked PR head must match before continuing.
Link the observed head and CI result from the selected task record before presenting merge confirmation.

---

## GATE 5: Merge

### Step 1: Final Confirmation

Before presenting the merge confirmation, consume the review evidence required by the user, task, or
repository. Accept the latest provider review status or a local review artifact when that workflow
created one. This universal PR-only flow does not require inventing a local artifact when no such
review was requested or configured. If required evidence is missing or unresolved, surface that
state before merge.

Before merging, summarize for the user:

```
Ready to merge:
- PR: #NN — <title>
- Base: <base-branch>
- Head: <feature-branch>
- Commits being merged: <count>
- CI: all checks green
- Phase handoff: <"updated N upcoming phase docs" | "upcoming phase docs already accurate" | "not applicable">
```

Ask once: "Merge now?" Use `AskUserQuestion`. Merging is hard to reverse cleanly (especially after the branch is deleted), so confirm even in auto-mode flows.

### Step 2: Merge

Use the merge method the project prefers. If unsure, ask. Common options:

```bash
# Squash (most projects' default)
gh pr merge <PR#> --squash --delete-branch

# Merge commit
gh pr merge <PR#> --merge --delete-branch

# Rebase
gh pr merge <PR#> --rebase --delete-branch
```

`--delete-branch` removes the remote branch after merge. Skip it if the project keeps merged branches around (rare).

### Step 3: Verify Merge Succeeded

```bash
gh pr view <PR#> --json state,merged,mergedAt
```

Confirm `merged: true`. If not, surface the error from `gh` and stop.
Record the observed merge state and local cleanup result in the selected task record. Do not report
completion from a planned command or partial status.

### Step 4: Local Cleanup

Switch back to the base branch and pull:

```bash
git checkout <base-branch>
git pull
git branch -d <feature-branch>   # safe delete; refuses if unmerged
```

If `git branch -d` refuses, do **not** force-delete with `-D` automatically — that would silently discard work. Surface it to the user; it usually means the local branch has commits the remote PR didn't (e.g., something committed after the last push).

---

## OUTPUT FORMAT

Final summary:

```
## Shipped: <PR title>

**PR**: <url> (merged at <timestamp>)
**Base**: <base-branch>
**Commits merged**: <count>
**CI**: all green (<N> checks)

### Phase handoff
<one of>
- N/A (single task, not a phase)
- Final phase — no upcoming phases to update
- Upcoming phase docs already accurate — no changes needed
- Updated <count> upcoming phase docs:
  - phase-2-session-join: <one-line summary of what was added>
  - phase-3-presence: <one-line summary>

### Local
- Switched to <base-branch>, pulled latest
- Deleted local branch <feature-branch>
```

---

## STOP CONDITIONS (do not declare success if any of these hold)

- CI is not green. Failed, cancelled, or still-running checks all count as not-green. The user's instruction is explicit on this.
- The PR is not in `merged: true` state after Gate 5.
- An approved handoff update silently failed to apply (file write error, merge conflict in upcoming phase doc).

In any of these cases, report the actual state honestly and let the user decide next steps. Optimistic summaries that mask failures cost the user real debugging time later.

---

## Red Flags

- Merging while any check is failed, cancelled, or still running.
- `git add -A` / `git add .` instead of staging by filename.
- Any use of `--force`, `--force-with-lease`, or `--no-verify`.
- Declaring "Shipped" when the PR is not in `merged: true` state.
- Skipping Gate 3 handoff updates on a multi-phase task.

---

## NOTES ON SAFETY

- Never use `--no-verify`, `--force`, `--force-with-lease`, or `git push -f` from this skill. Pushing to a PR branch is normal `git push`; if it's rejected, that's a signal something changed remotely (someone else pushed, a bot rebased) and the right move is to investigate, not overwrite.
- Never `git add -A` or `git add .`. Stage by filename so you don't accidentally commit `.env`, scratch files in `tasks/`, or local debugging artifacts.
- The `--no-merge` argument lets the user run everything up to (but not including) Gate 5, useful when they want CI green and handoff notes applied but want to merge manually via the GitHub UI.
