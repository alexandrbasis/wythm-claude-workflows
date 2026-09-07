# Mutation and async checks

Read when the changed behavior creates, updates or deletes entities, or uses asynchronous
interactions. Apply the relevant checks through the repository's framework and state model.
Queues, framework-managed mutations and optimistic updates may own completion and recovery;
verify the responsible mechanism rather than prescribing syntax in every caller.

- **Outcome:** verify the promised postcondition at the relevant boundary: response, event,
  persisted state or UI. Include required defaults and expected absence after deletion. For UI
  work, check affected views and cached/local state so they reflect the actual result.
- **Completion and failure:** identify who owns pending, success and error handling. The caller
  must observe completion or hand it to a mechanism that does; success feedback must match the
  task's promised outcome. Verify failure behavior where the operation can fail.
- **UI transitions:** closing a dialog or navigating early is valid only when the intended
  optimistic/background flow keeps status and recovery available. A failed operation must not
  silently look completed.
- **Consistency:** inspect partial-write and concurrency risks where applicable. Use the
  project's transaction, rollback, retry or cleanup behavior as appropriate; verify that an
  interrupted or failed operation leaves the required data and UI state consistent.

Choose checks that prove the affected behavior, and record their evidence in the existing task.
Routine implementation choices need no journal entry. Record only material decisions or
changes to the agreed plan, with what changed, why and its effect; reuse the task's existing
notes format. Workers return these notes for the orchestrator to consolidate.
