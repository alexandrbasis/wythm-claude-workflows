---
name: tdd
description: >-
  Test-driven development with red-green-refactor loop using vertical slices.
  Use when building features or fixing bugs with TDD, when /si or /si-quick
  needs canonical TDD discipline, when user mentions "red-green-refactor",
  "tracer bullets", "test-first", or asks for integration-style tests. Forbids
  horizontal slicing (all tests then all implementation).
disable-model-invocation: true
---

# Test-Driven Development

> **Upstream**: Adapted from [mattpocock/skills/tdd](https://github.com/mattpocock/skills/tree/main/tdd). Vocabulary aligned with this repo's `architecture-language/LANGUAGE.md`. Used as the canonical TDD reference by `/si` and `/si-quick`.

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe *what* the system does, not *how* it does it. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). Warning sign: your test breaks when you refactor, but behavior hasn't changed. If renaming an internal function fails tests, those tests were testing implementation, not behavior.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

**Named principles** (from *Software Engineering at Google*):

- **Beyoncé Rule** — "if you liked it, you should have put a test on it." If a behavior matters, it has a test; anything untested is fair game to break and nobody will notice.
- **Test pyramid (≈80/15/5)** — favor many fast unit tests, fewer integration tests, very few end-to-end. An inverted pyramid (mostly E2E) is slow and flaky.
- **DAMP over DRY in tests** — tests may repeat themselves for readability. A test should be obvious in isolation; don't hide its meaning behind shared helpers the way you would in production code.

## Anti-pattern: horizontal slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

This produces **bad tests**:

- Tests written in bulk test *imagined* behavior, not *actual* behavior
- You end up testing the *shape* of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow

### 1. Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet — proves the path works end-to-end.

### 3. Incremental loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist per cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

## Integration with this repo's flow

- `/si` and `/si-quick` defer to this skill for the canonical TDD discipline.
- `developer-agent` enforces vertical slicing during implementation.
- `senior-architecture-reviewer` verifies TDD compliance via git history (test commits precede implementation commits).

## Common Rationalizations

The excuses that quietly turn TDD back into test-after:

| Rationalization | Reality |
|---|---|
| "I'll add tests after the code works" | That's test-after, not TDD. The test no longer drives the design and tends to encode whatever the code happens to do. RED comes before code. |
| "Testing the implementation is fine, it's faster" | Tests bound to internals break on every refactor and stop being a safety net. Test behavior through the public interface. |
| "This slice is small, I'll skip the failing-test step" | If you didn't watch it fail, you don't know the test tests anything. A test that never went RED can pass for the wrong reason. |
| "I'll build the whole layer, then test the stack" | Horizontal slices defer integration risk to the end. Build thin vertical slices that prove the whole path early (see Anti-pattern above). |
| "Tests are green-ish, I'll refactor now" | Never refactor while RED. Get fully GREEN first, then refactor with the net in place. |

## Red Flags

- Code committed before any failing test for it exists.
- A test that has never been observed to fail.
- Tests that assert on private methods or internal state.
- A growing pile of untested code "to be covered later."
- Refactoring while the suite is red.
