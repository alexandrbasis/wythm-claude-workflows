# Implementation checklists — reference

> Loaded by `/si` STEP 3. Passive lookup data for the TDD loop: test-assertion anti-patterns, the
> mutation/async safety checklists, and the off-spec journal format. The TDD control flow itself
> (RED → GREEN, per-step gates) stays in `SKILL.md`.

## Test assertion quality (anti-pattern prevention)

- **NEVER** assert with `> 0`, `.toBeTruthy()`, or `.toHaveLength(expect.any(Number))` for
  enumerated data.
- **ALWAYS** assert exact values: `.toHaveLength(28)`, `.toEqual(["Corporation", "LLC", ...])`.
- **ALWAYS** assert exact field counts when the spec enumerates fields.
- When writing a test for a list/enum/options, use the exact expected set or count stated by the
  requirement or existing evidence map. If the test passes with `> 0` but the requirement says 28
  options, the test is WRONG even though it's green.

## Mutation & async safety checks

Apply whenever the current step creates, updates, or deletes entities, or involves async callbacks.
Skip for steps with no mutations or async UI interactions.

**Post-mutation UX checklist:**
- Is the async call awaited by the UI event handler (not fire-and-forget)?
- Does the caller show success feedback or navigate to a visible result?
- Does the caller refresh every local state snapshot that depends on the mutation?
- Are semantic defaults set (category, type, order, visibility) — not just technically required fields?
- If the current screen cannot display the new entity, is that intentional and documented?

**Async callback checklist:**
- Is the callback marked `async` and does it `await` the mutation?
- Does the caller have `try/catch` with a user-visible error state?
- Does a modal/dialog/overlay close only after the async chain resolves (not before)?
- If the operation can fail, is there a rollback or cleanup path for partial writes?

## Journal off-spec changes

The task document is the *plan*; the `## Deviations & Decisions` section is the *journal* —
append-only, dated, capturing reality that diverged from the plan. Reviewers (`/sr`) and future
maintainers read it to understand *why* the diff doesn't match the spec.

**When to write an entry:**
- A decision the spec didn't cover (e.g., chose `Map` over plain object for ordering; spec said
  "key-value store").
- A deviation from a planned acceptance criterion (e.g., skipped optimistic update because the cache
  invalidation tree was shared with another feature).
- A tradeoff the user didn't pre-approve (e.g., shipped O(n²) loop because n ≤ 50 in practice and the
  optimal version required a new index).
- A scope-narrow or scope-expand that survives the step (not a transient mid-step thought).

**When NOT to write:**
- The step matched the spec exactly — silence is the signal.
- TDD cycle internals (RED → GREEN refactors) — only the surviving outcome matters.
- One entry per deviation, not one per step.

**Entry format** (append under `## Deviations & Decisions` in the task document; create the section if
missing):

```markdown
### 2026-MM-DD — [Short title]
- **Step**: Sub-step 3.2
- **Type**: Decision | Deviation | Tradeoff | Scope change
- **What**: one sentence — what you did instead of / on top of the spec
- **Why**: the constraint that forced it
- **Impact**: what reviewers / future maintainers need to know (perf, rollback path, follow-up needed)
```

**Parallel mode**: workers return deviation drafts in their final message under a `## Deviations`
heading; the orchestrator merges them into the task document's journal once after the wave.
