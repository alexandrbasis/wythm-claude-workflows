# Antigravity CLI (agy) Prompt Templates

> **Model**: persisted default (no `-m` flag — set via `/model` or settings.json).
>
> **Before running**: every `@path` must exist; for paths outside the cwd workspace also pass `--add-dir <dir>`.

**Output pipeline** (appended to every template — shown once, abbreviated as `# ...pipeline` below):
```bash
--print-timeout 5m > /tmp/agy-result.txt 2> /dev/null && echo "Antigravity completed"
```
Read result with the **Read tool** on `/tmp/agy-result.txt` — `agy -p` already prints clean final-answer text (no JSON, no `jq` needed). `cat` would dump the full payload back into the conversation.

---

## Approach Validation

### Architecture Decision
```bash
agy -p "Respond with the final answer only.
I need to decide between approaches for [feature]:
Option A: [Description] — Pros: [...] Cons: [...]
Option B: [Description] — Pros: [...] Cons: [...]
Context: [project context, file paths]. Requirements: [key requirements].
Which approach would you recommend and why?" # ...pipeline
```

### Pre-Implementation Review
```bash
agy -p "Respond with the final answer only.
Review this implementation approach for @[task-file-path]:
1. [Step 1]  2. [Step 2]  3. [Step 3]
Is this aligned with requirements? What issues might I encounter?" # ...pipeline
```

---

## Code Review

### Custom Review Focus
```bash
agy -p "Respond with the final answer only.
Review uncommitted changes in this repository. Focus on:
1. [Focus area 1]  2. [Focus area 2]  3. [Focus area 3]
Provide specific feedback for each area." # ...pipeline
```

### File-Specific Review with Context
```bash
agy -p "Respond with the final answer only.
Review implementation in @[file1.ts] and @[file2.ts].
Check against requirements in @[tech-decomposition.md].
Focus on: correctness, edge cases, error handling." # ...pipeline
```

---

## Security Review

### General Security Audit
```bash
agy -p "Respond with the final answer only.
Security review of uncommitted changes. Check for: SQL/NoSQL injection, XSS,
command injection, auth issues, sensitive data exposure, input validation gaps.
Report findings with severity (Critical/High/Medium/Low)." # ...pipeline
```

### API Security Review
```bash
agy -p "Respond with the final answer only.
Review @[file/endpoint] for API security: rate limiting, input validation,
authentication, authorization, error info leakage, CORS configuration." # ...pipeline
```

---

## Implementation Verification

### Feature Completion Check
```bash
agy -p "Respond with the final answer only.
Verify [feature] implementation is complete per @[task-file-path].
Requirements: 1. [...] 2. [...] 3. [...]
Key files: @[file1] @[file2]
Check: all requirements met? Edge cases? Error handling? Test coverage?" # ...pipeline
```

### Refactoring Verification
```bash
agy -p "Respond with the final answer only.
Verify this refactoring preserves behavior.
Original behavior: [description]. Changed files: @[file1] @[file2].
Check: functionality preserved? Subtle behavior changes? New edge case bugs?" # ...pipeline
```

---

## Test Assessment

### Test Coverage Review
```bash
agy -p "Respond with the final answer only.
Review test coverage for @[file/module]. Key functionality: [Function 1], [Function 2].
All public functions tested? Edge cases? Error paths? What is missing?" # ...pipeline
```

---

## Performance & Bug Investigation

### Performance Analysis
```bash
agy -p "Respond with the final answer only.
Analyze @[file/function] for performance: inefficient algorithms, memory leaks,
blocking operations, missing caching, N+1 query patterns." # ...pipeline
```

### Bug Root Cause Analysis
```bash
agy -p "Respond with the final answer only.
Investigate bug — Symptom: [what happens]. Expected: [what should happen].
Context: [relevant info]. Suspected files: @[file1] @[file2].
Find root cause and suggest a fix." # ...pipeline
```

---

## Web Research (Google Search Grounding)

Antigravity inherits Gemini's native Google Search grounding — its advantage over other CLI tools. Read-only web tools work in `-p` mode without `--dangerously-skip-permissions`.

### Current Information with Google Search
```bash
agy -p "Respond with the final answer only.
Search the web for current information about [topic] as of [date].
Summarize key points with source URLs." # ...pipeline
```

### Library/API Research
```bash
agy -p "Respond with the final answer only.
Research [library/API] via web search: latest version, recent changes,
best practices, common patterns, known gotchas, migration notes from [version]." # ...pipeline
```

### Comparison Research
```bash
agy -p "Respond with the final answer only.
Compare [option A] vs [option B] for [use case]. Search the web for current
benchmarks and community opinions. Provide recommendation with rationale." # ...pipeline
```

---

## Integration Patterns

### Generate-Review-Fix Cycle

Claude generates code, Antigravity reviews, Claude fixes — three-step quality loop.

```bash
# 1. Claude generates code (in this conversation)
# 2. Antigravity reviews Claude's work
agy -p "Respond with the final answer only.
Review @[generated-file] for bugs, security issues, and improvements.
List each finding with severity." # ...pipeline
# 3. Claude reads review via Read tool and applies fixes
```

### Cross-Validation with Claude

Second opinion on architecture, security, or complex logic.

```bash
agy -p "Respond with the final answer only.
Evaluate this approach: [Claude's proposed approach].
Risks, blind spots, or better alternatives?" # ...pipeline
```

### Structured (JSON) Output for Programmatic Processing

`agy` has no JSON output flag — instruct it to emit JSON *as text*, then validate with `jq`:

```bash
agy -p "Respond with valid JSON only — no markdown fences, no explanation.
[PROMPT requiring structured output]" \
  --print-timeout 5m > /tmp/agy-structured.txt 2> /dev/null \
  && jq '.' /tmp/agy-structured.txt > /tmp/agy-structured.json \
  && echo "Antigravity completed"
```

### Multi-line Prompt with HEREDOC

For prompts too long for inline quoting.

```bash
PROMPT=$(cat <<'AGY_PROMPT'
Respond with the final answer only.
[Long multi-line prompt here.
Include @file/paths for context.]
AGY_PROMPT
)
agy -p "$PROMPT" --print-timeout 5m > /tmp/agy-result.txt 2> /dev/null \
  && echo "Antigravity completed"
```
