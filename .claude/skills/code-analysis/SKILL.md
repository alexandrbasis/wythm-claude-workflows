---
name: code-analysis
description: >-
  Analyze the structure and quality of the current codebase with evidence-backed metrics,
  patterns, and recommendations. Use for an explicit code audit, architecture assessment,
  codebase overview, hotspot/complexity question, module-dependency analysis, or
  pre-implementation exploration. Do not use for pre-merge review (use /sr), runtime
  debugging (use /dbg), or external-technology research (use /deep-research).
argument-hint: "[scope: file, module, or project]"
context: fork
agent: Explore
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(wc *)
  - Bash(find *)
  - Bash(git log *)
  - Bash(git shortlog *)
  - Bash(git rev-list *)
  - Bash(ls *)
---

# Deep Code Analysis

> **Announcement**: Begin with: "I'm using the **code-analysis** skill for deep code analysis."

## Overview

Perform code analysis scoped to the depth tier in Step 1 (Quick / Standard / Deep). Stop as soon as you have enough evidence to fill the output template for that tier — do not expand scope beyond it. Since this runs in a forked context, be decisive: a focused 10-finding report beats a 40-finding report with filler.

For a task-attached analysis, resolve the task and record the report/evidence links using
`../setup/references/task-context.md`. A standalone overview returns its report without
creating a synthetic task.

## Scope Boundaries

This skill READS and REPORTS — it does not suggest code changes or write fixes.

- For pre-merge code review → `/sr`
- For debugging runtime issues → `/dbg`
- For researching external technologies → `/deep-research`

## 1. Determine Analysis Depth

Match the depth to the request — not every question needs a full audit:

| Mode | When | Scope |
|------|------|-------|
| **Quick** | "what's the structure?", "explore this module", overview requests | Steps 2-3 only |
| **Standard** | "analyze", "assess", "audit", "code quality" | Steps 2-5 |
| **Deep** | "full audit", "comprehensive analysis", "deep dive" | Steps 2-6 + dependency analysis |

When the request is ambiguous, pick the mode whose "When" column best matches the user's phrasing. If still unclear, use Standard.

## 2. Scope Discovery

Understand what you're analyzing before diving in. When multiple discovery commands in a step have no dependencies between them, batch them in one turn. Never use placeholders or guess missing parameters.

```bash
# Project structure overview
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" \) \
  ! -path "*/node_modules/*" ! -path "*/dist/*" ! -path "*/coverage/*" \
  | head -60

# Line counts by directory
find . -type f -name "*.ts" ! -path "*/node_modules/*" ! -path "*/dist/*" \
  | xargs wc -l | sort -rn | head -20
```

Read project context dynamically — don't assume the stack or commands:
- Read a root `CLAUDE.md` or `AGENTS.md` only if one exists and applies to the target.
- Inspect manifests that exist (`package.json`, `pyproject.toml`, `go.mod`, and similar)
  before choosing language-specific commands.
- Read project architecture or test guidance only when discovery finds the relevant file.

If any `{{VARIABLE}}` placeholder in this skill or in `references/project-checks.md` is
still literal, resolve it from the repository, CI or project profile (for example,
discover `src/`, `lib/`, or `app/`) before running a command. Do not run a command
containing an unresolved placeholder; if evidence is unavailable, mark that check
skipped with the reason.

The command snippets below use TypeScript/JavaScript as examples. Adapt extensions,
paths, exclusions and commands to detected manifests/CI before running them; do not run
a snippet unchanged when the repository uses another language.

## 3. Architecture Analysis

- Identify layers and seams; read a project-structure document only if discovery finds one.
- Map module dependencies and import relationships
- Find circular dependencies or layer violations
- Check adherence to documented patterns
- Assess module cohesion — does each module own a clear responsibility?

## 4. Code Quality Metrics

- **File size hotspots**: files > 300 lines warrant attention
- **Complexity indicators**: deeply nested logic, long parameter lists, large switch/if chains
- **Code duplication**: repeated patterns across modules
- **Naming consistency**: do conventions hold across the codebase?
- **Test-to-code ratio**: count test files vs source files per module

```bash
# Find large files
find . -name "*.ts" ! -path "*/node_modules/*" ! -path "*/dist/*" \
  -exec wc -l {} + | sort -rn | head -15

# Test file ratio
find . -name "*.ts" ! -name "*.spec.ts" ! -name "*.test.ts" \
  ! -path "*/node_modules/*" ! -path "*/dist/*" | wc -l
find . \( -name "*.spec.ts" -o -name "*.test.ts" \) \
  ! -path "*/node_modules/*" | wc -l
```

## 5. Tech Debt Assessment

- **TODO/FIXME inventory**: search for `TODO`, `FIXME`, `HACK`, `XXX` across source files
- **Deprecated patterns**: old approaches that should be migrated
- **Missing error handling**: bare catches, unhandled promise rejections
- **Incomplete implementations**: stubs, placeholder returns
- **Dependency health**: check `package.json` for outdated or unmaintained packages

## 6. Git History Insights (Deep mode only)

```bash
# Hotspots: most frequently changed files (high churn = risk)
git log --since="6 months ago" --format=format: --name-only \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -20

# Recent contributors
git shortlog -sn --since="3 months ago"

# Commit velocity (activity trend)
git rev-list --count --since="3 months ago" HEAD
git rev-list --count --since="6 months ago" --until="3 months ago" HEAD

# Code ownership concentration (run for top hotspot files)
# git log --format='%aN' -- [file] | sort | uniq -c | sort -rn | head -3
```

## 7. Project-Specific Checks

For Standard and Deep analyses, read `references/project-checks.md` when it exists. Run only
the checks whose paths and stack were established during discovery; skip absent or irrelevant
checks. Quick analyses stop before this section.

Key areas:
- **Architecture layer separation**: verify layer boundaries are respected (e.g., domain must NOT import from infrastructure)
- **Database schema health**: model count, index coverage, and migration count when a
  schema or migrations path was discovered
- **Framework module boundaries**: providers/services stay within their module when the
  detected framework defines that concept
- **Error handling**: consistent use of domain exceptions (not raw `Error` throws)
- **API surface**: endpoint inventory, guard/middleware coverage, DTO/contract definitions

## 8. Output Format

Adapt the report to the analysis depth from step 1. Only include sections relevant to the mode.

### Quick (overview only)

```
# Codebase Overview: [scope]

**Structure**: [high-level description]
**Size**: [file count, LOC]
**Key Modules**: [list with brief descriptions]

**Notable**: [1-2 observations]
```

### Standard

```markdown
# Code Analysis: [scope]

**Date**: [ISO date]

## Summary
[2-3 sentence overview]

## Metrics
| Metric | Value |
|--------|-------|
| Total Files | X |
| Lines of Code | X |
| Test/Code Ratio | X% |
| Tech Debt Items | X |

## Architecture Findings
### Strengths
- [finding]

### Concerns
Include every concern you found, labeled with severity. Do not pre-filter to only CRITICAL/MAJOR — a small number of MINOR items in the report is expected and useful.
- [severity: CRITICAL/MAJOR/MINOR] [confidence: high/med/low] [finding]

## Recommendations
1. [actionable recommendation]
2. [actionable recommendation]
```

### Deep (full report)

All Standard sections plus:

```markdown
## Git History Analysis
[churn hotspots, ownership, velocity trends]

## Dependency Analysis
[outdated deps, security concerns, bundle impact]

## Detailed Findings
[expandable sections for each analysis dimension]
```
