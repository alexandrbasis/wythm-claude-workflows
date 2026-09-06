# Claudops skills

The 40 maintained skills below are also packaged for Claude Code and Agent Plugins. In Claude plugin mode, prefix commands with `/claudops:`; for example `/claudops:quick`. Source folder aliases are preserved by the build.

## Setup and shared conventions

| Command | Purpose | Invocation |
|---|---|---|
| [/setup](./setup/SKILL.md) | Configure claudops for a specific repository after copying the workflow or installing the plugin | Task-selected |
| [/update-setup](./update-setup/SKILL.md) | Inspect or apply upstream claudops changes to a project's copied .claude/ workflow | Task-selected |
| [/coding-conventions](./coding-conventions/SKILL.md) | Internal reference skill — coding standards and patterns for developer agents | Task-selected |
| [/review-conventions](./review-conventions/SKILL.md) | Internal reference skill — shared conventions for all code review agents | Task-selected |
| [/architecture-language](./architecture-language/SKILL.md) | Canonical architectural vocabulary — module, interface, seam, adapter, depth, leverage, locality | Explicit only |

## Delivery

| Command | Purpose | Invocation |
|---|---|---|
| [/ct](./ct/SKILL.md) | Use when a feature/scoped task is clear enough for technical planning — produces an implementation-ready technical decomposition before coding | Task-selected |
| [/si](./si/SKILL.md) | Implements a feature from a technical decomposition using TDD, keeping the task document updated and handing off cleanly to review | Task-selected |
| [/quick](./si-quick/SKILL.md) | Use when handling a small, untracked change with clear scope or a bugfix with a known root cause, and there is no tech-decomposition or task directory to follow | Task-selected |
| [/sr](./sr/SKILL.md) | Use when asked to review code before merge or review a PR, branch, commit range, task path, or current working tree | Task-selected |
| [/prc](./prc/SKILL.md) | Review and address code review comments on PR | Task-selected |
| [/finisher](./finisher/SKILL.md) | Ship an existing implementation by committing local changes, pushing an open PR, waiting for green CI, and merging it | Task-selected |
| [/ph](./ph/SKILL.md) | Prepare session handoff for continuation in a new conversation | Task-selected |
| [/udoc](./update-docs/SKILL.md) | Update documentation and generate changelog after task implementation | Task-selected |

## Discovery and planning

| Command | Purpose | Invocation |
|---|---|---|
| [/nf](./nf/SKILL.md) | Runs an in-depth feature-discovery interview that explores, challenges, and documents a new feature before planning | Task-selected |
| [/product](./product/SKILL.md) | Create a JTBD or PRD that records the user problem, evidence, scope, and measurable outcome through an interactive product interview | Task-selected |
| [/vp](./vp/SKILL.md) | Create interactive visual prototype playground for user approval before technical decomposition | Task-selected |
| [/blueprint](./blueprint/SKILL.md) | Turn a one-line objective into a bounded multi-session implementation plan with cold-start briefs | Task-selected |
| [/analyze](./analyze/SKILL.md) | Compare a task's discovery or product requirements with its tech decomposition and report traceability gaps | Task-selected |
| [/rip](./rip/SKILL.md) | Review a technical implementation plan for business-value alignment and scope fit | Task-selected |
| [/grill-me](./grill-me/SKILL.md) | Use when a plan, design, or discovery document needs stress-testing for hidden assumptions, scope gaps, unresolved branches, or ambiguous wording; also when the user explicitly says "grill me". | Task-selected |

## Exploration and architecture

| Command | Purpose | Invocation |
|---|---|---|
| [/brainstorm](./brainstorm/SKILL.md) | Compare options and clarify a decision through a collaborative brainstorming session | Task-selected |
| [/design-exploration](./design-exploration/SKILL.md) | Explore codebase and design approaches before implementation | Task-selected |
| [/code-analysis](./code-analysis/SKILL.md) | Analyze the structure and quality of the current codebase with evidence-backed metrics, patterns, and recommendations | Task-selected |
| [/improve-codebase-architecture](./improve-codebase-architecture/SKILL.md) | Explore a codebase for architectural deepening opportunities: refactors that turn shallow modules into deeper ones with better testability and locality | Task-selected |
| [/zoom-out](./zoom-out/SKILL.md) | Step up one layer of abstraction and produce a map of the relevant modules and their callers — used when you (or the agent) are stuck in one file and losing the bigger picture | Explicit only |
| [/ubiquitous-language](./ubiquitous-language/SKILL.md) | Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms | Task-selected |

## Quality and debugging

| Command | Purpose | Invocation |
|---|---|---|
| [/dev-server](./dev-server/SKILL.md) | Start any project's dev server and monitor it for errors in real-time | Task-selected |
| [/dbg](./dbg/SKILL.md) | Debug mode with runtime evidence and instrumentation | Task-selected |
| [/fci](./fci/SKILL.md) | Fix CI pipeline failures blocking PR merge | Explicit only |
| [/git-guardrails](./git-guardrails/SKILL.md) | Inspect, install, customize, or troubleshoot the harness-level git safety hook that blocks dangerous git operations (push, branch -D, checkout .) before they execute | Explicit only |
| [/tdd](./tdd/SKILL.md) | Test-driven development with red-green-refactor loop using vertical slices | Explicit only |
| [/qa](./qa/SKILL.md) | Interactive QA session where the user reports bugs conversationally and the agent files them as tracker issues (GitHub or Linear) one by one or as a dependency-linked breakdown | Task-selected |
| [/triage-issue](./triage-issue/SKILL.md) | Investigate a reported bug, find its root cause, and file a tracker issue (GitHub or Linear) with a TDD-based fix plan | Task-selected |

## Research and tools

| Command | Purpose | Invocation |
|---|---|---|
| [/cc-linear](./cc-linear/SKILL.md) | Execute Linear operations via direct GraphQL API — create issues, update status/priority/title, add comments, search tasks, manage labels, assign work, and link PRs | Task-selected |
| [/antigravity-cli](./antigravity-cli/SKILL.md) | Run Google Antigravity CLI (agy) for web-grounded research, cross-AI review, or validation | Task-selected |
| [/codex-cli](./codex-cli/SKILL.md) | Run OpenAI Codex CLI for one-shot cross-AI code review or approach validation | Task-selected |
| [/cursor-cli](./cursor-cli/SKILL.md) | Run Cursor CLI (Composer 2, a Kimi-K2.5 lineage) for one-shot cross-AI code review when a non-OpenAI/non-Anthropic perspective is specifically wanted | Task-selected |
| [/parallelization](./parallelization/SKILL.md) | Parallelize implementation across isolated git worktrees | Task-selected |
| [/deep-research](./deep-research/SKILL.md) | Research an external, current, niche, or unfamiliar technical topic with cited evidence | Task-selected |
| [/sbs](./sbs/SKILL.md) | Interactive teaching guide for learning while working | Task-selected |

The invocation column records Claude frontmatter. Portable clients need equivalent policy enforcement; the generated package README describes those limits.

Cross-AI protocol: [cross-ai-protocol.md](../docs/templates/cross-ai-protocol.md).
