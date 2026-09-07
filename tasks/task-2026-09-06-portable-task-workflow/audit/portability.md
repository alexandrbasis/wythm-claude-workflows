# Аудит portability канонических skills

> Аудит исходной версии `32cfafa`. Это находки и варианты решений, а не перечень применённых изменений. Фактический объём адаптации и проверки приведены в `../REVIEW.md`.

Источник аудита: `/Users/alexandrbasis/Desktop/Coding/claudops-astra-plugin-20260906`

Commit: `32cfafa`

Статус checkout на момент чтения: clean

Область: 14 канонических `.claude/skills/*/SKILL.md`, перечисленных в задании. Прочитано: 14/14 entrypoints, 2 074 строки. Связанные support-файлы прочитаны только там, где они определяют путь, placeholder, provider или artifact contract. Рецепты не запускались; runtime/model claims не подтверждались.

## Единый контракт task-folder

Для task-attached запуска скилл должен разрешать контекст в одном порядке: явный task path → текущий task/branch context → совпадающая scoped-конвенция репозитория → минимальный `TASK.md` fallback. Существующие legacy paths (`tasks/task-.../tech-decomposition-*.md`, `HANDOFF.md`, `docs/learning/*`) сохраняются и подхватываются resolver-ом; новый скилл для этого не нужен.

Если task найден, findings, receipts, решения и промежуточные результаты должны сохраняться в его папке или в её существующем task-документе, чтобы следующий сеанс мог продолжить работу. Если task не найден и действие само по себе полезно (server utility, standalone teaching, read-only analysis, provider query), скилл возвращает результат и не создаёт фиктивный product task. `/tmp` допустим только как transient transport/cache; task-attached результат должен иметь durable sidecar или ссылку в task-документе.

## Verdict по 14 скиллам

| Скилл | Verdict | Причина и адаптация | Task artifact contract |
|---|---|---|---|
| `setup` | **simplify** | Сейчас это одновременно project-context setup и массовый materializer workflow. Для plugin-режима должен быть лёгким: читать target, собирать подтверждённый project context и менять только target-owned `.claude`; полное копирование workflow — отдельный явно выбранный режим. | При task-attached setup сохраняет подтверждённые значения, unresolved values и bootstrap receipt в task folder/существующий task doc. Standalone setup не создаёт task; plugin остаётся source of truth, пока target override явно не выбран. |
| `update-setup` | **keep** | Граница plugin cache vs target и `--local-root` уже оформлены хорошо. Сократить повторяющиеся command recipes и оставить один canonical invocation/reference; не смешивать copied-workflow adoption с host plugin upgrade. | При наличии task сохраняет scan/selection/verify receipt и конфликтное решение рядом с task. Check-only или standalone update не создаёт фиктивный task. |
| `coding-conventions` | **simplify** | Полезен как internal reference, но project-specific placeholders и пути не должны быть runtime-источником истины plugin-а. Оставить общие invariants, project values получать через shared task/project context. | Только потребляет task doc как source of truth для реализации; сам ничего не пишет и task artifact не создаёт. |
| `review-conventions` | **simplify** | Generic review contract хорош, но `{{DOCS_DIR}}`, `{{TEST_DIR}}` и жёсткий `tasks/...` путь делают reference зависимым от setup и конкретной схемы репозитория. | Task-attached review сохраняет findings/summary в task doc или review sidecar. Standalone review возвращает report без создания task. |
| `architecture-language` | **keep** | Короткий, условный glossary pointer, без provider/path assumptions. | Обычно artifact не создаёт; при task-attached architecture decision обновляет task decision section/sidecar. Standalone vocabulary use не маскируется под task. |
| `cc-linear` | **move-out** | Provider-specific integration с `.claude/scripts/linear-api.sh`, default `TEAM`, фиксированными state names и именем assignee. Это опциональный tracker adapter, а не portable core. | Только при явном task-attached tracker operation сохраняет issue ID, URL, mutation receipt и read-back в task. Standalone Linear query/mutation не создаёт product task. |
| `code-analysis` | **simplify** | После улучшения entrypoint всё ещё содержит длинные TS/JS command examples и раскрытый `project-checks.md` с unresolved placeholders; сделать stack-neutral core и выбирать resolved reference checks после discovery. | Для task scope сохраняет analysis report и evidence paths в task folder. Для общего overview — ответ без task artifact. |
| `codex-cli` | **merge** | Большая часть one-shot/output-capture/no-context протокола дублируется с `cursor-cli` и `antigravity-cli`; provider-specific flags должны быть маленьким adapter layer. | При task path сохраняет provider result, prompt scope, exit/verification receipt в task evidence sidecar; без task — transient output/response, без fake task. |
| `cursor-cli` | **merge** | Тот же общий cross-AI lifecycle, отдельные Cursor flags и read-only mode. Слить protocol с другими CLI, оставить adapter reference для `agent`. | Тот же contract: durable result только при существующем task, иначе standalone response. |
| `antigravity-cli` | **merge** | Тот же lifecycle, но `agy`-specific print mode, `@path`, timeout и model persistence. Отдельный provider adapter нужен, отдельная большая workflow-копия — нет. | Task-attached result/authority boundary в task evidence; standalone web/review call не создаёт task. |
| `dev-server` | **simplify** | Полезный universal detector, но таблица и error regex разрослись, а `Monitor`, `TaskStop` и optional `browser-use` зависят от host capabilities. Capability check и один host-neutral session contract снизят ложные обещания. | Если server запущен для task, сохранить command/port/PID-or-monitor id, HTTP/UI probe и errors в task sidecar. Standalone server живёт в session monitor и не создаёт task. |
| `git-guardrails` | **move-out** | Это optional host hook manager с намеренно disabled state, `.claude/settings.json` и `$CLAUDE_PROJECT_DIR`; его следует держать в optional safety bundle, не выдавая за активную portable protection. | Artifact только для явно task-attached guard change: settings read-back и smoke-test receipt. Обычная проверка статуса не создаёт task. |
| `sbs` | **simplify** | 243 строки протокола обучения дублируют общие AskUserQuestion/Todo правила и используют отдельный `docs/learning` resume path. Оставить teaching-specific calibration, но task context и resumability направить через shared resolver. | Task-attached обучение пишет resume/notes в task folder или связывает legacy `docs/learning` note с task. General teaching сохраняет notes только после явного согласия и не создаёт product task. |
| `update-docs` (`udoc`) | **simplify** | Хорошо требует task path и раздельную commit/push authorization, но жёстко требует `tech-decomposition-*.md`, `docs/changelogs/YYYY-MM-DD` и конкретные subagent names. Пути и changelog policy должны резолвиться из task/repo context. | Обязателен существующий task context; docs/changelog receipt и список изменённых файлов привязываются к нему. При отсутствии task — запросить путь/остановиться, не создавать task автоматически. |

## Приоритетные находки

### P0 — `setup` всё ещё массово материализует plugin в target

**Класс:** доказанный portability-конфликт.

**Источник:** `.claude/skills/setup/SKILL.md:21-44` — “A plugin is a read-only template source; project configuration belongs in the target repository's `.claude/` directory”, затем “An authorized first setup includes copying these missing workflow templates”. Реализация `.claude/skills/setup/scripts/bootstrap_project.py:13-25,64-73` задаёт `COMPONENTS = {"skills", "agents", "docs", "scripts", "hooks"}` и обходит `source.rglob("*")`, копируя каждую отсутствующую запись в target `.claude/`.

**Сценарий:** пользователь устанавливает plugin в новый репозиторий и просит настроить project context; setup материализует весь bundled workflow.

**Последствие:** target получает большой копированный snapshot, plugin и target расходятся по source of truth, а последующие plugin upgrades перестают быть единственным способом обновления. Это прямо расходится с требованием plugin-authoritative operation и создаёт лишний diff в любом repo.

**Замена:** сделать project-context setup лёгким и default: resolver читает target, предлагает подтверждённые значения и пишет только target-owned context. Полное bootstrap всех компонентов оставить отдельным явным выбором с preview. Не трогать settings, secrets и runtime state; сохранить no-overwrite и отдельное approval для hook activation.

**Сохраняемый invariant:** plugin не мутируется; target path явен; существующие файлы не перезаписываются; hook side effects не активируются копированием.

### P1 — нет общего durable task contract

**Класс:** доказанная структурная фрагментация; последствия для отдельных host/repo — условная часть.

**Источники:** `.claude/skills/review-conventions/SKILL.md:82-86` — `tasks/<task-dir>/tech-decomposition*.md`; `.claude/skills/update-docs/SKILL.md:26-33` требует именно `tech-decomposition-*.md`; `.claude/skills/sbs/SKILL.md:40-44,190-204` использует `docs/learning/sbs-*`; CLI skills пишут результаты в `/tmp` (например `.claude/skills/codex-cli/SKILL.md:80-87`).

**Сценарий:** один task проходит analysis → cross-AI review → teaching или docs update, затем context compaction.

**Последствие:** evidence и resume state оказываются в разных ephemeral/legacy местах; следующий сеанс не знает, какой artifact authoritative. Отдельные skills могут требовать task, а utilities рядом с ними создавать только `/tmp` output.

**Замена:** использовать один shared task-context resolver (explicit path → current task → scoped repo convention → minimal `TASK.md` fallback), сохранять task-attached outputs в task folder/sidecars, а legacy paths только подхватывать. Standalone utility возвращает результат без создания fake product task.

**Сохраняемый invariant:** выбор task остаётся явным; несоответствие/отсутствие task не маскируется созданием фиктивного документа; durable handoff доступен следующему сеансу.

### P1 — три CLI skills дублируют один lifecycle и расходятся по provider contract

**Класс:** доказанное дублирование; drift и устаревание конкретного provider — гипотеза до runtime/official verification.

**Источники:** `.claude/skills/codex-cli/SKILL.md:80-87` — prompt → `/tmp/codex-result.md` → Read; `.claude/skills/cursor-cli/SKILL.md:66-74` — тот же lifecycle с `agent` и `/tmp/cursor-result.txt`; `.claude/skills/antigravity-cli/SKILL.md:53-63` — тот же lifecycle с `agy` и `/tmp/agy-result.txt`. У всех повторяется “no context from this conversation”, one-shot и background guidance.

**Сценарий:** cross-AI validation запускается для одной задачи через два или три provider-а.

**Последствие:** около сотен строк lifecycle-инструкций поддерживаются в трёх местах; authority boundary, task path и output retention могут разойтись. `/tmp`-only result теряется после session boundary.

**Замена:** один `cross-ai` protocol/reference: explicit invocation, prompt/path resolution, read-only/evidence boundary, task receipt and no-write semantics. Provider adapters содержат только binary check, flags, output extraction, timeout and model policy. Model freshness считать гипотезой, пока локальный binary или официальная проверка её не подтверждает.

**Сохраняемый invariant:** ни один external CLI не запускается неявно; one-shot result — evidence, не authorization; write/publication остаются у caller.

### P1 — `cc-linear` зашивает tracker defaults и mutation vocabulary

**Класс:** доказанный provider coupling; wrong-team mutation — условный риск.

**Источник:** `.claude/skills/cc-linear/SKILL.md:23` — `.claude/scripts/linear-api.sh`; `:50-54` — assignee “Alexander Basis” и GitHub URL example; `:114-125` — `LINEAR_TEAM_KEY` или default `TEAM` и фиксированный state order; `.claude/skills/cc-linear/references/linear-api-reference.md:53,81-94` повторяет default `TEAM` и `/tmp/linear-TEAM-*` caches.

**Сценарий:** plugin используется в repo с другим team key, custom states/users или без bundled `.claude/scripts/linear-api.sh`.

**Последствие:** command recipes могут не найти wrapper, default `TEAM` может направить read/write в неверную команду, а фиксированный state/assignee vocabulary не соответствует workspace.

**Замена:** вынести Linear в optional tracker adapter; требовать явный configured team или read-only discovery, резолвить wrapper relative to loaded skill/target, получать states/users/labels из API перед mutation. Кэш должен быть namespaced по resolved team и task receipt должен фиксировать destination.

**Сохраняемый invariant:** видимые mutations требуют authorization; перед create/update выполняются duplicate/schema/read checks; после mutation делается matching independent read-back, а для unsupported relation/PR link честно отмечается отсутствие read-back.

### P1 — host capability contract не совпадает с инструкциями utility skills

**Класс:** доказанный контрактный конфликт; отсутствие конкретного host tool — условная часть.

**Источники:** `.claude/skills/dev-server/SKILL.md:17-19` разрешает `Bash, Monitor, Read, Glob`, но `:149-153` требует `TaskStop`; `:130-136` требует optional `/browser-use`. В `code-analysis` `.claude/skills/code-analysis/SKILL.md:73-79` есть safeguard для unresolved placeholders, но раскрытый `.claude/skills/code-analysis/references/project-checks.md:8-81` содержит runnable `{{SRC_DIR}}`, `{{LANGUAGE}}`, `{{TEST_DIR}}`, `{{CONFIG_FILES}}`, `{{SCHEMA_PATH}}` и TypeScript/JS-specific commands.

**Сценарий:** plugin запускается на host без `TaskStop`/browser-use или анализируется non-TS repo в Standard/Deep mode.

**Последствие:** dev-server не имеет объявленного инструмента для корректной остановки persistent monitor; UI verification может быть недоступна. Analysis может остановиться на placeholders или выбрать неподходящую metric recipe, несмотря на общий текст “adapt”.

**Замена:** перед запуском capability-check: разрешить stop через фактически доступный monitor/session primitive и делать UI smoke только при наличии browser capability; project-checks резолвить/фильтровать до выполнения, а language recipes вынести за stack-selected reference. Неразрешённый check — explicit skipped, не command.

**Сохраняемый invariant:** port conflict и kill остаются user-authorized; server считается started только после HTTP probe (и optional UI probe); analysis остаётся read-only и не выдаёт skipped check за evidence.

## Разделение доказанного и предположительного

Доказано чтением source: массовый bootstrap компонентного дерева, отсутствие единого task artifact contract, повтор lifecycle в трёх CLI, provider defaults Linear, а также `Monitor`/`TaskStop` mismatch и unresolved placeholders в disclosed analysis reference. Предположения: конкретная доступность `Monitor`, `TaskStop`, `browser-use` и актуальность pinned CLI/model flags на пользовательском host; их не следует объявлять багами без runtime/official verification.

## Ограничения аудита

- Не запускались setup/update recipes, external CLIs, Linear calls, dev servers, hooks или model binaries.
- Не проверялись package/build/bootstrap/runtime claims: это оставлено владельцу основного аудита.
- Старый checkout `/Users/alexandrbasis/Desktop/Coding/wythm-codex-workflows` исключён после уточнения источника; findings относятся только к указанному Astra plugin root и commit.
