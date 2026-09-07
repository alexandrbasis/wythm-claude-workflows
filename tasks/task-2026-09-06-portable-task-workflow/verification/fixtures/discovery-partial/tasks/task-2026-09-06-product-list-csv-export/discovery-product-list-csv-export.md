# Discovery: Product list CSV export

**Created**: 2026-09-06
**Status**: Draft
**Task context**: [TASK.md](TASK.md)

> This is a greenfield inventory-product capability. No implementation or product documentation was found in the target repository.

## Feature Overview
An authorized operator can export the product list currently shown under the active filters as a CSV file. The export contains the product name, SKU, and quantity, uses UTF-8 encoding, and omits columns the operator has hidden.

## Why This Exists
- Operators need a portable copy of the product list they are currently working with.
- Exporting the current filtered view keeps the file aligned with the operator's active working context.
- A stable, UTF-8 CSV supports downstream spreadsheet and data-processing workflows.

## Usage Context
- **Who**: An authorized operator.
- **When**: After applying or otherwise having an active filter on the product list and requesting an export.
- **Context**: The export reflects the current filtered list at the time the operator starts the export. The exact authorization mechanism and filter-state source are open technical-planning details.

## Chosen Direction
Use the current filtered product-list view as the export source. The export follows the operator's current visibility state and produces a CSV containing the agreed product data. This direction matches the requirement to export the current filtered list and avoids introducing a separate selection workflow.

## How It Works
- **Entry points**: The operator starts an export from the current product-list context. The exact UI or API entry point and propagation of the active filter state are open technical-planning details.
- **Core flow**:
  - The system confirms that the operator is allowed to export.
  - The system reads the current filtered product list.
  - The system includes the name, SKU, and quantity columns, subject to the hidden-column rule.
  - The system returns a UTF-8 CSV; when the filtered list is empty, the file contains headers only.
- **Key states**: Success with product rows; success with headers only for an empty list; authorization failure and export failure are possible states. Their handling is an open technical-planning detail.
- **Important edge cases**: An operator-hidden column must not appear in the export. [NEEDS CLARIFICATION: if the operator hides name, SKU, or quantity, should that column be omitted despite the fixed column list, or are hidden columns limited to other list columns?]

## In Scope
- [ ] Export the current filtered product list for an authorized operator.
- [ ] Produce a CSV encoded as UTF-8.
- [ ] Include product name, SKU, and quantity columns according to the hidden-column rule.
- [ ] Exclude columns hidden by the operator.
- [ ] Produce headers only when the filtered list is empty.

## Out of Scope
- [ ] Product implementation or code in this discovery task.
- [ ] Exporting a different dataset, such as the unfiltered catalog or a manually selected set.
- [ ] External research and cross-AI validation for this draft, as explicitly requested.

## Product Blockers
- [ ] Resolve whether `название`, `SKU`, or `количество` can be hidden by the operator and, if so, whether the hidden-column rule removes that field from the export. This changes the exact output schema and acceptance criteria.

## Key Requirements
- [ ] Only an authorized operator can perform the export.
- [ ] The export represents the current filtered product list at export time.
- [ ] The CSV is UTF-8 encoded and contains the agreed product columns in the requested visibility state.
- [ ] An empty filtered list produces a file containing only the CSV headers.
- [ ] User-hidden columns are absent from the export.
- [ ] The export action delivers the resulting CSV to the operator.

## Open Technical-Planning Details
- The export entry point and how the current filters are carried into the export operation.
- The existing authorization source, permission wiring, and denial feedback.
- CSV delimiter, quoting/escaping, line endings, header spelling/order, and BOM policy; the product requirement fixes UTF-8 but does not select these serializer conventions.
- File delivery mechanism, filename, loading feedback, and export-error feedback.

## Constraints
- The repository is greenfield; the README states that no implementation exists.
- UTF-8 encoding, current-filter context, the three requested product fields, empty-list headers-only behavior, and hidden-column exclusion are agreed constraints for downstream planning.
- Authorization must be enforced, but no authorization model is available in the current repository.
- Only the fixed-columns versus hidden-columns interaction is a product blocker. The other open details are explicitly deferred to technical planning and do not block this discovery.

## Notes
- Local evidence inspected: `README.md` only; it identifies a greenfield inventory product and provides no existing data model or UI contract.
- Grill summary: the fixed-columns versus hidden-columns interaction is the remaining product blocker. Entry point, authorization wiring, CSV serialization conventions, and success/error delivery are open planning details rather than product decisions.
- **Cross-AI Validation: SKIPPED — the user explicitly requested that cross-AI validation and external research be omitted for now.**
