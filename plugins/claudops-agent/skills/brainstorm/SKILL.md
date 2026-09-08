---
name: brainstorm
description: Compare options and clarify a decision through a collaborative brainstorming session. Use when asked to 'brainstorm',
  'let's brainstorm', 'explore ideas', 'think through', 'brainstorm about [topic]', 'what are our options for', 'let's think
  about', 'pros and cons of', 'help me decide', or 'weigh the options'. NOT for feature discovery (use /nf), NOT for PRD/JTBD
  docs (use /product), NOT for deep research (use /deep-research), NOT for pre-implementation design (auto-triggered by design-exploration
  skill).
allowed-tools: Read Write Edit Grep Glob AskUserQuestion Agent Skill
metadata:
  claude_argument_hint: '["topic"]'
compatibility: Portable clients may not enforce Claude Code invocation guards or project setup behavior.
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/brainstorm/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/brainstorm/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Brainstorming Session

## Shared task context
For a project-related topic, resolve the repository and any linked task with
[`../setup/references/task-context.md`](../setup/references/task-context.md) before collecting
context. General topics need no artificial task. Reuse existing brainstorm notes and record a
feature-related result in the resolved task's artifact links and next action.

## Objective
Conduct a collaborative brainstorming session through natural dialogue, exploration of options, and structured capture of insights. Brainstorms can be project-related or general — the skill adapts its depth and tooling accordingly.

## Guidelines
- Use `AskUserQuestion` for clarifications — it renders as interactive options the user can pick from, which is friendlier than free-text for most choices.
- Ask **non-obvious and thought-provoking** questions that challenge assumptions
- Present multiple perspectives and approaches
- Capture key insights and decisions in the brainstorm notes

## Argument Validation

**If no `[topic]` argument is provided:**
1. Use `AskUserQuestion`: "What would you like to brainstorm about?"
   - Use the repository's configured brainstorming and task roots for context
   - Include a free-text option
2. Derive the topic slug from the user's response

## Resume Check

Before starting a new session, use the shared task resolver and inspect only the linked candidate
entrypoint. For a standalone general topic, search the repository's configured brainstorming
convention for `brainstorm-*-[topic-slug].md`.
1. If a matching draft exists:
   - Read the existing document
   - `AskUserQuestion`: "Found an existing brainstorm on this topic."
     Options: "Continue from where we left off" / "Start fresh" / "Review and build on it"
   - **Continue**: identify which sections are complete, pick up from the first incomplete area
   - **Start fresh**: proceed with full workflow
   - **Review**: present existing document for feedback, then expand

## Workflow

### Step 1: Calibrate Depth

Brainstorms vary widely in scope. Quickly assess what kind of session this is — the answer shapes everything else (how many questions to ask, whether to research, how formal the capture should be).

`AskUserQuestion` with options:
- **Quick decision** — "I need to pick between a few options" (5-10 min, 2-3 questions, lightweight capture)
- **Exploration** — "I want to think through something" (15-30 min, structured exploration, standard capture)
- **Deep dive** — "This is a big topic, let's go deep" (30+ min, full exploration with research, detailed capture)

### Step 2: Context Gathering (Adaptive)

Context gathering is not a blocking gate. For a project-related topic, inspect `CLAUDE.md`
and only the files needed for the named area before proposing options; if the topic does not
identify a code area, ask for that context or keep the discussion at product level. Pull in
more context as a specific branch requires it. For general topics, skip this step entirely.

**For project-related topics:**
- If the topic clearly touches existing code and codebase evidence affects the choice, invoke the `design-exploration` skill to scan the relevant area
- If the scope is unclear, start with the brainstorm conversation and invoke design-exploration later when specific areas of the codebase become relevant

**For general topics:**
- Skip codebase context entirely
- Jump straight to exploration

### Step 3: Exploration

The core of the brainstorm. Adapt the depth to the calibration from Step 1.

**Understanding the Topic:**
- Ask clarifying questions (batch related questions via `AskUserQuestion`)
- Focus on: goals, constraints, success criteria, concerns

**Exploring Approaches:**
- Propose 2-3 different perspectives or options
- Present trade-offs clearly using a consistent format:
  - Option name, brief description, pros, cons
- Lead with your recommendation and reasoning

**Deep Exploration** (for Exploration/Deep Dive depth):

| Category | Questions to Consider |
|---|---|
| **Practical** | What could go wrong? Edge cases? Resources needed? How does this scale? |
| **Assumptions** | What are we assuming? Who else is affected? What's the opposite approach? |
| **Impact** | How do we measure success? What's the MVP? What if we don't do this? |
| **Trade-offs** | Speed vs quality? Short-term vs long-term? Complexity vs simplicity? |

Present ideas in tight, self-contained sections sized to the calibration from Step 1 — shorter for Quick Decision, longer for Deep Dive. Pause to validate understanding between sections. Be ready to pivot if direction changes.

**Completion signals** — the brainstorm is "done" when:
- For Quick Decision: a recommendation, alternatives, and trade-offs are stated and the user has enough information to choose or defer
- For Exploration: the major decision angles are covered, conclusions and unresolved questions are captured, and the user confirms
- For Deep Dive: each selected question category is covered, remaining uncertainty is explicit, and the user has no more material "what about..." questions

### Step 4: Research (When Needed)

Research is a branch, not the trunk. Most brainstorms need none — the model's own knowledge plus user input is usually enough, especially for Quick Decision depth. Run research only when the answer genuinely depends on information you don't have.

**Quick lookups:**
- `get_code_context_exa` — for code-related context, APIs, libraries
- `web_search_exa` — for trends, market data, best practices

**In-depth research:**
- Spawn `comprehensive-researcher` agents when the decision hinges on external evidence the user will ask about.
- When fanning out across independent sub-topics, spawn all subagents **in the same assistant turn** — do not default to sequential. Inform the user what's being researched.

**Code context (project-related):**
- Use Explore agents (Sonnet) to scan relevant modules, patterns, and prior art

**Trigger research only when** the brainstorm cannot move forward without it — e.g., the user explicitly asks for market data, a claim requires external verification to be actionable, or an unfamiliar technology is central to the decision. Do not research to pad Deep Dive depth.

### Step 5: Capture

After exploration is complete, create the brainstorm artifact. The format adapts to the session depth.

**For Quick Decision depth:**
- `AskUserQuestion`: "Want me to save these notes, or was the conversation enough?"
  - If no: skip capture entirely — the conversation itself is the artifact
  - If yes: write a brief summary (skip the full template)

**For Exploration / Deep Dive depth:**
1. For a feature-related topic, create or update `brainstorm-[topic-slug].md` in the resolved task
   convention. For a general topic, use the repository's configured `docs/brainstorming/`
   convention. Link the artifact from `TASK.md` when a task exists.
2. Use template: `.claude/docs/templates/brainstorm-template.md`
3. Include:
   - Topic overview and type (project/general)
   - Key questions explored
   - Options discussed with pros/cons
   - Conclusions and insights
   - Research findings (if any)
   - Action items (if any)
4. Present summary to user for confirmation

### Step 6: Next Steps

After capture, offer a natural handoff to the next skill based on what emerged from the brainstorm.

`AskUserQuestion`: "What would you like to do next?"
- **"Create a feature spec"** — invoke `/nf` with the topic context
- **"Create a task"** — invoke `/ct` with conclusions as input
- **"Write a PRD"** — invoke `/product` with brainstorm insights
- **"Nothing, we're done"** — wrap up

Skip this step for general (non-project) brainstorms unless the user explicitly wants to act on the results.

## Scope Boundaries
- Feature discovery interviews: use `/nf`
- PRD/JTBD documentation: use `/product`
- Deep technical research: use `/deep-research`
- Pre-implementation design: auto-triggered by `design-exploration` skill (not this one)
- Task creation: use `/ct`

## Output
`docs/brainstorming/brainstorm-YYYY-MM-DD-[topic-slug].md` (optional for Quick Decision depth)
