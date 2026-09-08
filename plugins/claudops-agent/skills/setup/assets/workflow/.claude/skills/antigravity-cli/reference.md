# Antigravity CLI reference

The installed binary is authoritative. Check it before composing a call:

```bash
command -v agy
agy --version
agy --help
```

Official references: [headless CLI](https://antigravity.google/docs/cli/headless/),
[Gemini CLI migration](https://antigravity.google/docs/cli/gcli-migration/), and
[installation](https://antigravity.google/docs/cli/install/).

## Headless invocation

The tested JSON shape is:

```bash
agy -p "Return the final answer only." \
  --output-format json \
  --print-timeout 120s \
  --model '<exact slug from agy models>' \
  --effort high
```

Use `--model` and `--effort` only when supported by local help and explicitly
selected. Omit `--model` when the provider's configured default is intended.
`agy models` lists current slugs; choose and record the exact `gemini-*` slug
for an explicit Gemini run. Do not hard-code a routing chain or silently fall
back to another vendor.

The repository wrapper is the normal transport for review/research. Resolve the
loaded skill directory, then run this from the target repository root:

```bash
ANTIGRAVITY_SKILL_DIR="/absolute/path/to/loaded/antigravity-cli"
python3 "$ANTIGRAVITY_SKILL_DIR/scripts/review.py" \
  --prompt-file /tmp/agy-prompt.md \
  --file src/changed.py \
  --file tasks/requirements.md \
  --model '<exact slug from agy models>' \
  --effort high \
  --timeout 120 \
  --output-dir /tmp/agy-review-unique
```

`ANTIGRAVITY_SKILL_DIR` must point to the directory containing this loaded
skill, not a path inferred from the target repository's current directory.
`--prompt-file` is required by the runner, `--file` may be repeated, `--model`
is optional with no runner default, `--effort` is optional (`low`, `medium`, or
`high`), `--timeout` is a required positive finite number of seconds, and
`--output-dir` must be fresh. The runner pre-reads verified files and inlines
them; this avoids relying on provider `@file` reads that may be denied. It
writes `stdout.json`, `stderr.log`, `version.stderr.log`, `receipt.json`, and
`response.txt` after a successful response.

Do not use the legacy `--approval-mode` or `-o` flags. The tested Antigravity
form uses `-p`, `--output-format json`, and `--print-timeout`. Do not change
settings/auth, retry implicitly, or pass all-permission bypass flags.

## Output and validation

A JSON result contains fields such as:

```json
{
  "status": "SUCCESS",
  "response": "final answer",
  "structured_output": {"optional": "schema result"},
  "denied_actions": []
}
```

`structured_output` is optional metadata; `response` remains required. Retain
`stdout.json`, `stderr.log`, `version.stderr.log`, and `receipt.json`. Count the run as a valid
completed result only when
the process exits 0, `status` is `SUCCESS`, `response` is non-empty, and
`denied_actions` is empty or absent. Empty, blocked, denied, malformed,
timed-out, or visibly partial output is `PARTIAL`, including `SUCCESS` plus
exit 0; it is not a no-findings result and cannot support a passed review.

## Model and migration evidence

On 2026-09-08, local testing observed `agy 1.1.21` at the start and
`agy 1.1.27` later in the same test; the version changed during testing, but
the cause was not independently established. A tested Gemini request used the
discovered slug `gemini-3.8-flash-high` with `--effort high`. Treat this as a
dated local receipt, not a default or availability promise. The legacy
`gemini 0.58.0` returned `IneligibleTierError` with exit 55 for that account;
this required migration for that account and is not a universal account claim.
