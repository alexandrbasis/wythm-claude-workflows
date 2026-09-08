---
name: product
description: Create a JTBD or PRD that records the user problem, evidence, scope, and measurable outcome through an interactive
  product interview. Use when asked to 'create JTBD', 'write a PRD', 'product requirements', 'jobs to be done', 'product documentation',
  'product spec', or when a feature needs formal product-level documentation before technical planning. Conducts research,
  interviews, and pressure-tests the product thinking before writing. NOT for technical decomposition (use /ct), NOT for feature
  discovery (use /nf).
argument-hint: jtbd [feature] | prd [feature] | quick jtbd [feature] | quick prd [feature]
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Task, Skill
---

<!-- claudops-build: project-config-pointer -->
> If `.claude/skills/product/SKILL.md.disabled` exists, stop before reading a fallback.
> **Project configuration:** If the current project contains `.claude/skills/product/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.
> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, or legacy `.claude/` resource paths. Use repository evidence and optional `CLAUDOPS.md`; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.

# Product Documentation

## Shared task context
For a feature-related request, resolve the repository and any linked task with
[`../setup/references/task-context.md`](../setup/references/task-context.md). Product docs are
long-lived repo-level inputs; link them from the task record rather than copying them into a task.
Create/update a task record only when the product work is part of an active feature objective.

## Objective
Create standalone JTBD or PRD documents through a structured interview, evidence-aware research, and pressure-testing process. The output should be readable without extra verbal context.

## Guidelines
- Use `AskUserQuestion` for clarifications — structured options reduce ambiguity and keep the interview auditable. Skip it only when the user has already unambiguously answered in prior turns.
- Ask non-obvious, thought-provoking questions. If the user's answer sounds confident but vague ("users want it faster"), name the gap ("faster than what, measured how?") rather than accepting it.
- Focus on user progress and context, not features or demographics. A job statement is about the progress a user wants to make, not a feature request.
- Use the templates as output contracts throughout the interview — the interview gathers exactly what the template needs.
- Research is required when a JTBD or PRD makes external, current, competitive, or benchmark claims. Cite every such claim in "Research Findings"; when the document is grounded entirely in supplied product evidence, record why no external lookup was needed instead of researching by default.
- Do not include time estimates in any output.

**Context management.** This workflow runs long (design-exploration + research + interview + grill + write + validators). If compaction happens mid-flow:
- Re-open the template you're writing against.
- Re-open any existing JTBD or previously-written product doc in `product-docs/`.
- Resume from the last unanswered template section; do not restart.
Do not stop early due to token-budget worries — the parent harness handles compaction.

## Workflow

### Argument Validation

**Parse `$ARGUMENTS`:**
- `jtbd [feature]` or `cjtbd [feature]` → full-flow JTBD
- `prd [feature]` or `cprd [feature]` → full-flow PRD
- `quick jtbd [feature]` → quick mode JTBD (skip to Step 5)
- `quick prd [feature]` → quick mode PRD (skip to Step 5)
- `[feature]` only → `AskUserQuestion`: "Which document type?" Options: "JTBD — Jobs-to-be-Done analysis" / "PRD — Product Requirements Document"
- No argument → `AskUserQuestion`: "What feature?" + free-text option, then ask document type

**Quick mode**: When `quick` prefix is detected, skip Steps 1-4 (skip design-exploration, research, interview, and grill). Go directly to Step 5 (document writing): read the template, fill from the user's prompt and any linked context, and mark each unknown inline as `[NEEDS CLARIFICATION: <question>]`. In the template's **Research Findings** section, either cite supplied evidence by its prompt or document source, or record `No external lookup: quick mode is limited to supplied evidence` with the reason and mark external claims as `[NEEDS CLARIFICATION: ...]`. This records the research decision without launching research or asking a new question. Then run Step 6 (Cross-AI Validation) as usual — validation catches gaps that the skipped interview would have caught. Present output with: "Quick mode used — N clarifications remain. For deeper product thinking, run the full `/product` flow."

### Step 0: Load the Output Shape

Before asking questions, read the templates to understand the expected structure:
1. Read the selected `.claude/docs/templates/JTBD-template.md` or `.claude/docs/templates/PRD-template.md`
2. If the selected output is a PRD and a companion JTBD may be created, also read `.claude/docs/templates/JTBD-template.md`

Treat the templates as **output contracts** — the interview gathers exactly the information needed to fill them clearly.

**For PRD**: Check whether an existing JTBD already exists in `product-docs/JTBD/JTBD-*[feature-name]*.md`. If it does, load it as input context — the PRD builds on the JTBD.

**Load shared glossary**: If `product-docs/UBIQUITOUS_LANGUAGE.md` exists, read it and use its terms verbatim during the interview. If a domain term in this conversation conflicts with the glossary, flag the conflict immediately rather than silently drifting. If the glossary is missing or thin and new domain terms come up, propose the terms and update only after explicit authorization.

### Step 1: Context Gathering & Design Exploration

When the product decision changes or extends an existing project, invoke the `design-exploration`
skill to ground product documentation in codebase reality. For a greenfield or product-only
question, keep the context at product level and record that no codebase fit was needed.

When invoking, ask it to return:
- Key codebase findings and current fit for the feature area
- Existing patterns, modules, or flows related to the feature
- Constraints discovered in the existing system
- Risk flags or open decisions

For product documentation, prefer fit, constraints, and risks over implementation decomposition.

Record only material corrections or constraints in the task context; continue without a checkpoint
when the evidence does not change the product direction.

### Step 2: Research

When external evidence affects the job statement, scope, requirements, metrics, or a current
claim, fill the "Research Findings" section with cited sources. The research doesn't have to be
exhaustive — two or three high-quality references per claim is enough. Use quick lookups by
default; only escalate to `comprehensive-researcher` when findings would materially change the
job statement, scope, or requirements. If no external evidence is needed, state that decision
and its basis in the document rather than creating a placeholder research round.

**Quick lookups** (Exa MCP tools directly):
- Competitor approaches to the same job/problem
- Industry best practices for the feature type
- Market signals and opportunity indicators

**In-depth research** (spawn `comprehensive-researcher` agent):
Only when findings materially affect the job statement, scope boundaries, or requirements. When invoking, request a **concise decision memo**:
- Key findings relevant to the product framing
- Implications for job statement or requirements
- Competitive landscape signals
- Risks or caveats

**JTBD research focus**: switching behavior, competitive alternatives being "hired" today, outcome benchmarks, user job patterns
**PRD research focus**: how similar products solve this problem (with specific examples), feature specifications, success metrics benchmarks, UX patterns

If research was run, summarize the decision-changing findings before the interview; ask a follow-up
only when a missing source would change the product decision.

### Step 3: Deep-Dive Interview

Drive the conversation section-by-section toward filling the template. Batch questions per round — typically 2-4, matched to how much the user can reasonably answer at once. One-by-one drags; a ten-question firehose loses signal. When in doubt, 3. After each round, summarize what was gathered and which template section it fills.

---

**JTBD Interview Sections:**

**Job Statement:**
- Walk me through the situation — what moment triggers the need?
- What does the user want to accomplish (their motivation)?
- What does success look like for them (expected outcome)?
- Propose 2-3 candidate job variants — which resonates most?

**Success Criteria:**
- Functional: what are the objective requirements for getting this job done?
- Emotional Personal: how does the user want to feel during/after?
- Emotional Social: how does the user want to be perceived by others?

**Four Forces of Switching:**
- Push: what's broken, slow, or painful about how they do it today?
- Pull: what better future does the new solution promise?
- Anxiety: what could go wrong? What fears exist about switching?
- Habit: what's comfortable about the current way? What switching costs exist?
- What are they "hiring" today for this job? (Include non-consumption)

**User Context:**
- Who is the primary user — defined by circumstances, not demographics?
- What events trigger them to seek a solution?
- What constraints affect their usage?

---

**PRD Interview Sections** (in addition to shared context from JTBD):

**Problem & Evidence:**
- What pain exists and who feels it?
- What evidence proves this is a real problem? (user quotes, data, tickets)
- Why does solving this matter for the business?

**Non-Goals:**
- What are we explicitly NOT building in this version?
- Where could scope accidentally expand?

**Goals & Metrics:**
- What does success look like at launch?
- How will we measure it? (require: number + timeframe + measurement method)
- What metrics must NOT degrade?

**User Stories & Requirements:**
- What are the 3-5 key user stories?
- For each: what proves it's done? (acceptance criteria)
- Priority: what's P0 (must-have) vs P1 (should-have) vs P2 (nice-to-have)?
- Non-functional: performance, security, accessibility targets?

**Solution Shape:**
- What is the core user flow (3-6 steps)?
- What are the key states (loading, empty, error, success)?
- What business rules or constraints apply?

**Modules & Interfaces** (PRD only — fills the `Modules & Interfaces` section of `PRD-template.md`):
- Which deep modules are touched or introduced? Use `.claude/skills/architecture-language/LANGUAGE.md` vocabulary.
- For each module, what does its **interface** guarantee — invariants, ordering, error modes — not just type signatures?
- Where do the seams live, and what sits behind them?
- If a port + adapter pattern is proposed, are there genuinely two adapters (e.g. production + test)? One adapter = hypothetical seam.
- If new domain terms surface, capture them via `/ubiquitous-language` so the PRD, tech-decomposition, and code share a single glossary.

---

Use as few interview rounds as needed to fill material product decisions. When a remaining answer
would change scope or success criteria, ask; otherwise mark the uncertainty and continue to grill.
Use `AskUserQuestion` with multiple-choice options when there are clear alternatives. Challenge
confident but under-specified answers by naming the gap ("You said X — how would that work for case
Y?").

### Step 4: "Grill Me" Challenge Round

**Invoke the `/grill-me` skill** to pressure-test the product documentation shape before writing.

**Before invoking**, summarize the current state:
- Feature name and description
- (JTBD) Primary job statement, success criteria, four forces
- (PRD) Problem + evidence, goals, key requirements
- Areas of uncertainty or risk

**JTBD grill priorities:**
- Is the job statement truly a user job, not a feature request?
- Are the four forces balanced — or is anxiety/habit being ignored?
- Are success criteria measurable or vague?
- Does the competitive analysis reflect genuine switching behavior?

**PRD grill priorities:**
- Are the requirements complete enough for `/ct` to proceed?
- Do user stories have testable acceptance criteria?
- Is the scope boundary clear? Where could scope creep?
- Are there hidden dependencies or assumptions?

**After the grill session completes:**
Incorporate findings. Tighten unclear wording, scope boundaries, hidden assumptions.

**Shared glossary** (before writing the doc): if the grill or interview surfaced new domain terms,
ambiguous synonyms, or a sharpened fuzzy term, load `/ubiquitous-language`; update
`product-docs/UBIQUITOUS_LANGUAGE.md` only when authorized, otherwise record the proposed terms in
the task context. The PRD/JTBD uses canonical terms when available, and downstream `/ct` and `/si`
inherit the linked glossary.

**Checkpoint:** `AskUserQuestion`: "How should we proceed?" Options: "Proceed to document writing" / "Revisit based on grill findings" / "Cut scope based on findings"

### Completion Check

Before writing, confirm a new reader can answer without extra verbal context:

**For JTBD:** What job is being done? By whom and when? What are the success criteria? What forces drive or prevent the switch? What alternatives exist today?

**For PRD:** All of the above, plus: What's the problem and evidence? What are the goals and metrics? What are the key requirements? How does the solution work? What's in/out of scope?

If any remain unclear, continue the interview.

### Step 5: Document Writing

1. **Re-read template** if needed to confirm structure
2. **Create output directory** if it doesn't exist
3. **Write the document(s)**:
   - JTBD output: `product-docs/JTBD/JTBD-[feature-name].md`
   - PRD output: `product-docs/PRD/PRD-[feature-name].md`
4. **For PRD without prior JTBD**: Write a companion `JTBD-[feature-name].md` whenever the interview produced a clear job statement, at least one answer per Four Force (push/pull/anxiety/habit), and a named primary user. If any of those are missing, note it in the PRD's "Related JTBD" section and skip the JTBD write — don't stub a thin JTBD.
5. **If any required section is blank**, continue the interview instead of writing placeholder content; keep explicit `[NEEDS CLARIFICATION: ...]` markers when the user accepted an unresolved question
6. **Present summary** to user for confirmation

### Step 6: Cross-AI Validation

The skill initialization step loads each validator's CLI contract, so invented CLI commands produce unreliable results — run the skill initializer first for each.

Two phases — initialization (sequential), then review (parallel):

Phase 1 — Initialization. Use only the configured validator skills that are available. If a
validator requires initialization, initialize it before its review; otherwise continue with the
available set. A missing optional validator is recorded as skipped.

Phase 2 — Review. Dispatch available independent validator runs in parallel. If none are available,
record `SKIPPED` with the reason; do not block the product document or claim validation passed.

Format output per `.claude/docs/templates/cross-ai-protocol.md` (comparison table, validation, verdict).

**JTBD focus:** Job statement clarity, four-forces coherence, success criteria measurability, absence of solution bias in job framing
**PRD focus:** Requirements completeness for `/ct`, acceptance criteria testability, scope boundaries, metrics measurability, consistency with JTBD reference

**FILE_REFS:** `JTBD-[feature-name].md` and/or `PRD-[feature-name].md` + relevant codebase paths
**OUTPUT:** Append "Cross-AI Validation: PASSED/FAILED" with consolidated verdict

**If validation fails:** `AskUserQuestion`: "Revise document" / "Override and proceed" / "Abandon"

**Skip conditions:** No CLI available, or user explicitly skips.

## Completion

Product documentation is complete when the selected JTBD or PRD exists at its canonical path,
required sections are filled or explicitly marked for clarification, the relevant research
decision and citations are recorded, and cross-AI validation is appended when available and not
skipped. For a PRD, create the companion JTBD only when the stated evidence requirements are
met. An interview summary or validation preview does not replace the document write.

If this product document belongs to an active task, update the resolved task record with the
document link, evidence/validation status, and next action; do not copy the PRD/JTBD contents there.

## Output
- JTBD: `product-docs/JTBD/JTBD-[feature-name].md`
- PRD: `product-docs/PRD/PRD-[feature-name].md`

## Handoff — Next Steps

Product docs are long-lived artifacts that span multiple tasks. The canonical workflow after `/product`:

```
Product documentation complete for [feature-name]:
- Document: product-docs/[PRD|JTBD]/[PRD|JTBD]-[feature-name].md

Next steps:
→ Discover a specific feature from the PRD: /nf [feature-name]
→ Skip to tech planning: /ct [feature-name]
→ Visualize the design: /vp [feature-name]
→ Consistency check: /analyze [feature-name]
```
