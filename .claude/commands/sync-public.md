When the user requests to sync the Claude Code configuration to the public repository:

1. Execute the sync script:
   ```bash
   .claude/scripts/sync-to-public.sh
   ```

2. The script will:
   - Copy the `.claude/` directory to `wythm-claude-workflows` repository
   - Exclude sensitive files (settings.local.json, logs, etc.)
   - Create a commit with a descriptive message
   - Automatically push to GitHub

3. Show the user:
   - What files were synced
   - Commit status
   - GitHub repository URL: https://github.com/alexandrbasis/wythm-claude-workflows

4. If any errors occur, report them clearly and suggest manual intervention if needed

**Usage:** `/sync-public`

**Purpose:** Keep the public Claude Code workflows repository up-to-date with the latest agents, commands, hooks, and skills from the main Wythm project.

**Note:** This command is safe to run - it excludes all sensitive data (tokens, IDs, logs) by design.
