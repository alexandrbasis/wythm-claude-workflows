# Antigravity prompt templates

Read `../codex-cli/references/cross-ai-run.md` first. Resolve every bracketed
value and verify the `agy` command with `agy --help`; these are prompt shapes,
not executable commands.

## Review

```text
Return the final review only.
Review <diff scope or files> in <repo-root>.
Check against <resolved requirements path>.
Focus on <correctness, security, edge cases, compatibility, tests>.
Use @<path> only for verified existing files. Do not edit files.
```

## Web-grounded research

```text
Research <question> and return concise findings with source URLs.
Separate sourced claims, repository observations, and unresolved assumptions.
Use @<verified repository paths> only when local context is needed.
Do not modify files.
```

## Approach validation

```text
Evaluate the approach for <objective>.
Repository: <repo-root>
Task/requirements: <resolved-task-path-or-brief>
Relevant files: <verified paths>
Focus on <risks, alternatives, invariants, verification>.
Return a concise recommendation. Do not edit files.
```

The wrapper selects the installed provider's one-shot syntax, timeout, model
behavior, output capture, path syntax, and least-privilege flags after local
verification.
