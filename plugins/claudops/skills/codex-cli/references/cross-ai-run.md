# Cross-AI one-shot run

This reference is shared by the Codex, Cursor, and Antigravity wrappers. It
defines the lifecycle; each wrapper owns only its binary, flags, output mode,
and provider-specific restrictions.

## Invocation boundary

Run a provider only when the user explicitly names it or another skill passes a
specific delegation. Choose one provider unless the caller explicitly requests
fan-out. A provider result is evidence for the caller; it never authorizes
edits, commits, tracker writes, publication, or deployment.

## Context and transport

For a task-attached run, resolve `../../setup/references/task-context.md` from
this reference (or `../setup/references/task-context.md` from an entrypoint)
and retain the provider, prompt scope, binary version,
result path, and verification receipt in that task's evidence area. A
standalone lookup or review uses a temporary output file and does not create a
fake task. `/tmp` is transport, not durable evidence.

Give the provider every path and requirement it needs: the task record when
applicable, changed files or diff scope, repository root, and concrete review
questions. The provider starts without conversation context.

For Antigravity, read `../../antigravity-cli/SKILL.md` and
`../../antigravity-cli/reference.md` for the provider runner's exact invocation,
file-inlining, artifact, model-label, and bounded-input rules. Run its runner
from the target repository root after resolving the loaded skill directory.

For Cursor, read `../../cursor-cli/SKILL.md` and
`../../cursor-cli/reference.md` for its bounded runner and native result
contract. It uses explicit ask mode and stops on missing workspace trust.

## Preflight and model

Before the first call, verify the provider is available with `command -v` and
read its `--version` or `--help` when flags or output behavior matter. If the
binary is missing or its installed version lacks a needed capability, stop and
report a separate install/update action. Do not run a global package install,
remote installer, self-update, or settings write implicitly.

Use a model selected by the caller or configured by the provider. If no model
was selected, omit the model override and let the installed provider use its
configured default; the runner has no model default. For an explicit Gemini
perspective through Antigravity, discover a current `gemini-*` slug with
`agy models`, pass that exact slug, and record the provider plus actual model.
If the default model is not reported, label its identity unverified and do not
claim model-level independence. Never pin a model because this reference was
written at a particular date, and never auto-fallback to another vendor.

Use the least-privilege/read-only mode supported by the local help for review
and research. Do not pass autonomous write, force, or permission-bypass flags
unless the caller explicitly requested that behavior.

## Run, capture, and verify

Use the provider's one-shot mode and its documented output capture. For
Antigravity, the tested shape is `agy -p --output-format json
--print-timeout <duration>`; `--approval-mode` and `-o` are legacy forms and
are rejected by the tested CLI. Keep the prompt and result bounded; choose a
timeout appropriate to the provider and record it. Read the captured result,
check exit status, and distinguish a provider opinion from independently
verified repository evidence.

For Antigravity JSON results, accept a completed result only when process exit
is 0, the payload status is `SUCCESS`, `response` is non-empty, and
`denied_actions` is absent or empty. Keep stderr even on exit 0. Empty,
blocked, denied, malformed, timed-out, or visibly partial output is `PARTIAL`,
including `SUCCESS` plus exit 0; it is not a no-findings result and cannot
support a passed review. Other adapters use their native envelopes but must
meet the same completed-output and evidence standard. Do not retry implicitly,
change settings/auth, or bypass permissions.

For Cursor JSON, require exit 0, `type: result`, `subtype: success`,
`is_error: false`, and a non-empty string `result`. Treat workspace-trust
rejection as incomplete, and inspect otherwise valid answers for missing scope
or blocked reads. Cursor's `auto` routing or an unreported model default does
not establish independence from the main model.

The wrapper should return a compact receipt containing provider, version,
scope, prompt purpose, output location, exit status, and verification gaps.
When task-attached, persist that receipt through the task contract.

## Historical compatibility notes

Older local copies used `gpt-5.4`, Cursor `composer-2`, and Codex CLI v0.116.x
examples. Those values are historical examples only. If a legacy task requires
their exact flags, compare them with the installed binary's help and use them
only when supported; do not copy them into new commands.
