---
name: antigravity-cli
description: >-
  Run Google Antigravity CLI (agy) for web-grounded research, cross-AI review, or validation.
  Use when a request needs Antigravity's Google Search grounding or a distinct cross-AI
  perspective, or when a caller explicitly delegates to agy. Do not select it for an
  ordinary review or research request that does not need those capabilities. One-shot only.
allowed-tools:
  - Bash
  - Read
---

# Antigravity CLI Integration Skill

> **Announcement**: Begin with: "I'm using the **antigravity-cli** skill for cross-AI validation with Antigravity (agy)."

Invoke the Google Antigravity CLI (`agy`) for one-shot code review, web-grounded research, and cross-AI verification. `agy` is the successor to the Gemini CLI — Google [transitioned Gemini CLI to Antigravity CLI](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/) on 2026-05-19. It shares the Antigravity 2.0 agent harness and is built in Go.

## Self-Update: Official Documentation

When the skill feels outdated (wrong flags, unknown behavior, new features), consult these
official sources to update commands and reference files:

| Resource | URL |
|---|---|
| CLI overview | https://antigravity.google/docs/cli-overview |
| Using the CLI | https://antigravity.google/docs/cli-using |
| CLI features (slash commands, settings) | https://antigravity.google/docs/cli-features |
| GitHub repo (issues, releases) | https://github.com/google-antigravity/antigravity-cli |
| Transition announcement | https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ |

The most authoritative source is the local binary itself — run `agy --help` and `agy changelog`.

Use `WebFetch` or `mcp__exa__web_search_exa` to check for updates only when:
- An `agy` command fails with an unknown flag error
- The user asks about an Antigravity feature not covered here
- The user explicitly asks to verify this skill against upstream documentation

> **Last verified**: 2026-05-22 (agy v1.0.1, print mode, default-model routing). Flags and output format confirmed empirically via `agy --help` and live one-shot calls.

## Prerequisite Check

Before running any `agy` command, verify installation:

```bash
command -v agy >/dev/null || { echo "ERROR: antigravity CLI not installed. Run: curl -fsSL https://antigravity.google/cli/install.sh | bash"; exit 1; }
```

Auth is via the system keyring / Google Sign-In (no API key, no `-o json`). If `agy -p` returns an auth error, the user must run `agy` once interactively to sign in.

## Core Patterns

### 1. Custom Prompt (most common)

The canonical pattern: run `agy -p`, redirect the plain-text response straight to a file. There is **no JSON wrapper** — `agy -p` prints only the final answer to stdout (no thinking tokens, no tool traces), so no `jq` extraction is needed.

```bash
agy -p "Output ONLY the final answer. Task: [your prompt] @file/paths" \
  --print-timeout 5m \
  > /tmp/agy-result.txt 2> /dev/null \
  && echo "Antigravity completed"
```
Then read with **Read tool**: `/tmp/agy-result.txt`

**Why this works**: `agy -p` (alias `--print` / `--prompt`) runs a single prompt non-interactively and prints the response. `--print-timeout` is the CLI's built-in wait cap (default 5m). `2> /dev/null` suppresses startup noise. This replaces gemini's `-o json` + `jq -r '.response'` pipeline — `agy` already emits clean final-answer text.

### 2. Code Review

```bash
agy -p "Respond with the final review only — concise, fact-forward.
Review these files for bugs, security issues, and improvements:
- @path/to/file.ts
- @path/to/other-file.ts
Check against requirements in: @tasks/task-doc/tech-decomposition.md
Focus on: correctness, edge cases, error handling" \
  --print-timeout 5m \
  > /tmp/agy-review.txt 2> /dev/null \
  && echo "Review completed"
```
Then read with **Read tool**: `/tmp/agy-review.txt`

### 3. Web Research (Google Search Grounding)

Antigravity's differentiator over other CLI tools: native Google Search grounding (inherited from the Gemini CLI lineage). Verified to work in `-p` mode — read-only web tools run without needing `--dangerously-skip-permissions`.

```bash
agy -p "Respond with the final answer only — concise, fact-forward.
Search the web to find: [topic]. Cite sources with URLs.
Format: markdown with bullet points." \
  --print-timeout 3m \
  > /tmp/agy-research.txt 2> /dev/null \
  && echo "Research completed"
```
Then read with **Read tool**: `/tmp/agy-research.txt`

### 4. Background Execution (for long tasks)

For complex tasks that take 2-10 minutes. When you have multiple *independent* `agy` queries (e.g. a security review and a perf review of the same diff), launch them in the same turn as separate background Bash calls — don't serialize.

```bash
# Use Bash tool with run_in_background=true
agy -p "[complex prompt with @file references]" \
  --print-timeout 8m \
  > /tmp/agy-result.txt 2> /dev/null \
  && echo "Antigravity completed"
```

**Workflow**:
1. Run with `run_in_background: true` on the Bash tool
2. If there are other independent `agy` calls, fire them in the same turn (different output files: `/tmp/agy-sec.txt`, `/tmp/agy-perf.txt`)
3. Continue working on other tasks while `agy` runs
4. You will be notified automatically when each completes
5. Read each result with the Read tool
6. Summarize findings to the user

### 5. Extra Workspace Directories

`agy` operates on the current working directory as its workspace. To grant access to files outside it, add directories with `--add-dir` (repeatable):

```bash
agy -p "Review @../shared/lib.ts against @./src/main.ts" \
  --add-dir ../shared \
  --print-timeout 5m > /tmp/agy-result.txt 2> /dev/null
```

### 6. @path Safety

Verify every `@path` reference points to a real file before invoking — a missing path produces a degraded answer or wasted wall-clock. A quick `ls` or `[ -f path ]` guard is enough. `@path` injects file contents into the prompt context (it is **not** a tool call), so it works in `-p` mode without any permission flag.

## Critical Rules

### Use `-p` for One-Shot

Claude Code can only drive `agy` non-interactively. Without `-p`, the CLI drops into its TUI in a TTY and hangs the Bash call. `-p`, `--print`, and `--prompt` are aliases.

### Do NOT Use `--dangerously-skip-permissions`

`agy` auto-approves all tool calls (including shell + file writes) when given `--dangerously-skip-permissions`. **Claude Code's auto-mode classifier blocks this flag** — it creates an autonomous agent loop. You don't need it: `@path` injection and read-only web search already work without it. Reserve write/shell-executing tasks for the user running `agy` interactively.

### Plain-Text Output (No JSON)

`agy -p` has no `-o json` / output-format flag. It prints the final answer as plain text directly to stdout. Just redirect to a file and Read it — no `jq`. Read the result file with the **Read tool**; `cat` on a long review would dump the full payload back into the conversation.

### Model Selection

There is no `-m` flag for one-shot mode. The model is whatever was last persisted via the interactive `/model` slash command or `~/.gemini/antigravity-cli/settings.json`. Don't try to pass a model on the command line — it's not a recognized flag.

### Antigravity Has No Context From This Conversation

`agy` starts with zero context — it cannot see this conversation, open files, or prior turns. For any useful answer, the prompt itself has to carry what it needs:
- Task/requirement file paths via `@path`
- Implementation file paths for review targets
- Extra directories via `--add-dir` when broader context matters

### One-Shot Only

`agy -p` runs non-interactively and starts a fresh conversation each invocation. No follow-up questions, no conversation state. Craft your prompt to be complete and self-contained.

After the command completes, read the captured result and report what it established. A
one-shot review or research result is evidence for the caller; it does not authorize edits,
shell work, or publication by Antigravity.

### Timeout

Always set `--print-timeout` (the CLI's own wait cap; default 5m) AND a Bash tool `timeout`. Note: macOS has no `timeout` shell command (`gtimeout` only via coreutils) — rely on `--print-timeout` plus the Bash tool's `timeout` parameter, not a shell `timeout` wrapper.

| Task Type | `--print-timeout` | Bash tool `timeout` |
|---|---|---|
| Simple query | `2m` | `120000` |
| Code review (small) | `4m` | `240000` |
| Code review (large) / directory analysis | `8m` | `480000` |
| Web research | `3m` | `180000` |

### When NOT to Use

- Simple, quick tasks (overhead not worth the 1-10 min wait)
- Tasks requiring interactive conversation/refinement
- Trivial changes (typos, formatting)
- Simple web search (use Exa tools or /deep-research instead)
- Tasks that require the agent to write files or run shell commands (needs `--dangerously-skip-permissions`, which is blocked — use the interactive TUI)

## Reference Files

Read these as needed — they are NOT loaded into context automatically:

| File | When to Read |
|---|---|
| `reference.md` | Need exact flag syntax, config options, auth, or error handling |
| `templates.md` | Need a structured prompt template for a specific review or research type |
