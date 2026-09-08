---
name: tdd
description: Test-driven development with red-green-refactor loop using vertical slices. Use when building features or fixing
  bugs with TDD, when /si or /si-quick needs canonical TDD discipline, when user mentions "red-green-refactor", "tracer bullets",
  "test-first", or asks for integration-style tests. Forbids horizontal slicing (all tests then all implementation). Use as
  a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients
  may not enforce this host-level restriction.
metadata:
  claude_disable_model_invocation: 'true'
  invocation_guard: explicit-only; portable clients may not enforce Claude Code host-level invocation restrictions
compatibility: Portable clients may not enforce Claude Code invocation guards or project setup behavior.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/tdd/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/tdd/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.
> **Invocation guard:** use this as a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients may not enforce Claude Code host-level invocation restrictions.

# Test-Driven Development

> **Upstream**: Adapted from [mattpocock/skills/tdd](https://github.com/mattpocock/skills/tree/main/tdd). Vocabulary aligned with this repo's `architecture-language/LANGUAGE.md`. Used as the canonical TDD reference by `/si` and `/quick`.

When invoked for task work, resolve the task with `../setup/references/task-context.md`. Use its
approved requirements and decisions as the authority, and record only the resulting test evidence
and next action there; this reference does not create a second planning or test ledger.

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

- [ ] Use the approved task/decomposition and the current authorized request as the authority for
      interface changes and test priorities when this skill is invoked from `/si` or `/quick`;
      ask only about missing or materially changed decisions, and do not repeat approval already
      granted for the same scope
- [ ] Confirm missing interface or behavior priorities only when neither the resolved task/plan
      nor the current authorized request settles them
- [ ] Identify opportunities for [deep modules](deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List the behaviors to test (not implementation steps)

Ask: "What should the public interface look like? Which behaviors are most important to test?"
Use that question only when the invoking workflow has not already answered it.

**You can't test everything.** When the resolved task/plan or current authorized request sets
priorities, use them. Otherwise confirm which behaviors matter most before coding. Focus
testing effort on critical paths and complex logic, not every possible edge case.

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

- `/si` and `/quick` defer to this skill for the canonical TDD discipline.
- `developer-agent` enforces vertical slicing during implementation.
- Reviewers may use git history as supporting evidence when available, but commit chronology alone
  cannot prove that RED was observed. Report chronology as unverifiable when history is absent or
  when tests and implementation were intentionally coupled under repository policy; the behavioral
  RED-before-GREEN invariant still applies.

## Red Flags

- Code committed before any failing test for it exists.
- A test that has never been observed to fail.
- Tests that assert on private methods or internal state.
- A growing pile of untested code "to be covered later."
- Refactoring while the suite is red.
