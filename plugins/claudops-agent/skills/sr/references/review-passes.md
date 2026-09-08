# Targeted Review Passes & Pattern Propagation — reference

> Loaded by `/sr` STEP 5.4/5.5. The review pipeline's control flow lives in `SKILL.md`; this file holds
> the trigger table and per-pass checklists. These passes are **orchestrator-owned inline checks**, not
> subagents — no subagent file exists for them. Run the matching pass when the diff hits its trigger and
> add findings to `key-findings`.

## Targeted review passes

### Error-path pass

**Trigger:** diff contains `async` / `await` / `.then(` / `Promise`.

- For each async call chain: what happens if it throws? Where does the error propagate?
- Does the caller have try/catch with a user-visible error state?
- Does a modal/dialog/overlay close before the async chain resolves?
- Are there multi-step write operations that lack atomicity (if step 2 fails, step 1 is orphaned)?

### Integration-seams pass

**Trigger:** diff crosses component/module boundaries.

- Data passed through navigation or routing (are all required params forwarded?)
- Callback shapes: does the caller await the callback? Does it handle errors?
- State subscriptions: after a mutation, is every dependent state snapshot refreshed?
- Modal/dialog lifecycle vs async operations: does the UI update only after resolution?

### Cross-surface entity pass

**Trigger:** diff creates, updates, or deletes entities.

- Does the entity appear correctly on its canonical management/list surface, not just the origin screen?
- Are semantic defaults set (category, type, grouping, order)?
- Is there success feedback visible to the user after the operation?

## Pattern propagation

When a reviewer flags a major or critical finding, scan sibling files for the same anti-pattern before
finalizing. Sibling occurrences are often where the real bug lives — the flagged file is frequently just
the first place it was spotted.

- Spend up to ~5 minutes scanning.
- Stop at 5 sibling occurrences, or when coverage of plausible locations (same module, same layer, same
  call-site shape) is exhausted — whichever comes first.
- Record findings in `key-findings` even if those files are outside the current diff; if clean, record
  "scanned N files, no sibling occurrences".
