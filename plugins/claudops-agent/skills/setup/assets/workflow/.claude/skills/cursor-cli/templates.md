# Cursor prompt templates

Read `../codex-cli/references/cross-ai-run.md` first. Resolve every bracketed
value and verify the command flags with `agent --help`; pass the completed prompt file to
`scripts/review.py` as described in `SKILL.md`.

## Review

```text
Review <diff scope or changed files> in <repo-root>.
Check against <resolved requirements path>.
Focus on <correctness, security, edge cases, compatibility, tests>.
Return severity, file:line, evidence, and a concrete fix for each finding.
Use the supplied inline evidence; do not edit files or run shell commands.
```

## Approach validation

```text
Evaluate the approach for <objective>.
Repository: <repo-root>
Task/requirements: <resolved-task-path-or-brief>
Relevant files: <paths>
Focus on <risks, alternatives, invariants, verification>.
Return a concise recommendation. Use the supplied inline evidence; do not edit files or run shell commands.
```

## Security or performance pass

```text
Inspect <changed files or diff scope> in <repo-root> for <security/performance focus>.
Use <requirements or task path> as context.
Separate observed evidence from assumptions and return actionable findings only.
Use the supplied inline evidence; do not edit files or run shell commands.
```

Pass every required file through repeatable `--file` options. Paths written in a
prompt do not prove that Cursor read their contents. Include the expected scope
and require the response to state any missing evidence. Ask for no tool use when
the inlined inputs are sufficient. Read both the response and receipt before
calling the review complete.
