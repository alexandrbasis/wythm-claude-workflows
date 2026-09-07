# Аудит delivery-pipeline skills

> Аудит исходной версии `32cfafa`. Это находки и варианты решений, а не перечень применённых изменений. Фактический объём адаптации и проверки приведены в `../REVIEW.md`.

## Область и покрытие

- Источник: `/Users/alexandrbasis/Desktop/Coding/claudops-astra-plugin-20260906`, commit `32cfafa`, ветка `codex/skills-astra-plugin`; рабочее дерево на момент аудита чистое.
- Прочитаны полностью 12/12 канонических entrypoint-файлов: `si`, `si-quick`, `sr`, `prc`, `finisher`, `parallelization`, `ph`, `tdd`, `dbg`, `fci`, `qa`, `triage-issue`.
- Выборочно прочитаны связанные reference/agent-файлы, когда они участвуют в контракте: `si/references/{verification-gate,implementation-checklists}.md`, `sr/references/review-passes.md`, `technical-decomposition-template.md`, `developer-agent.md`, `automated-quality-gate.md`, `task-decomposer.md`, `spec-compliance-reviewer.md`.
- Аудит read-only; checkout не менялся.

## Вердикт по каждому entrypoint

| Skill | Вердикт | Фактический вход | Фактический выход | Причина |
|---|---|---|---|---|
| `si` | **simplify / keep** | `tasks/.../tech-decomposition-*.md` или прямой путь; требования, тест-план, implementation steps | Изменения кода/тестов; тот же task doc (`status`, checkboxes, `Tracking`, `Deviations & Decisions`, `Completion Summary`); branch/commit/PR | Оставить главным implementation-stage, но убрать локальную оркестрацию resolver, VC, receipts и повторные gates в общий task-контракт. Сохраняет TDD и evidence gate. |
| `si-quick` (`quick`) | **merge into `si`** | Пользовательский запрос + repo/package scripts; только задача с ясным scope, `<5` файлов и без task doc | Изменённые файлы/тесты; один commit после разрешения; task doc обычно отсутствует | Это второй implementation pipeline с собственной scope/TDD/verify/commit логикой и явным запретом создавать task doc. Оставить как `si` mode `quick`, который всё равно создаёт/находит минимальный record. |
| `sr` | **simplify / keep** | Task path, PR URL/number, branch, range или auto-detect working tree | Ровно один review artifact: task dir `code-review-[feature].md` либо `.claude/reviews/code-review-...md`; findings/verdict/verification | Специализация review полезна. Вынести target resolution, task linkage и review receipt в общий контракт; сохранить immutable-snapshot и no-spec/no-approval safeguards. |
| `prc` | **simplify / keep** | PR number или текущая branch → open PR; reviews, inline/general comments | Изменения по одобренным пунктам; commit; push при отдельной авторизации; drafts/replies, отправка только при явном разрешении | Оставить feedback-resolution stage, но хранить comment inventory, decision и verification в текущем task record; не дублировать authorization semantics. |
| `finisher` | **simplify / keep** | Open PR/branch; optional task/phase directory | Commit/push; green CI read-back; merge; local branch cleanup; optional phase handoff updates | Ship gate нужен, но task resolution сейчас best-effort/silent. Использовать общий resolver и финальный receipt; merge остаётся отдельной hard-to-reverse authorization boundary. |
| `parallelization` | **move-out** | Existing readable task doc + independent work items + git state | Isolated worktrees, patches/merges, consolidated task-doc update, validation summary | Это execution strategy, а не отдельный пользовательский pipeline. Встроить policy в `si`/общий delegation contract; оставить только компактную reference-секцию с isolation/conflict/approval invariants. |
| `ph` | **simplify / keep** | Existing task directory + tech decomposition; optional existing `HANDOFF.md` | `tasks/task-[name]/HANDOFF.md` и note в task doc | Handoff полезен как session utility, но не должен быть недоступен без старого schema-shaped task. Резолвить общий task record, писать туда handoff receipt; legacy `HANDOFF.md` сохранять. |
| `tdd` | **move-out** | Approved task/decomposition или пользовательский plan when no approved artifact | Test/code/refactor behavior; durable output задаёт вызывающий stage | Это invariant/reference layer, не pipeline stage. Сократить до канонической RED→GREEN→REFACTOR policy в общем контракте; не требовать отдельного user-facing invocation. |
| `dbg` | **simplify / keep** | Bug description/error + runtime reproduction; project root | Transient `.debug/debug.log`, instrumentation, post-fix evidence; optional `tasks/.../bug-report-*.md` for non-trivial bugs | Runtime evidence stage сохраняется. Его debug log и optional bug report должны быть привязаны к общему task record; trivial bug не должен терять durable decision/evidence. |
| `fci` | **merge into `si` recovery mode** | Workflow/run id + CI logs + resolved package scripts/cwds | Code/test changes; local CI-equivalent checks; remote CI status; no task record currently | CI repair — implementation recovery path, а не отдельный durable pipeline. Оставить отдельный trigger/section, но наследовать `si` task receipt и resolved commands; не повторять full verification policy. |
| `qa` | **merge with `triage-issue` as `issue-intake(batch)`** | Interactive multiple user-reported bugs + one resolved Linear/GitHub destination | Multiple tracker issue URLs with blocker relations; no local task artifact | Batch mode полезен, но issue intake and authorization should share one contract. Each issue gets a minimal task record or linked existing task before tracker write. |
| `triage-issue` | **merge with `qa` as `issue-intake(single)`** | One reported bug + code exploration + resolved tracker/repo/team | One tracker issue URL/body-only; root cause, behavior-level TDD plan, acceptance criteria, handoff | Single mode is distinct UX, not distinct persistence model. Preserve no-fix/TDD-plan boundary and body-only path; use same task record and authorization receipt as `qa`. |

## Приоритетные находки

### P0 — отсутствует единый task identity/resolution contract

- Evidence: `.claude/skills/si/SKILL.md:42-48` — “Confirm task exists ... If the document is missing core structure, stop”; `.claude/skills/si-quick/SKILL.md:30-45` — “not already tracked by a task doc” and “If ... task directory already exists, use `/si` instead”.
- Affected request: portable common task-folder contract and requirement that every stage resolves an existing task or creates the minimum durable human-agent record.
- Consequence: the two implementation entrypoints cannot share a task identity; quick work has no durable requirements/evidence/next action, while formal work hard-stops on a missing legacy schema. Downstream `sr`, `ph`, `finisher`, `dbg`, `fci` cannot reliably attach their receipts.
- Replacement: one resolver in `setup/references/task-context.md`: explicit path → linked active task → scoped repo-convention match → `tasks/task-YYYY-MM-DD-slug/TASK.md` fallback. Reuse legacy docs/paths; accept a compact single-file task and fill missing structural fields from observed evidence.
- Preserved invariant: requirements remain traceable; ambiguity stops or asks; no stage silently creates a second task.

### P0 — stage outputs are split across incompatible stores

- Evidence: `.claude/skills/finisher/SKILL.md:65-81` — task resolution is “best-effort and silent” and no task means Gate 3 skips; `.claude/skills/ph/SKILL.md:96-99` — writes only `tasks/task-[name]/HANDOFF.md`; `.claude/skills/qa/SKILL.md:146-150` — outputs are tracker URLs, while `/dbg` writes `.debug/debug.log` and `/sr` writes a review file.
- Affected request: every stage must persist human-agent state and make stage outputs discoverable by the next stage.
- Consequence: a successful review, CI fix, handoff, debug run, or issue intake can exist without a resolvable task record; “done” is stored in mutually unrelated artifacts and cannot be resumed or independently read back.
- Replacement: every stage writes one receipt to the resolved task record with `stage`, `status`, `requirements`, `evidence`, `outputs` (path/URL), `authorization`, `blockers`, and exactly one `next_action`. Keep specialized artifacts (`HANDOFF.md`, review file, debug log, issue URL) and link them; do not replace or rename legacy paths.
- Preserved invariant: specialized evidence remains intact, while the task record becomes the index and handoff surface.

### P1 — verification is duplicated as multiple mandatory ledgers

- Evidence: `.claude/skills/si/SKILL.md:52-69` requires a counted VC ledger and per-step/final checks; `.claude/skills/si/SKILL.md:128-163` separately requires checkbox/test-plan updates plus four self-verification checks; `.claude/skills/si/SKILL.md:188-194` requires a final Completion Summary. The referenced `verification-gate.md` adds another per-type recipe and checked-vs-total gate.
- Affected request: critical simplification while preserving requirements and evidence.
- Consequence: one implementation stage must keep several overlapping representations of “done”; they can drift (VC checked, step test recorded, self-verification run, summary refreshed) and consume attention without adding independent evidence.
- Replacement: keep one `requirements` checklist and one append-only `evidence` receipt per stage. A final summary is a projection of receipts, not a second checklist. Preserve exact VC recipes only for brittle/countable requirements.
- Preserved invariant: no completion/review handoff without all requirements covered by concrete evidence; exact-count and visual safeguards remain where triggered.

### P1 — delegation policy is duplicated and too granular

- Evidence: `.claude/skills/si/SKILL.md:85-100` delegates parallel work to another skill; `.claude/skills/parallelization/SKILL.md:62-115` repeats wave detection, batching, worker prompt, isolation, and return obligations; `developer-agent.md` repeats task-doc-first, TDD, scope, validation, and structured JSON requirements. `/sr` adds a separate all-reviewers batch protocol.
- Affected request: simplify every pipeline skill and remove unnecessary delegation layers.
- Consequence: the same scope, TDD, task-doc, isolation, and return rules have multiple owners; edits can fix one layer while another still requires the old protocol. More workers/receipts are mandated than the acceptance criteria require. Actual runtime cost and failure frequency are **untested**; the static duplication is proven.
- Replacement: one delegation envelope in the common contract: `work_item`, `task_path`, `allowed_scope`, `input_artifacts`, `authorization`, `expected_outputs`, `validation`, `return_receipt`. `si` chooses sequential/parallel; the internal strategy only supplies isolation and merge rules. Review agents use the same receipt shape.
- Preserved invariant: worker isolation, no cross-item edits, scoped authorization, validation before consolidation, and explicit conflict handling.

### P1 — path/schema and authorization semantics are not portable

- Evidence: `.claude/skills/si-quick/SKILL.md:129-131` requires missing `.claude/docs/references/deviation-rules.md` (confirmed absent at `32cfafa`); `.claude/skills/fci/SKILL.md:53-55` and `95-103` still expose unresolved command placeholders; `.claude/skills/finisher/SKILL.md:241-243` has its own push authorization rule, while `.claude/skills/qa/SKILL.md:19-22` infers tracker-write authorization and `.claude/skills/prc/SKILL.md:123-124` separates code-fix authorization from external replies.
- Affected request: preserve authorization and make artifacts portable across stages/repositories.
- Consequence: invocations can fail on a missing reference or silently diverge on whether prior authorization covers commit, push, merge, tracker write, or external reply. Placeholder examples are explicitly guarded against in text, but no shared resolved command/path schema exists.
- Replacement: the common task record stores `repo_root`, `task_path`, `legacy_paths`, `verify_commands` with working directories, and an operation-scoped `authorization` receipt (`operation`, `destination`, `scope`, `source`, `timestamp`, `expiry/consumed`). Each stage resolves once, persists the receipt, and stops at a new boundary.
- Preserved invariant: no push/merge/tracker write/external reply without matching explicit authorization; no unresolved command is executed; legacy paths remain readable.

## Common contract proposal for the next edit

Use `setup/references/task-context.md` as the single portable reference, linked from every pipeline entrypoint. It should define only the resolver and receipt semantics; specialized skills keep their domain behavior.

1. **Resolve**: explicit path → linked active task → scoped repo-convention match → create `tasks/task-YYYY-MM-DD-slug/TASK.md` minimum fallback. If several candidates match, stop and ask; do not guess.
2. **Reuse**: preserve legacy task/decomposition/handoff/review/bug-report paths and schemas. No forced renames. A compact task may be one file with sections.
3. **Minimum durable record**: `identity`, `request`, `requirements`, `decisions`, `evidence`, `authorization`, `outputs`, `blockers`, `next_action`, `status`. Existing schemas are accepted semantically; missing structural fields are filled from evidence only when they are actually known.
4. **Stage receipt**: each stage appends one receipt with `stage`, `status`, `inputs`, `outputs`, `evidence`, `authorization`, and `next_action`. Utility stages reference the current task instead of inventing a new artifact index.
5. **Boundaries**: substantive blockers stop the stage; uncertainty is recorded as `unknown`/`untested`; a new external destination or destructive operation requires fresh authorization. A stronger model does not remove these guards.

## Proven conflicts vs untested hypotheses

### Proven from source/static checks

- `/si` requires a pre-existing structured decomposition while `/si-quick` explicitly excludes tracked task work; no shared resolver or fallback record is defined.
- `/finisher` may silently run without a task, while `/ph` requires one and `/sr` permits review without one.
- Stage outputs are heterogeneous and not linked by a common task index.
- `/si` has VC, per-step, self-verification, and completion-summary representations of completion.
- `.claude/docs/references/deviation-rules.md` is referenced but absent in this checkout.
- Authorization rules vary by operation and skill; no persisted, operation-scoped authorization schema exists.

### Untested hypotheses (do not present as observed failures)

- Actual token/latency cost or user friction from duplicated gates and delegation was not measured.
- Real invocation behavior when multiple tasks match repo conventions was not exercised.
- Whether a specific runner would execute an unresolved placeholder is not claimed; the text now says to resolve placeholders first, but the common resolved-command contract is missing.
- Tracker/PR side effects were not executed; conclusions about missing local records are based on declared outputs, not live writes.

## Coverage

**12/12 canonical skills covered; 12/12 entrypoint files read in full.** No implementation or workflow execution performed.
