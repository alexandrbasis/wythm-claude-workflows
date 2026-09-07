# Аудит pipeline-навыков discovery/planning

> Аудит исходной версии `32cfafa`. Это находки и варианты решений, а не перечень применённых изменений. Фактический объём адаптации и проверки приведены в `../REVIEW.md`.

## Объём и покрытие

- Источник: `/Users/alexandrbasis/Desktop/Coding/claudops-astra-plugin-20260906`, `HEAD 32cfafa`, clean checkout.
- Граница источника: только канонические `.claude/skills/**/SKILL.md`; старый July-checkout и `.agents/skills` исключены.
- Прочитано полностью: **14/14 entrypoints** — `nf`, `blueprint`, `brainstorm`, `product`, `grill-me`, `design-exploration`, `ct`, `rip`, `analyze`, `vp`, `deep-research`, `improve-codebase-architecture`, `ubiquitous-language`, `zoom-out`.
- Для зависимых выводов также прочитаны: `.claude/docs/templates/{discovery,brainstorm,JTBD,PRD,technical-decomposition,splitting-decision,cross-ai,plan-review}-template.md`, `.claude/skills/ct/references/decomposition-guide.md`, `.claude/skills/nf/references/interview-guide.md`.
- Внешний research не выполнялся; выводы ниже основаны на этих файлах.

## Вердикт по каждому entrypoint

`keep` означает сохранить как отдельный этап, но не обязательно без изменений; `simplify` — оставить роль, сократив обязательную процедуру; `merge` — поглотить роль общим контекстом/соседним этапом; `move-out` — оставить как явно вызываемый вспомогательный workflow вне обязательного feature pipeline.

| Skill | Вердикт | Входы | Текущие выходы | Решение и сохраняемый контракт |
|---|---|---|---|---|
| `/nf` | **simplify** | feature prompt; `.claude/docs/templates/discovery-template.md`; `product-docs/PRD/*`, `product-docs/JTBD/*`, `product-docs/UBIQUITOUS_LANGUAGE.md`; кодовая база; `nf/references/interview-guide.md` | `tasks/task-YYYY-MM-DD-[feature-name]/discovery-[feature-name].md`; validation append; handoff `/vp` или `/ct` | Оставить основным discovery-этапом. Убрать повторное сканирование/обязательную cross-AI цепочку из core; писать в уже resolved task context, создавать минимальный `TASK.md` только при отсутствии записи. Инвариант: standalone discovery с явными `in/out`, flow, requirements и unresolved markers. |
| `/blueprint` | **merge** | one-line objective; PRD/JTBD/task docs; кодовые области; риски/паттерны | `docs/superpowers/plans/YYYY-MM-DD-<feature-slug>.md` | Слить с `/ct` как режим multi-session/split для больших задач; DAG и cold-start brief оставить только при реальной межсессионной работе. Канонический план — внутри resolved task context (`blueprint.md` или секция `TASK.md` + tech decomposition), чтобы не создавать второй корень артефактов. |
| `/brainstorm` | **move-out** | topic; optional existing `docs/brainstorming/brainstorm-*`; при проектном topic — `CLAUDE.md` и нужный код | `docs/brainstorming/brainstorm-YYYY-MM-DD-[topic-slug].md` (optional для Quick) | Оставить general decision aid вне обязательного feature pipeline. Для feature-context привязывать заметки к resolved task; не запускать отдельную resume/calibration ветку, если пользователь уже дал решение. Инвариант: brainstorm никогда не маскируется под discovery/PRD/plan. |
| `/product` | **simplify** | `JTBD-template` или `PRD-template`; existing JTBD; `product-docs/UBIQUITOUS_LANGUAGE.md`; product evidence; optional code context/research | `product-docs/JTBD/JTBD-[feature-name].md` и/или `product-docs/PRD/PRD-[feature-name].md`; optional companion JTBD; validation append | Сохранить как optional long-lived product framing. Сделать research, grill и cross-AI условными по claims/риску; не повторять полный `/nf` interview. Инвариант: PRD/JTBD остаётся repo-level source of truth, а технический task только ссылается на него. |
| `/grill-me` | **simplify** | discovery/plan/design artifact; code/docs when answer is resolvable there | inline compact summary: clarifications, scope cuts, assumptions, wording, risks | Сохранить как общий read-only ambiguity pass, bounded by stop condition; вызывать только при material ambiguity. Caller при необходимости пишет summary в task evidence. Инвариант: grill не расширяет scope и не мутирует artifact без явного разрешения. |
| `/design-exploration` | **merge** | feature + constraints + caller goal; codebase; optional checklist | inline findings: patterns, fit, integrations, constraints, prior art, approaches, questions, risks | Слить в общий context scan, который один раз потребляют `/nf`, `/product`, `/ct`; оставить standalone routing alias только для явного запроса. Инвариант: рекомендации опираются на прочитанный код и не являются tech decomposition. |
| `/ct` | **keep + simplify** | resolved task context; discovery/product/prototype links; repo conventions/code; architecture glossary; technical-decomposition template/guide | `tasks/task-YYYY-MM-DD-[feature-name]/tech-decomposition-[feature-name].md`; optional `splitting-decision.md`; optional phase docs | Оставить центральным planning/splitting этапом. Свести семь gates к input resolution → context/ambiguity → plan → proportionate review → optional split; task-splitter/decomposer и cross-AI сделать capability-gated. Инвариант: test plan, must-haves, requirements traceability, concrete steps, risks and implementation handoff remain. |
| `/rip` | **move-out** | plan path/directory; related code; PRD/business requirements | inline plan walkthrough; optional `plan-review.md` template | Вынести из core: его business-value walkthrough пересекается с `/ct` review и `plan-reviewer`. Оставить для явного human walkthrough, не требовать перед каждым implementation handoff. Инвариант: read-only, facts + questions, every material mismatch surfaced. |
| `/analyze` | **merge** | resolved task dir; discovery/JTBD/PRD; tech decomposition; test cases/steps | inline traceability matrix/verdict | Объединить с `/ct` как один deterministic traceability check после tech decomposition; сохранить отдельный explicit command как thin alias. Инвариант: `REQ → TEST → Step`, findings before verdict, no writes. |
| `/vp` | **keep + simplify** | resolved task; discovery or quick prototype answers; UI/backend template + tips; project visual context | `tasks/task-YYYY-MM-DD-[feature-name]/playground-[feature-name].html`; `vp-approval.md` | Сохранить строго optional visual validation; запускать только если visual uncertainty/approval matters. Оставить explicit Approve/Changes/Reject и sidecar; `playground`/browser path capability-gated with a portable static fallback. Инвариант: opened playground is never treated as approval until sidecar decision exists. |
| `/deep-research` | **move-out** | explicit external/current/niche question; optional local manifest/code/context | inline Quick/Comparison/Full report; no canonical file path | Вынести из default feature path; invoke only when an external claim changes scope/decision. If findings affect a task, persist a compact `research.md` under resolved task and link it. Инвариант: cited/current sources, confidence, caveats, open questions; no research theater. |
| `/improve-codebase-architecture` | **move-out** | target code area; relevant glossary/PRD/JTBD/task docs; codebase | inline candidate list and optional deepened-module design | Оставить отдельным architecture-refactoring workflow, не включать в every-feature pipeline. Handoff actionable candidate to `/ct`; durable rejection/decision only when explicitly authorized. Инвариант: read-only exploration, deletion test, no unrelated tech-debt expansion. |
| `/ubiquitous-language` | **simplify** | existing glossary; conversation; active PRD/JTBD/discovery; source code only for ambiguity | `product-docs/UBIQUITOUS_LANGUAGE.md` on explicit/authorized update; inline terms summary | Сохранить как shared vocabulary utility. Step-0 calls from `/nf`, `/product`, `/ct` must remain load-only; post-grill write only under explicit/propagated authorization. Инвариант: merge preserves existing terms and canonical wording is reused downstream. |
| `/zoom-out` | **move-out** | current file/area; callers/dependencies; optional glossary | inline compact module/caller/dependency map; no file | Оставить explicit diagnostic helper вне pipeline. Не создавать artifact и не запускать автоматически; use when local context is genuinely lost. Инвариант: map only, no redesign or implementation plan. |

## Приоритетные находки

### 1. Доказанный конфликт: `/product` и `/analyze` используют разные корни product docs

Источники:

- `.claude/skills/product/SKILL.md:219-220`: `JTBD output: product-docs/JTBD/...` и `PRD output: product-docs/PRD/...`.
- `.claude/skills/analyze/SKILL.md:36-43`: spec lookup требует `PRD-*.md in docs/product-docs/PRD/` и `JTBD-*.md in docs/product-docs/JTBD/`.
- `product-docs/README.md:3,24-26`: product docs живут в repo-root `product-docs/`, отдельно от `.claude/`.

Сценарий отказа: после `/product` `/analyze` не находит PRD/JTBD и выдаёт `SKIPPED`, хотя входной artifact существует.

Замена: один repo-relative resolver для product docs; legacy root `product-docs/{PRD,JTBD}` считать каноническим, а старые/проектные варианты принимать только через scoped linked path. Инвариант: любой следующий этап видит документ, который записал предыдущий, без перемещения или дублирования.

### 2. Доказанный конфликт: нет единого task context и единого правила reuse/create

Источники:

- `.claude/skills/nf/SKILL.md:68-71`: всегда `Create tasks/task-YYYY-MM-DD-[feature-name]/` и пишет discovery.
- `.claude/skills/vp/SKILL.md:36-47`: ищет только `tasks/task-YYYY-MM-DD-*[argument]*/`, а при отсутствии discovery предлагает новый режим.
- `.claude/skills/ct/SKILL.md:50-67`: глобально ищет похожие docs и только потом создаёт fallback task path.
- `.claude/skills/blueprint/SKILL.md:115-117` и `.claude/skills/brainstorm/SKILL.md:131-133`: создают artifacts в `docs/superpowers/plans/` и `docs/brainstorming/`, вне task dir.

Сценарий отказа: существующая задача с legacy naming, linked plan или brainstorm не распознаётся; `/nf` или `/vp` создаёт второй task dir, а `/ct` строит план без полного контекста.

Замена: shared `task-context.md` reference, применяемый всеми pipeline skills: `explicit path → current linked task → repo convention scoped matching → ask only on true ambiguity → create minimum tasks/task-YYYY-MM-DD-slug/TASK.md if absent`. `TASK.md` — индекс/состояние, legacy docs переиспользуются и не переписываются.

Инвариант: один resolved task context на feature; stage writes only needed artifacts and always records links, current state, evidence, and one next action.

### 3. Доказанный конфликт: `/analyze` заявлен как автоматический GATE 4, но `/ct` его не запускает

Источники:

- `.claude/skills/analyze/SKILL.md:4-8`: `Also invoked automatically as GATE 4 in /ct`.
- `.claude/skills/ct/SKILL.md:115-130`: GATE 4 — запись decomposition; exit — fresh developer can implement.
- `.claude/skills/ct/SKILL.md:154-157`: `/analyze` указан как `Optional adjunct`.

Сценарий отказа: агент либо ждёт несуществующий обязательный traceability pass, либо выполняет его дважды/не выполняет вовсе; пользователь не знает, когда verdict является частью `/ct`.

Замена: merge `/analyze` в один компактный post-plan check внутри `/ct` либо удалить автоматическое обещание и оставить explicit alias. Не оставлять одновременно «automatic GATE 4» и «optional adjunct».

Инвариант: ровно один воспроизводимый `REQ → TEST → Step` matrix после существования decomposition; matrix и verdict read-only.

### 4. Доказанный overlap: один и тот же context/research/grill цикл повторён в нескольких этапах

Источники:

- `.claude/skills/nf/SKILL.md:47-63`: design exploration → optional research → deep-dive questions → grill → glossary update.
- `.claude/skills/product/SKILL.md:62-102` и `175-202`: design exploration → research → interview → grill → glossary update.
- `.claude/skills/ct/SKILL.md:69-99`: requirements quality + 2–3 Explore workers with the same architecture/change-surface/risk mandates.
- `.claude/skills/design-exploration/SKILL.md:33-48`: its own parallel context scan and the same fit/options/constraints/risk output.

Сценарий отказа: feature проходится через `/nf` и `/product`, затем `/ct` заново читает и исследует те же материалы; обязательные checkpoints и subagents делают простой change длиннее, а stale summaries расходятся.

Замена: общий reusable procedure в `task-context.md`: один evidence-backed context scan; далее только missing decision branch; grill, research, prototype — optional escalations. Соседние навыки принимают ссылку на уже записанное evidence, а не повторяют scan.

Инвариант: каждый stage обязан добавить новую проверяемую информацию или артефакт; повторный scan разрешён только при изменившемся входе/риске.

### 5. Риск/гипотеза с доказанной capability-зависимостью: optional tools описаны как обязательная последовательность

Источники:

- `.claude/skills/nf/SKILL.md:74-80` и `.claude/skills/product/SKILL.md:225-245`: сначала последовательно инициализируются три CLI, затем reviews parallel; skip только при отсутствии CLI/opt-out.
- `.claude/skills/ct/SKILL.md:160-170`: стандартный completion path требует `task-splitter` и `task-decomposer` при split.
- `.claude/skills/design-exploration/SKILL.md:33-39`: fan-out зависит от Explore workers.
- `README.md:176-180`: portable clients must supply capabilities selected workflow needs.

Сценарий отказа (гипотеза о runtime): portable client без `Task`/`Agent`, Exa или CLI не может пройти declared core path, хотя research/prototype/split были optional по смыслу; разные skills дают разные fallbacks.

Замена: capability matrix в общем task context: core = read/write/search/ask; optional capability absence записывается как `SKIPPED — reason`, не блокирует минимальный artifact и next action. Cross-AI, parallel workers, browser/playground и split agents запускаются только при наличии capability и material need.

Инвариант: отсутствие optional tool никогда не приводит к выдуманным evidence/approval и не уничтожает canonical task record; задача заканчивается валидным статусом и понятным следующим действием.

## Итоговая форма упрощённого pipeline

1. **Resolve**: определить feature/task context; reuse existing docs; создать минимум `TASK.md` только если task entrypoint отсутствует.
2. **Describe**: `/nf` (или `/product` для отдельного JTBD/PRD) записывает source-of-truth artifact и unresolved markers.
3. **Question/grill**: один bounded ambiguity pass по необходимости; summary/evidence привязан к task.
4. **Prototype**: `/vp` только при визуальной неопределённости или явном запросе; sidecar фиксирует decision.
5. **Plan/split**: `/ct` пишет technical decomposition; traceability и split evaluation proportionate to risk.
6. **Implement**: `/si` получает resolved task path и следующий action из `TASK.md`.

Сохраняемые invariants: repo-relative paths, reuse-before-create, explicit user approval for prototype/scope changes, read-only review tools, no fabricated evidence, and a durable link/state/evidence/next-action record per task.
