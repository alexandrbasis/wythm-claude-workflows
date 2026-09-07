# Evidence Map — reference

> Loaded by `/si` STEP 1.5 when a requirement needs a precise verification recipe. The control flow
> lives in `SKILL.md`; this file is optional reference material. Existing task schemas and a compact
> `TASK.md` are valid when they carry the same meaning. Do not create a parallel checklist merely to
> satisfy this reference.

## VC entry format

If a task already uses Verification Checklist items, retain their existing form:

```
- [ ] `VC-001` | TYPE: field | NAME: fieldName | REQ: REQ-XXX | SPEC: text input, max 100 chars | TEST: assert field renders
```

When no checklist exists, keep one evidence map in the resolved task record. Map each substantive
requirement, acceptance item, or test to an implementation step and observed command/artifact; do
not generate `VC-NNN` rows solely because this reference names them. Preserve existing IDs when they
already exist.

## VC type catalog

`field`, `option`, `behavior`, `ui-element`, `api-call`, `validation-rule`, `error-state`,
`navigation`, `state-change`.

## Per-type verification recipes

When verifying a VC entry against the actual code (STEP 1.5 per-step and final passes):

| TYPE | How to verify (in the real code) |
|---|---|
| `field` | grep for the field name in the component/form |
| `option` | compare exact options only when the requirement explicitly specifies the set or count |
| `behavior` | run the relevant test, confirm it passes |
| `ui-element` | confirm the element exists in render output |
| `api-call` | confirm the endpoint URL and payload match spec |
| `validation-rule` | confirm the validation logic exists |
| `error-state` / `navigation` / `state-change` | confirm the behavior exists in code and is covered by a passing test |

Mark an existing item verified only when its evidence is observed. If an item cannot be verified, do
not mark it; record the concrete blocker or untested reason in the same task record.

## Coverage rule

Every substantive requirement or acceptance item must be covered by at least one implementation
step. If an item is uncovered, flag it immediately and assign it to a step:

> WARNING: VC-007 (businessType options) is not covered by any implementation step. Adding to Step N.

## Gate outcome

Before cleanup/review, report covered, blocked, and untested items. Missing evidence blocks a
completion claim, while an untested item may remain an explicit follow-up when the task's scope or
authorization does not require that check. Announce the observed result and next action; do not
invent a countable gate when the task has no countable checklist.
