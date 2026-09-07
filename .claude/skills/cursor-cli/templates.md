# Cursor prompt templates

Read `../codex-cli/references/cross-ai-run.md` first. Resolve every bracketed
value and verify the command flags with `agent --help`; these are prompt
templates, not executable commands.

## Review

```text
Review <diff scope or changed files> in <repo-root>.
Check against <resolved requirements path>.
Focus on <correctness, security, edge cases, compatibility, tests>.
Return severity, file:line, evidence, and a concrete fix for each finding.
Do not edit files.
```

## Approach validation

```text
Evaluate the approach for <objective>.
Repository: <repo-root>
Task/requirements: <resolved-task-path-or-brief>
Relevant files: <paths>
Focus on <risks, alternatives, invariants, verification>.
Return a concise recommendation. Do not edit files.
```

## Security or performance pass

```text
Inspect <changed files or diff scope> in <repo-root> for <security/performance focus>.
Use <requirements or task path> as context.
Separate observed evidence from assumptions and return actionable findings only.
Do not edit files.
```

The wrapper selects the installed provider's one-shot syntax, model behavior,
output capture, timeout, and least-privilege flags after local verification.
