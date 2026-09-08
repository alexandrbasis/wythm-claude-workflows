---
name: blueprint
description: Turn a one-line objective into a bounded staged implementation plan with cold-start briefs. Use when asked to
  'blueprint', 'multi-session plan', 'long-term plan', 'construction plan', 'break into sessions', 'plan across sessions',
  'multi-step project plan', 'session plan', or when work needs staged handoffs. Produces a plan where each step can be resumed
  independently by a fresh agent with no prior context.
argument-hint: <objective>
allowed-tools:
- Read
- Glob
- Grep
- Bash
- Agent
- AskUserQuestion
- WebSearch
- WebFetch
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/blueprint/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/blueprint/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# /blueprint — Multi-Session Construction Plan

## Shared task context
Resolve the repository and task with
[`../setup/references/task-context.md`](../setup/references/task-context.md) before drafting.
Reuse a linked task and its existing plan entrypoint. This skill is an optional multi-session mode
of the planning stage; it must not create a parallel task root when `/ct` already owns the plan.

## Purpose

Use this skill when an objective spans domains, handoffs, or dependencies that benefit from a
sequenced plan. Decompose the objective so each step:
1. Has a **cold-start context brief** — everything a fresh agent needs to execute without reading prior session history
2. Has **explicit dependencies** — which steps must complete first
3. Has **verification criteria** — how to confirm the step is done

### Context discipline while drafting

Context may be compacted mid-plan. If you sense the window tightening, write the plan to disk incrementally (one step at a time) rather than building the whole blueprint in memory. Produce every step through to the end — do not stop early because of token concerns. If compaction fires mid-draft, resume from the last written step.

## When to Use

- Feature spans multiple domains (backend + mobile + infra)
- Work needs staged execution, handoffs, or independently verifiable milestones
- Multiple developers/agents need to coordinate
- User says "this is a big one" or "break this down for me"

## Pipeline

### Phase 1: Research (understand the landscape)
1. Read relevant PRDs, JTBDs, and existing task docs
2. Explore the codebase areas that will be touched
3. Identify existing patterns to follow
4. List unknowns and risks

When the objective spans independent codebase areas (e.g., backend + mobile + infra), you may
spawn one Agent subagent per area in the same turn and synthesize the findings. Use this fan-out
only when the areas can be explored independently and the caller has the required agent access;
otherwise inspect the smallest relevant set in one pass.

### Phase 2: Design (create the dependency DAG)
1. Break the objective into behaviorally meaningful implementation steps
2. Map dependencies between steps (which must come first?)
3. Identify parallelizable steps (can run simultaneously)
4. Record relative complexity only when it changes sequencing, ownership, or review depth

### Phase 3: Draft (write step documents)
For each step, produce:

```markdown
## Step [N]: [Title]

### Cold-Start Brief
> A fresh Claude session should read ONLY this section to begin work.

**Objective**: [What this step accomplishes]
**Codebase entry points**: [Specific files/directories to read first]
**Patterns to follow**: [Existing code patterns this step should mirror]
**Key decisions already made**: [Design choices from Phase 2 that constrain this step]
**What exists before this step**: [State of the codebase when this step starts]

### Dependencies
- Blocked by: [Step X, Step Y] or "None — can start immediately"
- Blocks: [Step Z]

### Scope
- **In scope**: [Specific deliverables]
- **Out of scope**: [What NOT to do in this step]

### Acceptance Criteria
- [ ] [Criterion 1 — testable/verifiable]
- [ ] [Criterion 2]
- [ ] Relevant tests pass: `[specific test command]` or `Not applicable — plan artifact`
- [ ] Type check passes: `[specific command]` or `Not applicable — plan artifact`

### Estimated Complexity
[S / M / L] — [Brief justification]

### Suggested Task Command
`/ct [resolved task path]` to refine this step in the active plan. Use the detailed planning
guide only when this step has material migration, permission, integration, coverage or coordination
risk and the compact plan cannot carry the needed detail.
```

### Phase 4: Review (adversarial check)

First, list every concern you noticed while drafting — missing migrations, implicit env setup, unclear step boundaries, weak acceptance criteria — including low-confidence ones. Then classify each into: Completeness / Independence / Ordering / Gaps / Rollback. Carry the low-confidence items into the Risks table below with explicit "(low confidence)" tags rather than dropping them silently.

After listing, verify against the checklist:
1. **Completeness**: Does executing all steps achieve the original objective?
2. **Independence**: Can each step truly be executed by a fresh agent with only its cold-start brief?
3. **Ordering**: Are dependencies correctly captured? No circular dependencies?
4. **Gaps**: Are there implicit steps (migrations, config changes, env setup) that should be explicit?
5. **Rollback**: If step N fails, does it break steps 1..N-1?

Finish the review before writing the final plan. A plan is complete when each step has detail
appropriate to its horizon: steps executable next have self-contained cold-start briefs; later
steps have a bounded objective, dependencies, scope, and acceptance/verification criteria that
are sufficient for later refinement; and the review's risks, open questions, and rollback
implications are recorded.

## Output

Save the blueprint in the resolved task's existing plan convention. If no plan entrypoint exists,
use `blueprint.md` beside `TASK.md` in the minimum task record. Preserve an existing
`docs/superpowers/plans/` document when it is the linked task artifact.

```markdown
# Blueprint: [Feature Name]

**Objective**: [The original one-line objective]
**Created**: [Date]
**Steps**: [N]
**Execution horizon (optional)**: [Describe only when useful for coordination]
**Parallelizable steps**: [List]

## Dependency Graph
```
Step 1 ─── Step 2 ─── Step 4
              │
              └── Step 3 ─── Step 5
```

## Steps

[Step documents from Phase 3]

---

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | [H/M/L] | [Strategy] |

## Open Questions
- [Question that needs user input before execution]
```

## Integration

- Each step can be refined with `/ct [resolved task path]` in the existing task plan; a phase or
  separate detailed plan is warranted only when the step's risk or handoff needs it.
- Steps can reference existing task docs in `tasks/` if they already exist.
- When detailed planning is warranted, point the `/ct` consumer to
  `.claude/skills/ct/references/decomposition-guide.md` and preserve the active plan link.
- After writing, update the resolved task record with the blueprint link, current stage and next
  action. Keep the blueprint as the source for its multi-session steps.

## Constraints

- **Cold-start briefs are self-contained** — a fresh agent reads only its step's brief and can begin work. If you find yourself about to reference "see Step 2", inline the information instead.
- **Keep steps behaviorally bounded and resumable** — split when a step would be unsafe, vague, or impossible to verify as a unit; do not impose an elapsed-time target.
- **Plan to the level each step needs right now** — the next executable step gets a full cold-start brief; later steps get enough objective, dependencies, scope, and verification to refine safely. Stop adding detail once the next executor has enough to start.
- **Output is a plan document, not code edits.** The deliverable is the blueprint file; `/si` executes each step in a later session. If the user explicitly authorized implementation in the same request, continue to the authorized `/si` handoff after saving the plan; otherwise stop at the saved plan and state the separate handoff.
