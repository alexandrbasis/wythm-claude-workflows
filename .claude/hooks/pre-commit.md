# Hook: pre-commit migration guard

Purpose: Prevent commits where `backend/prisma/schema.prisma` changed but no migration was added.

## Behavior
- If `schema.prisma` is staged and no file under `backend/prisma/migrations/` is staged,
  run the Make Migrations command and stage the generated migration files.

## Agent steps
1. Check staged files for `backend/prisma/schema.prisma`.
2. Check if any files are staged under `backend/prisma/migrations/`.
3. If schema changed and no migration is staged, run the command from `/mm`:
   - See `.claude/commands/mm.md`.
4. Stage `backend/prisma/migrations/**` and proceed with the commit.

## Example Git hook script (optional)
Place in `.git/hooks/pre-commit` and make executable (`chmod +x .git/hooks/pre-commit`).

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"
STAGED_FILES="$(git diff --cached --name-only)"
if echo "$STAGED_FILES" | grep -q '^backend/prisma/schema\.prisma$' && \
   ! echo "$STAGED_FILES" | grep -q '^backend/prisma/migrations/'; then
  echo "[pre-commit] schema.prisma changed; generating migration via /mm..."
  npm --prefix backend run prisma:migrate:dev -- --name "auto_$(date +%Y%m%d_%H%M%S)" --create-only
  npm --prefix backend run prisma:migrate:deploy
  npm --prefix backend run prisma:generate
  git add backend/prisma/migrations
fi
exit 0
```

## Requirements
- Environment variables per `backend/docs/migration-structure.md`.
- Local Git hooks must be enabled by the developer (this doc provides a reference script).


