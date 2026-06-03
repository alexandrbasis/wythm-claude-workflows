# Spec Verification Gate — reference

> Loaded by `/si` STEP 1.5. The gate's control flow lives in `SKILL.md`; this file holds the VC
> entry format, the type catalog, and the per-type verification recipes. Purpose: prevent the #1
> incident type — partial implementation of specs — by making a countable, verifiable contract
> before any code is written.

## VC entry format

Each Verification Checklist item is one line:

```
- [ ] `VC-001` | TYPE: field | NAME: fieldName | REQ: REQ-XXX | SPEC: text input, max 100 chars | TEST: assert field renders
```

When the task document has no `## Verification Checklist` section, generate it from the requirements,
test plan, and implementation steps: scan every requirement (`REQ-XXX`), test case (`TEST-XXX`), and
must-have, and create one `VC-NNN` entry per discrete verifiable item.

## VC type catalog

`field`, `option`, `behavior`, `ui-element`, `api-call`, `validation-rule`, `error-state`,
`navigation`, `state-change`.

## Per-type verification recipes

When verifying a VC entry against the actual code (STEP 1.5 per-step and final passes):

| TYPE | How to verify (in the real code) |
|---|---|
| `field` | grep for the field name in the component/form |
| `option` | count exact options in code, compare to spec count — **exact match required** |
| `behavior` | run the relevant test, confirm it passes |
| `ui-element` | confirm the element exists in render output |
| `api-call` | confirm the endpoint URL and payload match spec |
| `validation-rule` | confirm the validation logic exists |
| `error-state` / `navigation` / `state-change` | confirm the behavior exists in code and is covered by a passing test |

Mark verified: `- [ ] \`VC-001\`` → `- [x] \`VC-001\``. If an entry cannot be verified, DO NOT mark
it — flag it and implement before moving on.

## Coverage rule

Every VC entry must be covered by at least one implementation step. If an entry is uncovered, flag it
immediately and assign it to a step:

> WARNING: VC-007 (businessType options) is not covered by any implementation step. Adding to Step N.

## Gate outcome

Final count: checked vs total. If checked < total, list every unchecked entry and implement it before
cleanup. Announce: `Verification: X/Y items checked. [PASS/FAIL]`. **FAIL blocks moving to
cleanup/review** — all VC entries must be checked.
