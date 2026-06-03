---
name: si
description: >-
  Implements a feature from a technical decomposition using TDD, keeping the task document updated
  and handing off cleanly to review. Use when starting, continuing, or resuming implementation from a
  tech-decomposition or task directory. Trigger: 'implement this task', 'start implementation',
  'continue/resume implementation', 'build from the tech decomposition', or after /ct produces a
  decomposition. NOT for creating the plan (/ct), feature discovery (/nf), small untracked changes
  (/si-quick or /quick), or code review (/sr).
argument-hint: [task-directory | tech-decomposition-path]
allowed-tools: [Agent, AskUserQuestion, Edit, Read, Write, Bash, Glob, Grep, Skill, TodoWrite]
---

# Start Implementation Command

> **Announcement**: Begin with: "I'm using the **si** skill for structured TDD implementation."

## Quick start
`/si tasks/task-2026-05-31-streak-freeze` → validate doc (STEP 1) → spec-verification gate (STEP 1.5)
→ branch + status (STEP 2) → TDD implement, per-step verify + journal (STEP 3) → cleanup (STEP 4) →
PR + handoff to `/sr` (STEP 5).

## Primary objective
Implement from a technical decomposition with TDD, lightweight task-document updates, and a clean
handoff into review.

## Constraints
- Follow the active tech-decomposition / task document as the source of truth.
- Document lifecycle: `Technical Review` → `In Progress` → `Implementation Complete`.
- **TDD discipline** is canonical from `.claude/skills/tdd/SKILL.md` — vertical slices only (one
  RED→GREEN per behavior). Horizontal slicing (all tests, then all code) is forbidden.
- **LLM limitations awareness**: consult `.claude/docs/references/llm-mental-model.md` in "brittle
  zones" (counting, long lists, visual properties) and add explicit verification steps there.
- Domain terminology is canonical from `product-docs/UBIQUITOUS_LANGUAGE.md` (if present) — use its
  terms verbatim in code identifiers, commit messages, and test names.
- Context is compacted automatically. Don't stop early over token concerns — persist progress to the
  task document after each step so a fresh window can resume from the same state.

---

## STEP 1: Task Validation
1. **Validate document**:
   - Confirm task exists (direct `tech-decomposition-*.md` path OR task directory containing one).
   - Confirm required sections exist: `Primary Objective`, `Must Haves`, `Test Plan`, and
     `Implementation Steps`.
   - Confirm task status is appropriate — ask before proceeding if unclear.
   - Confirm requirements and steps are specific enough to implement without guessing.
   - If the document is missing core structure, stop and ask the user to clarify.

---

## STEP 1.5: Spec Verification Gate
> **Purpose**: prevent the #1 incident type — partial implementation of specs — by creating a
> countable, verifiable contract before any code is written.

1. **Extract / generate the checklist**: read the task document's `## Verification Checklist`. If
   absent, generate it now — one `VC-NNN` entry per discrete verifiable item from every requirement,
   test case, and must-have. Format, type catalog, and per-type verification recipes live in
   **`references/verification-gate.md`** — read it now.
2. **Count and announce**: "Verification Checklist contains N items. All N must be checked before
   implementation is complete."
3. **Map VC entries to steps**: for each implementation step, list the VC entries it covers. Flag any
   uncovered entry immediately and assign it to a step.
4. **Per-step verification** (during STEP 3): re-read the step's VC entries from the task document
   (don't rely on memory), verify each in the real code using the recipes, and mark `- [x]` only when
   confirmed. If an entry can't be verified, flag it and implement before moving on.
5. **Final verification** (before STEP 4): count checked vs total. If checked < total, list every
   unchecked entry and implement it. Announce "Verification: X/Y items checked. [PASS/FAIL]" — **FAIL
   blocks cleanup/review.**

---

## STEP 2: Setup
1. **Update task status** to "In Progress" with timestamp.
2. **Create feature branch** (permission gate) if needed: `feature/team-[ID]-[slug]` or the repo
   convention.
3. **Update `Tracking`** with the branch name once it exists.

---

## STEP 3: Implementation

### Parallelization
When two or more steps meet the criteria below, spawn all eligible developer-agent workers in a single
assistant message via `.claude/skills/parallelization/SKILL.md`. Don't default to sequential — if the
task document has wave annotations or independent modules, parallel is the expected path. Sequential is
the fallback when independence is unclear.

**Wave detection**: if the task document has wave annotations (e.g., `— **Wave 1**`, `— **Wave 2**`),
group steps by wave and run all same-wave steps in parallel before advancing. Otherwise use the matrix
below.

- **Parallelize when**: steps modify different modules/dirs with no shared state; independent test
  suites; steps annotated with the same wave number.
- **Do NOT when**: steps touch the same files or depend on a prior step's output; database migrations
  (order matters); steps that share test fixtures or DB state.

**Worker doc-edit rule**: in parallel mode, workers do not edit the task document or other shared
files. Workers return their checkbox diffs (and any deviations) in their final message; the
orchestrator consolidates all document updates once after the wave merges.

### Sequential Mode

#### Before each step
1. **Announce**: "Starting Step [N]: [Description]".
2. **Review**: acceptance criteria, tests, artifacts for this step.

#### During implementation (TDD)
1. **Stay in scope**: implement what the step asks, nothing more. No new abstractions, adjacent
   refactors, or defensive handling for impossible cases — surrounding cleanup belongs in STEP 4.
2. **Follow the agreed Test Plan** from the task document.
3. **RED before GREEN**: each new behavior starts with a failing test that fails for the right reason.
4. **One behavior per cycle**: keep each RED → GREEN → REFACTOR loop narrow.
5. **No retroactive tests**: if implementation got ahead of the test, stop and return to RED. If
   fixing that would revert shared or user-authored work, ask first instead of deleting blindly.
6. **Update docs during code changes**.
7. **Use repo-appropriate verification commands** from the task doc or package scripts — quiet variant
   for routine loops, full output when debugging a failure.
8. **Verification gate**: the tests named for the active step must pass before you mark it complete.

For test-assertion anti-patterns (exact counts vs `> 0`), the mutation/async safety checklists, and
the off-spec journal format, read **`references/implementation-checklists.md`**. Apply the
mutation/async checklist whenever a step creates/updates/deletes entities or uses async callbacks.

The task document is the source of truth — read the files it names, implement against its acceptance
criteria, and stop exploring once you have the context for the current step.

#### After each step
1. **Update task document**:
   - Mark step checkbox: `- [ ]` → `- [x]`.
   - Update the step `**Tests**` field with command + result, or an explicit skip reason.
   - Mark Test Plan checkboxes if applicable.
   - Refresh `Tracking` / `Notes` if branch, risks, scope, or follow-ups changed.
   - **Journal off-spec changes** under `## Deviations & Decisions` if this step diverged from the
     plan (triggers + format in `references/implementation-checklists.md`). Skip if the step matched
     the spec exactly.
   - If the task doc already uses a per-step changelog, keep it updated; otherwise don't add a new
     legacy field.
   - **Parallel mode**: workers don't edit shared docs; the orchestrator updates once after merge and
     merges worker-returned deviations into the journal.

   ```markdown
   - [x] Sub-step 3.1: Update CreateSessionUseCase logic
     - **Tests**: `cd backend && npm run test:silent -- [test-filter]` - PASS
   ```

2. **Commit (permission gate)**:
   - Ask permission **before** any git write (`commit`, branch create/switch, stash apply/drop,
     `push`, `rebase`, `merge`). Read-only inspection (`git status`, `git log`) is fine.
   - Conventional commits with issue reference: code + tests `feat(scope): [summary]` + `Refs:
     TEAM-123`; docs-only `docs(scope): update [doc name]` + `Refs: TEAM-123`. Tightly coupled doc
     changes may share the code commit.

#### Self-verification (after each step)
Verify your claims across **every** file and test touched in the step — not just the first:
1. Every file listed in the step exists on disk (`ls` each).
2. Every test mentioned can be found and passes (run them).
3. If a commit was claimed, verify with `git log -1 --oneline`.
4. If a module or contract changed, run the relevant build, typecheck, or validation command.

---

## STEP 4: Completion

### Cleanup pass
If the diff accumulated obvious slop, run a focused cleanup before the final quality gate:
1. Invoke `/simplify` or do a targeted manual cleanup on changed files.
2. Re-run the relevant tests after any cleanup.
3. Commit cleanup changes separately only with approval.

---

## STEP 5: Prepare for Code Review
1. **Permission gate**: push + PR require explicit user approval.
2. **If approved, create PR**.
3. **Hand off to `/sr`** once the task document status is `Implementation Complete` and review context
   is ready.

### Finalize task document
1. **Update status** to "Implementation Complete" with timestamp.
2. **Verify all checkboxes** are accurate.
3. **Add or refresh the Completion Summary**: what changed; verification evidence (commands + results,
   quality gate path/summary); deferred follow-ups or known skips; and a one-line **pointer** to
   `## Deviations & Decisions` if it has entries (e.g., "See journal: 4 entries, 1 scope-expand, 2
   tradeoffs, 1 unplanned decision"). Don't restate — point reviewers at it.
