# Configure and activate project hooks

Read when the user selects hook configuration. Configure only matching language/architecture hooks, then show the exact settings JSON diff before activation. Preserve existing matchers and settings. Existing approval for that exact diff remains valid.

**Hook placeholder mapping** — derive each value from Phase 1 detection results:

| Hook File | Placeholder | How to Fill |
|---|---|---|
| **lint-on-write.py** | `{{LINT_TARGETS}}` | Python list of source dirs, e.g. `["src"]` or `["backend", "frontend"]` |
| | `{{LINT_EXTENSIONS}}` | Python tuple of extensions, e.g. `(".ts", ".tsx")` or `(".py",)` |
| | `{{SKIP_PATTERNS}}` | Python tuple of path substrings to skip, e.g. `("node_modules", "dist/", "prisma/migrations")` |
| | `{{FORMAT_CMD}}` | Python list for formatter, e.g. `["npx", "prettier", "--write"]` or `["npx", "eslint", "--fix"]`. If no formatter detected, set to `[]` |
| **ts-typecheck-on-write.py** | `{{TYPECHECK_TARGET}}` | Directory with tsconfig.json relative to project root. `"."` for root-level tsconfig, or subdir like `"backend"` |
| | `{{TYPECHECK_CMD}}` | Python list, e.g. `["npx", "tsc", "--noEmit"]` |
| | `{{TYPECHECK_EXTENSIONS}}` | Python tuple, e.g. `(".ts", ".tsx")` |
| **test-after-edit.py** | `{{TEST_CMD_LIST}}` | Python list form of test command, e.g. `["npm", "run", "test:silent"]` or `["pytest", "-q"]` |
| | `{{SOURCE_DIRS}}` | Python list of watched dirs, e.g. `["src"]` or `["backend/src", "lib"]` |
| | `{{SOURCE_EXTENSIONS}}` | Python tuple matching language, e.g. `(".ts", ".tsx")` or `(".py",)` |
| **bash-guard.sh** | `{{PROTECTED_DIRS}}` | Pipe-separated dir names, e.g. `node_modules\|src\|dist` |
| | `{{DB_DANGER_PATTERN}}` | Regex for destructive DB commands based on ORM. Prisma: `prisma migrate reset\|prisma db push --force-reset`. Django: `migrate --run-syncdb\|flush`. Empty if no ORM. |
| | `{{DB_SAFE_CMD}}` | Safe alternative, e.g. `prisma migrate dev` or `python manage.py migrate` |
| | `{{DB_MIGRATE_PATTERN}}` | Regex for migration commands. Prisma: `prisma migrate`. Django: `manage.py migrate`. Empty if no ORM. |
| | `{{DB_MIGRATE_SAFE_FLAG}}` | Safety flag. Prisma: `--create-only`. Django: `--plan`. Empty if no ORM. |
| | `{{TEST_SILENT_PATTERN}}` | Regex matching test commands, e.g. `npm run test\|npm test`. Empty to disable enforcement. |
| | `{{TEST_SILENT_SUFFIX}}` | Suffix to enforce, e.g. `:silent` or ` --quiet` |
| **file-guard.sh** | `{{PROTECTED_FILE_PATTERN}}` | Regex for files needing special workflow, empty if none |
| | `{{PROTECTED_FILE_MESSAGE}}` | Block message, empty if none |
| | `{{CORE_LAYER_PATH}}` | Path substring for core/domain layer based on architecture. DDD: `/domain/`. Clean arch: `/core/`. Empty if no clear domain layer. |
| | `{{CORE_FORBIDDEN_IMPORTS}}` | Regex for forbidden imports in core layer, e.g. `from.*infrastructure\|from.*@prisma`. Empty if no core layer. |
| | `{{INTERFACE_NAMING_ENABLED}}` | `true` or `false` — enable only if codebase uses I-prefix convention |
| | `{{INTERFACE_PATH_FILTER}}` | Path filter for naming enforcement, e.g. `/src/` |
| | `{{CONSOLE_LOG_BLOCKED}}` | `true` or `false` — enable only if project uses a structured logger |
| | `{{CONSOLE_LOG_PATH_FILTER}}` | Path filter, e.g. `/src/` |
| | `{{CONSOLE_LOG_ALTERNATIVE}}` | Alternative message, e.g. `Use the Logger service instead of console.log` |
| **analytics-reminder.sh** | `{{SCREEN_FILE_PATTERN}}` | Regex for screen/page files. React Native: `/(app\|screens)/.*\.tsx$`. Next.js: `/app/.*/page\.tsx$`. Empty to disable. |
| | `{{ANALYTICS_REMINDER_MESSAGE}}` | Reminder text, or empty to disable |
| **stop-guard.sh** | `{{STOP_TEST_CMD}}` | Shell test command string, e.g. `cd backend && npm run test:ci 2>&1 \| tail -20` |
| | `{{STOP_BUILD_CMD}}` | Shell build command string, e.g. `cd backend && npx tsc --noEmit 2>&1 \| tail -20` |
| | `{{CODE_CHANGE_PATTERN}}` | Egrep regex selecting "real code" diffs. Reminder is suppressed when no diff matches. Examples — single Node app: `\.(ts\|tsx\|js\|jsx)$`; backend monorepo: `^backend/.*\.(ts\|tsx\|prisma)$`; python: `\.py$`. Empty falls back to `.*` (always remind). |
| | `{{WIKI_PATHS}}` | Space-separated path prefixes that trigger the wiki reminder, e.g. `docs/adr docs/architecture src`. Empty = always remind (when `VERIFY_WIKI=true`). Set `VERIFY_WIKI=false` in the file to disable entirely. |
| **test-before-pr.sh** | `{{BACKEND_PATH_FILTER}}` | Egrep regex matched against changed paths for scope 1. Single-app projects: `.*`. Monorepo backend: `^backend/`. Empty disables the scope. |
| | `{{BACKEND_TEST_CMD}}` | Test command for scope 1, run from project root via `eval`. Single-app: `npm run test:silent`. Monorepo: `cd backend && npm run test:silent`. Empty = skip tests. |
| | `{{BACKEND_BUILD_CMD}}` | Build/typecheck for scope 1, e.g. `npx tsc --noEmit` or `cd backend && npx tsc --noEmit`. Empty = skip build. |
| | `{{MOBILE_PATH_FILTER}}` | Path filter for scope 2 (mobile/frontend). Set all three MOBILE_* values to empty to disable the second scope on single-app projects. |
| | `{{MOBILE_TEST_CMD}}` | Test command for scope 2, e.g. `cd mobile-app && npm test -- --silent`. Empty = skip tests. |
| | `{{MOBILE_BUILD_CMD}}` | Build/typecheck for scope 2, e.g. `cd mobile-app && npx tsc --noEmit`. Empty = skip build. |

**Important**: For Python hook files, placeholders are replaced with Python literals (no quotes around lists/tuples). For shell hook files, values go inside existing double quotes. When a value should be empty/disabled, use empty string `""` for shell or `[]`/`()` for Python.

**Step 4: Wire hooks into settings.json**

Before activation, show the exact settings JSON diff and obtain approval for its hooks and side effects. Preserve prior approval for the same diff. Group additions by event and matcher:

**PreToolUse — Bash matcher** (add to existing or create):
1. `bash-guard.sh` — blocks `rm -rf`, force-push, destructive DB commands
2. `test-before-pr.sh` (timeout: 300) — blocks `gh pr create` unless tests + build pass for each affected scope

**PreToolUse — Write|Edit matcher** (add to existing or create):
3. `file-guard.sh` — architecture layer boundary enforcement

**PostToolUse — Write|Edit matcher** (create new):
4. `lint-on-write.py` — auto-format after file edits
5. `ts-typecheck-on-write.py` (timeout: 60) — run tsc after TS edits
6. `test-after-edit.py` (timeout: 120) — run tests after source edits (has 30s cooldown)
7. `analytics-reminder.sh` — remind about analytics for new screens/pages

**Stop** (add to existing or create):
8. `stop-guard.sh` — verification checklist before stopping (once per 24h)
9. `auto-commit-on-stop.sh` — WIP auto-commit on session end

**Wiring rules:**
- Resolve hook basenames to their actual subdirectory under `.claude/hooks/` (guards, testing, lint, typecheck, lifecycle). Verify the file exists. Use quoted absolute paths derived from the target repository; keep command quoting valid inside JSON.
- Present auto-commit separately in the activation diff: it writes Git history at session end. Activate it only when that behavior is approved.
- Add to **existing** matcher arrays when the event+matcher already exists in settings.json
- Create new matcher entries when they don't exist
- Preserve all existing hooks (like `pre-commit-validation.py`, `command-logger.py`, `sensitive-file-guard.py`, `read-counter.py`, `cost-tracker.py`)
- Set `timeout` for hooks that run external commands (typecheck, test, PR gate)

Example — existing `settings.json` has:
  "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "existing.sh"}]}]

Adding `bash-guard.sh` and `test-before-pr.sh` should produce:
  "PreToolUse": [{"matcher": "Bash", "hooks": [
    {"type": "command", "command": "existing.sh"},
    {"type": "command", "command": ".claude/hooks/guards/bash-guard.sh"},
    {"type": "command", "command": ".claude/hooks/testing/test-before-pr.sh", "timeout": 300}
  ]}]

