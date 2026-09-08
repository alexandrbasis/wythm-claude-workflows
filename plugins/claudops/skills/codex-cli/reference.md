# Codex CLI reference

This file is a lookup aid, not a pinned compatibility contract. The installed
binary is authoritative. Start with:

```bash
command -v codex
codex --version
codex --help
codex exec --help
codex exec review --help
```

Use only subcommands and flags shown by that local help. Keep reviews in the
least-privilege mode the installed CLI supports, capture the documented output,
and use the model selected by the caller or configured profile. Omit `-m` when
the configured default is intended. Do not install, update, or write settings
from this reference.

## Common capabilities to verify locally

Recent installations may expose a non-interactive `codex exec`, a review
subcommand, a model option, sandbox/approval options, and an output-file option.
Their names, combinations, and output streams can change. In particular,
verify whether a review accepts a custom prompt together with a scope flag and
where findings are written before constructing a command.

The prompt should include the repository root, task/requirements path, changed
files or diff scope, focus areas, and the request to return findings without
editing files. Persist the provider version, scope, output location, exit
status, and verification gaps as the cross-AI receipt.

## Historical compatibility note

Older workflow copies described Codex CLI v0.116.x, `gpt-5.4`, `--full-auto`,
and differences between `codex review` and `codex exec review`. These are not
current defaults. Consult local help before using an old task's exact command;
do not copy its model or autonomous-write flags into a new run.

If the binary is missing or a required capability is unavailable, report that
fact and stop. Installing/updating Codex or changing its profile is a separate
user-authorized action.
