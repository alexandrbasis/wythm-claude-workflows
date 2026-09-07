# Detailed planning

Use this reference when a plan has material migration, permission, integration,
coverage or coordination risk, or the user requests a detailed decomposition.
Add only detail that resolves that risk; keep the existing task and accepted decisions.

## Detail that earns a place

| Trigger | Add to the plan |
|---------|-----------------|
| Entity creation, update or deletion | Relevant defaults, persistence, immediate feedback and visibility on affected surfaces; handling of existing data when needed |
| User-facing validation or asynchronous interaction | Applicable error/loading/empty/success behavior and how users recover; connect service constraints to the affected UI |
| Migration, permissions or external contract | Compatibility, failure handling, access boundaries and a safe rollout/recovery approach |
| Many interacting requirements | One requirement-to-verification mapping, reusing source IDs and linking implementation steps |
| Independent delivery phases | Functional outcomes, dependency order and the contracts each phase introduces or consumes |

Resolve domain terminology from existing project sources. Read the architecture-language
reference when the plan makes architectural guarantees that need its vocabulary.
Ground decisions in inspected files; choose ordinary implementation details directly.

## Separate document, when useful

Use the task's existing plan format. If no suitable format exists, start from
`.claude/docs/templates/technical-decomposition-template.md`, resolved through the
shared task context. The template is a scaffold: omit irrelevant sections and keep
equivalent existing headings. Preserve legacy links and source requirement IDs.

Define observable completion and suitable verification before detailing implementation.
Tests should describe required behavior; Given/When/Then helps when a scenario needs it.
Use actual commands with their owning package. Keep each requirement in one authoritative
place and link it from steps instead of maintaining duplicate acceptance ledgers.
Task tracking and eventual execution evidence stay in the existing task record.

## Independent review

Use `plan-reviewer` when an independent pass can resolve a specific readiness risk,
or when requested. Supply the active plan, relevant evidence and the review question.
For architectural risk, use a reviewer that accepts plans, or assess that risk directly;
an implementation-only reviewer is not a plan reviewer.

Use `/analyze` for a material spec/plan coverage problem, not as another obligatory
review of the same facts. Cross-AI validation is optional: use the resolved
`.claude/docs/templates/cross-ai-protocol.md` when warranted and available. Incorporate
findings once; record an unavailable required check as a limitation, never as passed.

## Splitting

Consider a split when distinct deliverable outcomes or prerequisites make execution
and review safer. Keep tightly coupled work together. A phase introduces its contracts
before or with its first consumer; no earlier phase may depend on a later guessed contract.

Ask `task-splitter` to evaluate a concrete candidate boundary when helpful, passing the
active plan even if it is a section of `TASK.md`. If that capability is unavailable,
evaluate the same boundaries directly. A no-split decision fits in the existing plan.

Present a proposed phase structure for the user's decision unless that exact split is
already authorized. After approval, `task-decomposer` or the caller creates phase folders
and plans. The parent links each phase and dependency; phases link the parent and their
active inputs. Preserve requirement and verification coverage across phases. Hand `/si`
the first active phase; completing it does not complete the parent feature.
