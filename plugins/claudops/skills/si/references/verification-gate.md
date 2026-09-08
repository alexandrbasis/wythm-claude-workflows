# Verification recipes

Use these for requirements where a superficially passing check can miss the requested
outcome. Keep evidence in the task's existing acceptance/checklist entries; preserve existing
IDs. If no entries exist, use a compact note in the task's plan/progress section, without a
separate VC schema or duplicate ledger.

| Requirement | Evidence that proves it |
|---|---|
| Exact fields, options or counts | Compare the specified set, values and count with actual output; verify order when required. Non-empty output alone cannot prove an enumerated requirement. |
| Rendered UI or visual properties | Inspect the rendered state, relevant interactions and specified layout or appearance using suitable UI tests or the available browser. Finding a field name in source proves only code presence. |
| API request or validation contract | Exercise the public boundary and compare the relevant payload, response and success/error behavior. Use repository fixtures or a permitted environment; a URL or validator in source is not runtime evidence. |
| Navigation, mutation or async state | Exercise the action through the relevant path and observe the resulting state, including required failure/recovery behavior and affected surfaces. |

Derive expected values from the agreed requirement or authoritative repository evidence;
assert exact counts only when the requirement fixes them. Choose the smallest reliable check
that distinguishes the intended behavior from a plausible failure.

Associate uncovered acceptance with the step that delivers it. Mark an item complete only
when its required evidence is observed. Record unavailable checks, their impact and the next
action; they remain unverified. Optional checks may be left as named follow-ups when the
agreed scope does not require them, while missing required evidence blocks completion.
