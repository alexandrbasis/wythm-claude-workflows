# Codex prompt templates

Read `references/cross-ai-run.md` first. Resolve every bracketed value from
the caller, task context, repository, or installed `codex --help`; never run a
template with unresolved markers.

## Approach validation

```text
Evaluate the proposed approach for <objective>.
Repository: <repo-root>
Task or requirements: <resolved-task-path-or-brief>
Relevant files: <paths>
Focus on: <risks, alternatives, invariants, verification>
Return: concise findings and a recommended approach. Do not edit files.
```

## Review

```text
Review <diff scope or changed files> in <repo-root>.
Check against <resolved requirements path>.
Focus on <correctness, security, edge cases, compatibility, tests>.
For each finding include severity, file:line, evidence, and a concrete fix.
Return findings only; do not edit files.
```

## Research or explanation

```text
Answer <question> using the supplied repository context.
Inspect <paths> and distinguish observed facts from assumptions.
Return <requested format> with unresolved evidence gaps.
Do not modify files.
```

The wrapper chooses the installed CLI's one-shot syntax, model behavior, output
capture, and least-privilege flags after local help verification. These prompt
templates do not prescribe a model, install command, or current flag set.
