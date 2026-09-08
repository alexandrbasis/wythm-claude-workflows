# Antigravity prompt templates

Read `../codex-cli/references/cross-ai-run.md` first. Resolve every bracketed
value, verify paths, and check `agy --help`; these are prompt shapes, not
executable commands. Use a fresh `--output-dir` per run. The runner writes
`stdout.json`, `stderr.log`, `receipt.json`, and successful `response.txt`.

## Code review

Prompt file:

```text
Return the final review only.
Review the supplied files in <repo-root> against <requirements path>.
Focus on correctness, security, edge cases, compatibility, and tests.
Do not edit files or run shell commands.
```

Run with one `--file` per verified input:

```bash
ANTIGRAVITY_SKILL_DIR="/absolute/path/to/loaded/antigravity-cli"
python3 "$ANTIGRAVITY_SKILL_DIR/scripts/review.py" \
  --prompt-file /tmp/agy-review-prompt.md \
  --file src/changed.py \
  --file tasks/requirements.md \
  --model '<exact slug from agy models>' \
  --timeout 120 \
  --output-dir /tmp/agy-review-unique
```

Run this command from the target repository root. Resolve
`ANTIGRAVITY_SKILL_DIR` from the loaded skill location; do not infer it from
the target repository's current directory.

For the configured provider default, omit `--model`. For an explicit Gemini
perspective, run `agy models`, choose a current `gemini-*` slug, pass that exact
slug, and label the receipt `Gemini <slug> via Antigravity (agy)`.

## Web-grounded research

```text
Research <question> and return concise findings with source URLs.
Separate sourced claims, repository observations, and unresolved assumptions.
Do not modify files.
```

```bash
ANTIGRAVITY_SKILL_DIR="/absolute/path/to/loaded/antigravity-cli"
python3 "$ANTIGRAVITY_SKILL_DIR/scripts/review.py" \
  --prompt-file /tmp/agy-research-prompt.md \
  --timeout 120 \
  --output-dir /tmp/agy-research-unique
```

## Approach validation

```text
Evaluate the approach for <objective>.
Repository: <repo-root>
Task/requirements: <resolved task path or brief>
Relevant files: <verified paths supplied separately>
Focus on risks, alternatives, invariants, and verification.
Return a concise recommendation. Do not edit files.
```

Pass each relevant existing file with a repeatable `--file` option. The runner
uses `agy -p --output-format json --print-timeout`; do not substitute the old
`--approval-mode` or `-o` forms. Inspect `status`, non-empty `response`,
optional `structured_output`, `denied_actions`, exit status, and stderr before
treating the result as complete.
