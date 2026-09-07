# Antigravity CLI reference

The installed `agy` binary is authoritative. Verify before composing a
command:

```bash
command -v agy
agy --version
agy --help
```

Use the locally supported one-shot/print mode, path injection, timeout, output
format, and web-grounding controls. Do not infer a model flag or persisted
settings path from this file. If the provider routes models through its own
configuration, omit a model override.

The prompt must carry repository root, task/requirements path, changed files or
diff scope, and concrete questions. For research, request URLs and distinguish
provider-sourced claims from local repository evidence. Capture the result and
record provider version, scope, exit status, and verification gaps.

## Historical compatibility note

Earlier workflow copies described `agy -p`, `--print-timeout`, a persisted
default model, and a specific `v1.0.1` behavior. Treat those as historical
examples. Verify each flag and output behavior with the installed `agy --help`
before using them for a legacy task.

If `agy` is absent or cannot provide the requested capability, report it and
stop. Installation, update, sign-in, or settings changes are separate
user-authorized actions; do not run a remote installer from this reference.
