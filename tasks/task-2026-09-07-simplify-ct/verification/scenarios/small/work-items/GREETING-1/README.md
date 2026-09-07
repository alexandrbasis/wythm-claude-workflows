# Trim surrounding whitespace in greetings

Objective: greet(name) ignores surrounding whitespace while preserving whitespace inside the name. Existing greeting punctuation stays unchanged.
Stage / status: ready for implementation.

## Agreed acceptance
- `greet("  Alex  ")` returns `Hello, Alex!`.
- `greet("Ann  Lee")` returns `Hello, Ann  Lee!`.
- An empty or whitespace-only name returns `Hello, !`.

## Context
This task is implementation planning only. The behavior above is settled.

## Technical plan
Stage / status: ready for implementation.

### Changes
- Update `greeting.py:greet` to trim leading and trailing whitespace from `name` before interpolation, while leaving internal whitespace unchanged.
- Extend `tests/test_greeting.py` with coverage for surrounding whitespace, internal repeated whitespace, and empty or whitespace-only names.

### Steps
1. Change `greet` to use the trimmed name in the existing greeting format.
2. Add tests for the three accepted behaviors above.
3. Run `python3 -m unittest discover -s tests -q` from the repository root.

### Verification
The planned unittest command must confirm:
- `greet("  Alex  ") == "Hello, Alex!"`.
- `greet("Ann  Lee") == "Hello, Ann  Lee!"`.
- Empty and whitespace-only names return `"Hello, !"`.

The checks are planned and were not run during this planning stage.

### Risks and decisions
Use Python's standard `str.strip()` so only boundary whitespace changes; this preserves the settled internal-whitespace behavior and requires no migration, external contract, or split work.

## Progress and next action
Readiness was checked against the settled outcome, inspected code and tests, ordered steps, and the repository test command. No material blocker remains; implementation has not started. Next action: hand this ready plan to `/si work-items/GREETING-1/README.md`; implementation requires its own authorization.
