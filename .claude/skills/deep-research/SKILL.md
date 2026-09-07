---
name: deep-research
description: >-
  Research an external, current, niche, or unfamiliar technical topic with cited evidence.
  Use for explicit research, comparisons, technology evaluation, migration/dependency
  decisions, or questions whose answer depends on sources outside the local codebase. Do
  not use for quick brainstorming (use /brainstorm), feature discovery (use /nf), or
  static local code analysis (use /code-analysis).
argument-hint: "[topic or question]"
context: fork
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Grep
  - Glob
  - Task
  - mcp__exa__web_search_exa
  - mcp__exa__get_code_context_exa
  - mcp__ref__ref_search_documentation
  - mcp__ref__ref_read_url
---

# Deep Research

For task-linked research, resolve the repository and task with
[`../setup/references/task-context.md`](../setup/references/task-context.md). Research is an
optional evidence branch: persist a compact `research.md` in the resolved task only when findings
change scope, requirements or a technical decision; otherwise return the answer inline and record
the decision if the caller needs it.

## Overview

Conduct comprehensive research on technical topics, synthesizing information from multiple sources. Since this runs in a forked context, explore extensively — only the final findings return to the main conversation.

## 1. Determine Research Depth

Not every request needs a 10-source report. Match the depth to the question:

| Depth | When | Output |
|-------|------|--------|
| **Quick** | Simple factual question, "how do I X", single-topic lookup | Direct answer with 1-2 sources |
| **Comparison** | "X vs Y", "which library for", "should we use" | Comparison table + recommendation |
| **Deep** | Technology evaluation, migration analysis, architectural decision | Full structured report |

If the user's intent is ambiguous, default to **Comparison** — it's the most common need.

## 2. Source Strategy

### Tool Priority (Exa-first)

Pick the smallest set of tools that answers the question. Many Quick-depth queries need zero tool calls. When you do search, choose by fit:

- **`get_code_context_exa`** when you need API/library code examples or usage patterns.
- **`web_search_exa`** when the question is conceptual, comparative, or ecosystem-wide.
- **`ref_search_documentation` / `ref_read_url`** when you need authoritative confirmation and Exa's summary is insufficient.
- **`WebSearch` / `WebFetch`** only as a fallback when the above can't reach the source.

Do not run a tool to confirm something you already know confidently from the docs or the codebase — cite the source instead.

### Parallel Search

Since this runs in a fork, optimize for speed by launching parallel queries:
- When queries have no dependencies, emit all of them in the **same assistant turn** (one tool-use block per query). Do not wait for the first to return before issuing the next.
- Combine web searches with a local `Grep`/`Glob` pass in the same turn when codebase context is relevant.
- Use multiple small, focused queries rather than one broad query

### Source Types

| Source | Best For |
|--------|----------|
| Official docs | Authoritative API/config info |
| GitHub repos | Real implementations, issue discussions, activity signals |
| Technical blogs | Best practices, gotchas, real-world experience |
| Stack Overflow | Common problems, community-vetted solutions |
| Local codebase | Integration points, existing patterns, constraints |

## 3. Research Strategies

Choose the smallest strategy that answers the question:

- **Technology evaluation:** official documentation first, then repository activity or
  adoption evidence only when it affects the decision, then local integration constraints.
- **Problem solving:** search the exact symptom, confirm with official troubleshooting
  guidance, and inspect local code only when the fix depends on it.
- **Best practices:** use official guidance and local conventions; add community sources
  only when they resolve an open trade-off.

## 4. Cross-Verification

- Match source count to depth: Quick = 1–2 sources (skip Cross-Verification entirely); Comparison = 2–3; Deep = 3–5.
- Stop gathering once the answer is stable across sources — additional confirmatory sources add little value. If the first 2 sources agree and are authoritative (official docs, primary repos), that's enough.
- Verify claims against official docs only when the claim is load-bearing for a recommendation.
- Check publication dates — prefer content from the last 12 months
- Look for consensus; flag disagreements explicitly
- Be skeptical of AI-generated content in search results

## 5. Output Format

Adapt output to the research depth determined in step 1.

### Quick Answer
```
**Answer**: [concise answer]

**Source**: [url] — [what it confirmed]

**Caveat**: [any important limitations or conditions]
```

### Comparison
```
## [X] vs [Y] for [use case]

| Criteria | X | Y |
|----------|---|---|
| [criterion] | [assessment] | [assessment] |

**Recommendation**: [which and why, considering our project context]
**Sources**: [urls]
```

### Full Report
```markdown
# Research: [Topic]

**Question**: [what was investigated]
**Date**: [ISO date]
**Sources**: [count]

## Summary
[3-5 sentences answering the research question]

## Findings

### [Finding title]
**Confidence**: HIGH / MEDIUM / LOW
**Sources**: [list]
[details]

## Recommendations
1. [recommendation with rationale]
2. [recommendation with rationale]

## Sources
- [Source title] — [URL] — [what it provided]

## Open Questions
- [anything unresolved]
```

## 6. Project Context

Instead of relying on a static list, read project context dynamically:
- Read a root `CLAUDE.md` or `AGENTS.md` only when one exists and local constraints affect
  the answer.
- Inspect manifests only when the recommendation depends on installed versions or stack.
- Reference local patterns only when they change the recommendation; if you cite a file or
  function, open it with `Read` first rather than speculating.

This ensures recommendations stay aligned with the project as it evolves. Missing optional tools
or sources are a recorded limitation, not a passed check.

## 7. Before Returning

- [ ] Sources are cited with URLs
- [ ] Information is current (dates checked)
- [ ] Findings are relevant to our project context
- [ ] Recommendations are actionable (not just "it depends")
- [ ] Conflicting information is flagged, not hidden
