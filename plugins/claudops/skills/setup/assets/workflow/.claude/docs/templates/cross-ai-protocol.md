# Cross-AI Validation Protocol

Output format reference for skills that run cross-AI validation.

## 1. Invoke Skills

Invoke the configured available validator skills (currently `/codex-cli`, `/antigravity-cli`, and
`/cursor-cli`) with the calling skill's **FOCUS** and **FILE_REFS**. Do not invent a provider or
block a task because an optional adapter is absent. Each adapter handles its own binary flags and
returns a receipt with provider, actual model when known, version, scope, exit status, result path,
and retained stderr.

For an explicit Gemini perspective, `/antigravity-cli` must discover a current `gemini-*` slug
from `agy models`, pass that exact slug, and label the source `Gemini <slug> via Antigravity (agy)`.
When the model is omitted, label the source `Antigravity (agy; model unverified)` until the receipt
reports the actual model; never infer Gemini or claim model-level independence from the provider
name alone.

For Cursor, select a current model slug when the requested independence requires
it. Label `auto` or an unreported default model as unverified; the Cursor brand
does not establish a separate model family. Native completed output requires
`type: result`, `subtype: success`, `is_error: false`, and a non-empty `result`,
in addition to exit 0. Retain workspace-trust failures and visibly incomplete
answers as `PARTIAL`.

- **All configured validators available** → invoke in parallel, then produce comparison table + validation (sections 2-4)
- **Two or more available** → invoke those in parallel, produce comparison table + validation
- **One available** → invoke solo, skip comparison table, produce single-source verdict (section 4)
- **None available** → write `**Status**: SKIPPED — no cross-AI CLI available` → stop

## 2. Comparison Table (multi-agent mode only)

| # | Finding | Codex | Antigravity (agy) | Cursor | Agreement |
|---|---------|-------|--------|--------|-----------|
| 1 | [description] | [severity or —] | [severity or —] | [severity or —] | YES / NO |

De-duplicate by semantic equivalence. "—" means that AI didn't flag it.
If severity differs, use the higher one.
When fewer than three adapters ran, omit absent columns. Use the provider/model labels from the
receipts in source cells and findings; do not relabel an unverified default as Gemini.

## 3. Validation

For each finding, verify against actual code:

| # | Finding | Source | Valid? | Rationale |
|---|---------|--------|--------|-----------|
| 1 | ... | all / codex+antigravity / codex+cursor / antigravity+cursor / codex / antigravity / cursor | VALID / INVALID | [evidence from code] |

- **VALID**: Verifiable in code. Propagates to verdict.
- **INVALID**: Factually wrong (wrong file, misread logic, non-existent pattern). Dropped with reason.
- **DISPUTED**: Some AIs found it, others didn't. Orchestrator checks code and decides.

Only VALID findings propagate to the consolidated verdict. A provider is available for comparison
only when it returned valid completed output. Missing binaries/capabilities are unavailable;
non-zero exits, timeouts, malformed JSON, blocked reads, empty responses, visibly partial responses,
or any `denied_actions` are `PARTIAL` results. They are not a no-findings source and cannot produce
a `PASSED` review. A payload with `status: SUCCESS` and process exit 0 still fails this completeness
check when its answer is empty or denied.

## 4. Consolidated Verdict

```
**Agents**: [list adapters that ran] | **Mode**: Multi / Single ([which]) / Skipped
**Status**: PASSED / FAILED / PARTIAL
**Agreement rate**: X/Y findings (multi-agent mode only)
```

Status definitions:
- **PASSED** — every selected adapter returned valid completed output, with 0 Critical and 0 Major valid findings
- **FAILED** — 1+ Critical or 3+ Major valid findings
- **PARTIAL** — one or more selected adapters returned incomplete output or were unavailable/timed out; do not present as passed

Final findings table (VALID only):

| Severity | Finding | Source | Assessment |
|----------|---------|--------|------------|
| CRITICAL / MAJOR / MINOR / INFO | [description] | codex / Antigravity (agy) / Gemini <slug> via Antigravity (agy) / cursor / all / etc. | [brief note] |
