# Shared task context

Use this contract when a workflow creates or advances a task. Resolve the task before
research, interviews, planning, implementation or review; save enough state for a person
or a fresh agent to continue. A standalone explanation, reference lookup or utility
command needs no artificial task. When a utility supports a task, record its relevant
result in that task.

## Resolve the repository and resources

The target repository/workspace and the installed skill directory are different roots.
Read applicable project instructions and existing conventions, including task locations
and command sources recorded in the project's `CLAUDE.md` or `AGENTS.md`. In a
monorepo, keep the selected workspace explicit and run commands in their owning package.
Obtain commands from real configuration or CI; placeholders are lookup requests, never
executable defaults. Ask only for values that cannot be established and block the work.

Resolve relative skill links and scripts from the active skill's location. For a legacy
`.claude/docs`, `.claude/scripts` or `.claude/agents` reference, use the corresponding
project resource if present; otherwise use `assets/workflow/.claude/` under the installed
`setup` skill. When using a source checkout without that bundled tree, use the source
`.claude/` directory containing the active `skills/setup` (the same fallback used by
`scripts/bootstrap_project.py`). Verify the chosen resource exists; never substitute the
consuming project's cwd for a missing resource root. For `.claude/skills/<name>` references, use the active local override or the
installed sibling skill (command aliases `quick`/`udoc` map to source folders
`si-quick`/`update-docs`). Available tools determine execution, not a named provider in an
example. If a required capability is unavailable, perform a supported equivalent or
record the specific blocked check. Never claim a skipped check passed.

A plugin can operate without copying its workflows into a project. Respect explicit
local overrides and disabled markers; do not rewrite plugin files during a task.

## Resolve agent roles in the current host

Use a named role directly only when the current host registers that agent type. Otherwise,
find its exact `name` in the applicable `.claude/agents` resource tree resolved above and
read the role's Markdown instructions. Resolve each `skills:` dependency to the active
local override or installed sibling skill and read it explicitly; portable hosts do not
preload Claude agent dependencies. Treat the role's Claude `model` and `tools` fields as
reference metadata, not host API arguments. Pass the role instructions, dependencies, bounded task
and write ownership to a supported generic worker. Role filenames are instructions, not
Codex `agent_type` values. A reviewer uses read-only ownership unless changes are requested.
Preserve any inline-only return contract; one orchestrator owns shared task/review files.

If the host cannot delegate, apply the same role and convention checks in the current
agent and report that the result lacks an independent worker. Preserve evidence and
required verification; a missing named agent does not justify skipping its review lens.
This rule applies to role names requested by individual workflows, including discovery,
planning and review.

Use the current host's equivalent for named tools in workflow examples, including file
editing and user input. If structured input is unavailable, ask the same question in
ordinary conversation. Tool naming differences alone do not create a product blocker.
Workflow references such as `/ct` mean the corresponding installed skill. If the host
has no matching slash-command or Skill tool, read and apply the sibling `SKILL.md`,
using the alias mapping above. In skill instructions, `$ARGUMENTS` means the text supplied
with that invocation; pass the actual user/task text explicitly when the host does not
substitute it.

## Find or start one task

1. An explicit task file/directory is authoritative. Follow its index, linked active
   plan and phase pointers. A supplied file outside `tasks/` stays where it is.
2. Otherwise reuse the task already established in the conversation or explicitly
   linked from the current issue/branch. Verify the link; a similar branch name alone
   is not proof. A request for a different objective starts a different task.
3. Search the configured task root or existing repository convention for the named
   objective/ID. Read candidate entrypoints, not every historical artifact. If several
   candidates remain plausible, ask which one; do not select by recency alone.
4. If no match exists, create the minimum record in the established task root. With no
   convention, use `tasks/task-YYYY-MM-DD-<slug>/TASK.md`. Check collisions first; reuse
   only a matching objective and choose a distinct slug for a different task. For a
   read-only request, return the proposed path without writing it.

Use an existing task index as the entrypoint. A single existing plan can itself serve
as the record; add compact state and links there. If several documents have no clear
entrypoint, add `TASK.md` linking them. Preserve existing names, identifiers and content;
do not create a second discovery or plan merely to fit a template. Resolve linked paths
relative to the file that owns them, and verify they exist before relying on them.

## Minimum durable record

Create the record at the start of task work, even when discovery is incomplete. Keep
these facts in one place; headings and filenames can follow the repository's vocabulary:

```markdown
# <Task title>
Objective: <observable outcome and scope>
Stage / status: <current activity; draft, ready, in progress, blocked or complete>

## Context and decisions
<Sources, agreed constraints, unresolved questions; distinguish assumptions from decisions.>

## Artifacts
<Links to existing discovery, active plan/phase, prototype, review or evidence as produced.>

## Progress and next action
<Last completed result, verification or explicit not-run reason, blocker and concrete next step.>
```

For a small task, discovery, plan, decisions and verification can be sections in this
single record. Split out a document only when it has an independent purpose, enough
detail to need separate review, or an existing consumer requires it. Templates supply
useful structure; equivalent existing sections satisfy the contract. Missing headings
are repairable from evidence; missing product decisions remain explicit questions.
Distinguish an open question from a blocker: block the next stage only when the missing
answer materially changes its scope, acceptance or safety. Routine implementation choices
can be resolved during planning; do not re-ask rules already settled by the user's request.

## Advance and hand off

Before a stage, read the entrypoint and only its relevant linked inputs. Record the
stage result, link any new artifact, update actual status and the next action before
handoff or a long pause. Resume unanswered questions and unfinished steps on re-entry.
An answer, approval, finding or check result must survive outside the chat when it
affects later work. Do not duplicate whole source documents into the record.
Reconcile derived notes and old blockers against the user's current authorized
requirements. An earlier agent's question is not a new requirement or a reason to
re-confirm an answer already supplied. Preserve actual human decisions and their source.
When relevant inputs or code change, recheck affected decisions and verification;
retain historical evidence as history, not as proof for the new revision.

Prototype and splitting are conditional. Record prototype approval against the reviewed
artifact/revision; a generated preview is not approval. After splitting, the parent
links all phases and their dependencies; each phase links its parent, inputs and active
plan. Implementation follows the selected phase, not a superseded parent plan. Completing
one phase does not complete the whole feature. A no-split decision fits in the plan.

Distinguish implementation, review, CI, merge and deployment evidence. Mark only observed
results complete. Preserve required acceptance coverage, human decisions, dirty-worktree
boundaries and authorization for external writes. Reuse authorization already granted
for the same scope; task status is not new authorization. In parallel work, one owner
updates shared task/review records from worker results.
