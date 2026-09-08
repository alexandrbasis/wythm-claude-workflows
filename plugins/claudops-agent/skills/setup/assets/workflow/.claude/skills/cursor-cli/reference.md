# Cursor CLI reference

## Native invocation and model selection

Verify `agent --version`, `agent --help`, and `agent models` on the current host.
The runner uses the documented one-shot shape:

```text
agent -p --mode ask --output-format json [--model <selected-slug>] <prompt>
```

`--print` alone is not a read-only boundary: local help explicitly grants write
and shell tools. Keep `--mode ask` for a review. Workspace trust is checked
separately even in ask mode. A trust error must remain incomplete; the adapter
never enables trust or permission bypass implicitly.

Select a slug from the current model listing when a particular perspective is
required. `auto` is routing, not a verified model identity. A requested model is
not independently confirmed merely because the command accepted its slug.
Do not reuse historical `composer-2` examples or infer a model's lineage from
Cursor's provider name.

## JSON completion contract

Accept only an object with all of these fields, after process exit 0:

```json
{"type":"result","subtype":"success","is_error":false,"result":"Review text"}
```

The `result` must be a non-empty string. Preserve raw output and stderr even on
success. Error or incomplete envelopes, malformed JSON, non-zero exits,
timeouts, and empty answers cannot become a passed review. Inspect the answer
for limitations that the envelope does not encode; a successful transport may
still report an unavailable file or an unfinished analysis. This adapter does
not consume `stream-json` or partial deltas as a final answer.

## Runner artifacts and bounds

The adjacent `scripts/review.py` requires a verified prompt file, positive finite
`--timeout` in seconds, and a new `--output-dir`. Optional `--file` arguments are
pre-read and inlined; optional `--model` has no runner default. Python 3.10+ is
required. Combined UTF-8 input is capped at 96 KiB to keep one-shot argv bounded.

The process has a hard timeout and its process group is terminated on expiry.
Artifacts include `stdout.json`, `stderr.log`, `version.stderr.log`, and
`receipt.json`; only completed output produces `response.txt`. A failed version
preflight produces a receipt and version stderr without starting the review.
The receipt records scope, requested model/default uncertainty, version, purpose,
output paths, exit status, and verification gaps. It does not grant permission
to edit or publish the reviewed project.

## Verified local compatibility

On 2026-09-08, Cursor Agent `2026.09.02-c22c1a3` accepted the shape above and
returned the illustrated completion envelope. The account listed `auto` as its
default and `composer-2.5` among available models. These are dated observations,
not pinned defaults. A new temporary workspace rejected the same call without
trust; an explicitly trusted synthetic fixture completed in ask mode.

## Official sources

- [CLI parameters](https://cursor.com/docs/cli/reference/parameters) — supported
  flags and the separate workspace-trust prompt.
- [Output format](https://cursor.com/docs/cli/reference/output-format) — JSON
  result envelope, error output, and stream events. JSON does not report the
  resolved model; preserve the requested slug without claiming confirmation.
- [Permissions](https://cursor.com/docs/cli/reference/permissions) — configured
  tool permissions. The runner leaves these settings unchanged.
- [CLI usage](https://cursor.com/docs/cli/using) — ask and plan modes. Read-only
  mode is provider behavior, not proof of OS-level sandbox isolation.
