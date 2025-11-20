# Auto-Sync to Public Repository Setup

## Overview

The `auto-sync-public-repo.py` hook automatically syncs your `.claude/` directory to a public GitHub repository whenever you commit changes to `.claude/` files.

## What It Does

1. **Triggers on**: `PostToolUse` event after `git commit` commands
2. **Checks**: If any `.claude/` files were changed in the commit
3. **Syncs**: Copies `.claude/` directory to public repository (excluding sensitive files)
4. **Commits & Pushes**: Automatically creates commit and pushes to GitHub

## Setup Instructions

### 1. Create Public Repository

```bash
# Create public repository for your workflows
gh repo create your-claude-workflows --public --description "Claude Code workflows and configuration"

# Clone it to your workspace
cd "$(dirname "$PWD")"
git clone https://github.com/yourusername/your-claude-workflows.git
```

### 2. Update .claude/settings.local.json

Add the following to your `.claude/settings.local.json`:

```json
{
  "env": {
    "PUBLIC_REPO_PATH": "/absolute/path/to/your-claude-workflows"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-sync-public-repo.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Important**: Set `PUBLIC_REPO_PATH` to the absolute path where you cloned your public repository.

### 3. Make Hook Executable

```bash
chmod +x .claude/hooks/auto-sync-public-repo.py
chmod +x .claude/scripts/sync-to-public.sh
```

### 4. Test the Setup

#### Manual Test (Recommended First)

```bash
# Test sync script manually
PUBLIC_REPO_PATH="/path/to/public/repo" .claude/scripts/sync-to-public.sh

# Or use the slash command
/sync-public
```

#### Automatic Test (After Manual Works)

```bash
# Make a small change to a .claude file
echo "# Test" >> .claude/commands/sync-public.md

# Commit the change
git add .claude/commands/sync-public.md
git commit -m "test: verify auto-sync hook"

# Check logs to see if hook triggered
tail -20 .claude/hook-debug.log

# Verify public repo was updated
cd /path/to/public/repo && git log --oneline -1
```

## How It Works

### Hook Flow

```
You commit changes to .claude/
        ↓
Claude executes git commit via Bash tool
        ↓
PostToolUse hook triggers automatically
        ↓
auto-sync-public-repo.py runs
        ↓
Checks: git diff HEAD~1 HEAD for .claude/ files
        ↓
If found → executes sync-to-public.sh
        ↓
Syncs files to public repo (excluding secrets)
        ↓
Creates commit and pushes to GitHub
        ↓
Done! ✓
```

### Files Excluded from Sync

The following files are automatically excluded from public sync:

- `settings.local.json` - Contains sensitive tokens and IDs
- `hook-debug.log` - May contain sensitive paths
- `sync-public.log` - Sync operation logs
- `*.log` - All log files
- `__pycache__/`, `*.pyc` - Python cache
- `.DS_Store` - macOS system files
- `history.jsonl` - Conversation history
- `session-env/`, `todos/`, `debug/` - Runtime directories

## Manual Sync Command

Use `/sync-public` to manually trigger a sync without making a commit.

**When to use:**
- Testing the sync before enabling the hook
- Syncing changes you haven't committed yet
- Recovering from a failed automatic sync
- Initial sync of existing files

## Configuration

### Environment Variables

Set in `.claude/settings.local.json` → `env`:

- `PUBLIC_REPO_PATH` - **Required**. Absolute path to your public repository

### Hook Timeout

Default: 60 seconds. Increase if syncs take longer:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "command": "...",
            "timeout": 120  // Increase to 120 seconds
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Hook Not Triggering

1. **Check hook is executable**:
   ```bash
   ls -la .claude/hooks/auto-sync-public-repo.py
   ```

2. **Check settings.local.json syntax**:
   ```bash
   python3 -m json.tool .claude/settings.local.json
   ```

3. **Check hook logs**:
   ```bash
   tail -f .claude/hook-debug.log
   ```

### Sync Failing

1. **Verify rsync is installed**:
   ```bash
   which rsync
   ```

2. **Check PUBLIC_REPO_PATH**:
   ```bash
   echo $PUBLIC_REPO_PATH
   ls -la "$PUBLIC_REPO_PATH/.git"
   ```

3. **Check sync logs**:
   ```bash
   tail -f .claude/sync-public.log
   ```

4. **Test sync script manually**:
   ```bash
   PUBLIC_REPO_PATH="/path/to/repo" .claude/scripts/sync-to-public.sh
   ```

### Permission Errors

Ensure scripts are executable:

```bash
chmod +x .claude/hooks/auto-sync-public-repo.py
chmod +x .claude/scripts/sync-to-public.sh
```

## Logs

### Hook Execution Log

```bash
tail -f .claude/hook-debug.log
```

Shows:
- When hook triggers
- What files changed
- Sync status

### Sync Operation Log

```bash
tail -f .claude/sync-public.log
```

Shows:
- Detailed sync operations
- rsync output
- Git operations
- Errors and warnings

## Security

**Never commit**:
- `.claude/settings.local.json` (contains tokens)
- `.claude/hook-debug.log` (may contain sensitive paths)
- Any files with API keys or tokens

**Always verify**:
- Check public repository after first sync
- Ensure no sensitive data leaked
- Review `.gitignore` in public repo

## Disabling Auto-Sync

### Temporary Disable

Comment out the hook in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      // {
      //   "matcher": "Bash",
      //   "hooks": [...]
      // }
    ]
  }
}
```

### Use Manual Sync Only

Remove the PostToolUse hook entirely, use `/sync-public` command when needed.

## Example: Wythm Project

See the implementation in action:

- **Public repo**: https://github.com/alexandrbasis/wythm-claude-workflows
- **Hook**: `.claude/hooks/auto-sync-public-repo.py`
- **Sync script**: `.claude/scripts/sync-to-public.sh`
- **Command**: `.claude/commands/sync-public.md`

## Related Files

- `auto-sync-public-repo.py` - Hook script (this directory)
- `../scripts/sync-to-public.sh` - Sync script
- `../commands/sync-public.md` - Manual sync command

---

**Need help?** Check logs first, test manually, then enable automatic sync.
