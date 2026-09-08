# Cursor CLI reference

The installed `agent` binary is authoritative. Verify before composing a
command:

```bash
command -v agent
agent --version
agent --help
```

Use the locally supported print/one-shot command, output format, model option,
workspace/trust option, and read-only mode. Do not assume a model name, flag,
default, or output stream from this file. Omit a model override when the
caller/configuration should choose it.

The prompt must carry repository root, task/requirements path, changed files or
diff scope, and concrete review questions. Capture the result and record the
provider version, scope, exit status, and verification gaps. A result is a
second opinion, not authorization to edit files.

## Historical compatibility note

Earlier workflow copies used `composer-2`, `--mode=ask`, `--trust`, and a
specific `v2026.03.20` version. Treat those as historical values. Verify each
flag with the installed `agent --help` before using it for a legacy task.

If `agent` is absent or cannot provide the requested mode, report the missing
capability and stop. Installing/updating Cursor is a separate user-authorized
action; do not run a remote installer or write settings from this reference.
