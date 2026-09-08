# Task Splitting Decision

**Date**: YYYY-MM-DD
**Decision**: SPLIT RECOMMENDED
**Task Context**: [resolved task directory and `TASK.md` or existing entrypoint]
**Parent Active Plan**: [path to the active plan or the relevant `TASK.md` section]

## Summary

[2-3 sentences explaining why the task should be split and what logical sequence is recommended.]

## Why Split

| Signal | Evidence From Parent Doc | Impact |
|--------|---------------------------|--------|
| Functional breadth | [Existing requirement IDs, plain acceptance or use-case clusters] | [Why one PR is too broad] |
| Verification breadth | [Test suites / cases] | [Why testing becomes hard to review] |
| Module or domain spread | [Paths / bounded contexts] | [Why reviewer load is too high] |
| Contract or prerequisite sequencing | [What must exist before what] | [Why ordering matters] |

**Approach**: [Vertical functional slices / Prerequisite-then-consumer slices]
**Decision Level**: [MUST SPLIT / SHOULD SPLIT]
**Guardrail**: No phase may depend on a contract, interface, DTO, endpoint shape, schema, or module boundary first defined in a later phase. Each phase must retain its assigned functional acceptance and verification, with a real consumer for any prerequisite contract.

## Phase Plan

### Phase N: [Descriptive Name]

**Goal**: [Functional outcome or concrete prerequisite outcome]
**Delivers**: [What becomes possible or testable after this phase]
**Includes Requirements**: [Existing source IDs or plain-language acceptance items]
**Includes Tests**: [Test suite names, existing test IDs, behavior checks, or both]
**Includes Implementation Steps**: [Relevant parent step numbers / sub-steps]
**Files / Modules**: `path/to/module`, `path/to/other-module`
**Depends On**: [None / Phase N-1]
**Introduces For Later Phases**: [Contracts, modules, endpoints, or data shapes introduced here, or `None`]
**Must Not Assume**: [Future contract/API/schema details this phase does not know yet, or `None`]
**Out Of Scope**: [What intentionally stays for later phases]
**Behavioral Verification**: [How this phase can be tested without relying on later phases]

[Repeat for each phase. Choose the smallest number that preserves safe, behaviorally testable
sequencing; do not split to satisfy a numeric target.]

## Sequencing Validation

1. **First**: [Phase Name] — [Why this phase must happen first]
2. **Next**: [Phase Name] — [Why it safely builds on the earlier phase]
3. **Contract Direction Check**: [Explain why no earlier phase depends on contracts introduced later]
4. **If Applicable**: [Explain where shared contracts/data models are introduced and why that order is safe]

## Risks If Not Split

- [Risk 1]
- [Risk 2]

## Recommendation

✅ **Split this task into [N] phases in the sequence above.**

[Additional context for the human decision-maker]
