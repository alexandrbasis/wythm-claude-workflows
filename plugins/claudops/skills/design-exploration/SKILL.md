---
name: design-exploration
description: Explore codebase and design approaches before implementation. Use when asked 'explore the design', 'how would
  this fit', 'design exploration', 'what patterns exist for', 'how is X implemented', or when another skill (brainstorm, nf)
  needs codebase context to ground a design proposal. NOT for code review (use /sr), NOT for static analysis (use /code-analysis).
allowed-tools:
- Read
- Glob
- Grep
- Agent
- AskUserQuestion
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/design-exploration/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/design-exploration/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Design Exploration

Gather codebase context and explore design approaches before implementation. This skill bridges the gap between "we have an idea" and "we have a concrete direction" by grounding proposals in what actually exists in the codebase.

When this supports a task, use [`../setup/references/task-context.md`](../setup/references/task-context.md)
to resolve the repository, linked task and applicable local instructions. Return findings to the
caller; the caller records them once in the task context instead of creating a parallel artifact.

## When This Skill Runs

Typically invoked by `/brainstorm` or `/nf`, but can also run standalone when someone needs to understand how a feature fits into the existing architecture. The caller provides:
- Feature name and initial description
- Known constraints or requirements
- Specific areas to focus on (if known)
- The current goal: feature framing, design choice, or pre-implementation fit check

## Process

### Step 1: Parallel Context Gathering

Use `references/exploration-checklist.md` as a menu, selecting only the feature-type checklist
items that affect the caller's decision. Use one focused scan by default; fan out independent
angles only when broad coverage materially changes the decision and the host provides the worker.
Do not fan out to satisfy a fixed count. Use a faster model unless the task clearly needs deeper
reasoning.

Common scan angles:
1. **Closest prior art**: similar features, modules, screens, services, or flows
2. **Core data or state model**: entities, schemas, stores, contracts, or domain concepts
3. **Integration boundaries**: APIs, shared utilities, routing, permissions, jobs, or external dependencies
4. **User-facing surface**: routes, screens, components, or interactions, if the feature has UX implications
5. **Constraints and conventions**: architecture rules, test patterns, shared abstractions, docs, and known limitations

Only go as deep as needed for the caller's goal. When invoked from `/nf`, prefer fit, viable options, constraints, and risks over implementation decomposition.

### Step 2: Synthesize Findings

After agents return, compile a structured findings report:

```
## Codebase Findings

### Existing Patterns
- [Pattern name]: [Where it's used, how it works]

### Current Fit
- [Where this feature would likely belong or extend]

### Integration Points
- [Where new code connects to existing code]

### Constraints Discovered
- [Things the codebase enforces that the design must respect]

### Relevant Prior Art
- [Existing flow, screen, module, or service worth reusing or extending]
```

### Step 3: Propose Approaches

Present **2-3 design approaches** with trade-offs. Lead with your recommendation and explain why.

For each approach:
- **What**: Brief description (2-3 sentences)
- **How it fits**: Which existing patterns it follows
- **Trade-offs**: Pros and cons grounded in codebase evidence
- **Effort signal**: Relative complexity (low / medium / high)
- **Risk signal**: Key uncertainty, dependency, or downside to watch

### Step 4: Incremental Design Summary

Once the user picks an approach (or you have a clear winner):

Present one compact, clearly labeled summary covering only the areas that materially affect the
caller's decision:
   - Where the feature fits in the current product or architecture
   - How the user flow or system flow would likely work
   - Which data, state, or contracts are affected
   - What constraints or dependencies shape the design
   - What risks, open questions, or irreversible choices remain
   - Implementation-heavy details only if they materially affect discovery or planning

Ask for revision only when a specific unresolved choice blocks the caller; otherwise return the
summary without an artificial continue loop.

When invoked from `/nf`, stop short of full tech decomposition. The goal is to clarify direction, not to write the implementation plan.

## Output Contract

When this skill completes, it returns to the caller:

1. **Key codebase findings** — existing patterns, current fit, integration points, and constraints discovered
2. **Design approaches** — viable options, with a recommendation if one stands out
3. **Open questions** — anything that still needs user judgment or further exploration
4. **Risk flags** — issues, dependencies, or scope cautions that could affect direction

## Key Principles

- **Evidence-based**: Every design recommendation references actual codebase patterns
- **YAGNI**: Each proposed approach should cover only what the caller's goal requires. If an approach adds abstraction beyond the stated goal, either drop it or label the extra clearly as "optional — not required by the brief."
- **Follow existing conventions**: New code should look like it belongs in the codebase
- **Caller-sensitive depth**: Tune depth to the caller's goal instead of always pushing into implementation detail
- **Multiple choice preferred**: Use `AskUserQuestion` with options when clarifying
- **Parallel exploration**: Launch independent Explore scans simultaneously when fan-out is justified; keep narrow questions focused
