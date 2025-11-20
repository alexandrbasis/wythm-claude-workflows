# Setup Guide: Wythm Claude Code Workflows

This guide will help you set up and use the Claude Code workflows from this repository in your own projects.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Full Installation](#full-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

- **Claude Code** - [Installation Guide](https://docs.anthropic.com/en/docs/claude-code/setup)
- **Python 3.11+** - Required for hooks
- **Node.js 18+** - Required for project-specific tools
- **Git** - Version control
- **GitHub CLI (`gh`)** - For PR automation: `brew install gh` (macOS)
- **rsync** - For file syncing (usually pre-installed on macOS/Linux)

### Optional Dependencies

- **Linear Account** - For Linear integration features
- **Telegram Bot** - For notification hooks
  - Create bot via [@BotFather](https://t.me/botfather)
  - Get your chat ID via [@userinfobot](https://t.me/userinfobot)

## Quick Start

### Option 1: Copy Individual Components

Pick specific agents, commands, or hooks that interest you:

```bash
# Clone this repository
git clone https://github.com/alexandrbasis/wythm-claude-workflows.git

# Copy specific components to your project
cp wythm-claude-workflows/.claude/agents/code-review-agents/security-code-reviewer.md \
   your-project/.claude/agents/

cp wythm-claude-workflows/.claude/commands/cr.md \
   your-project/.claude/commands/
```

### Option 2: Copy Entire Configuration

For a complete setup:

```bash
# Clone this repository
git clone https://github.com/alexandrbasis/wythm-claude-workflows.git

# Copy entire .claude directory
cp -r wythm-claude-workflows/.claude your-project/

# Important: Remove or customize hooks to avoid conflicts
rm your-project/.claude/hooks/*
```

## Full Installation

### Step 1: Clone Repository

```bash
cd ~/projects
git clone https://github.com/alexandrbasis/wythm-claude-workflows.git
cd wythm-claude-workflows
```

### Step 2: Review Components

Explore what's available:

```bash
# List all agents
ls -la .claude/agents/

# List all commands
ls -la .claude/commands/

# List all hooks
ls -la .claude/hooks/

# List all skills
ls -la .claude/skills/
```

### Step 3: Copy to Your Project

```bash
# Navigate to your project
cd /path/to/your/project

# Create .claude directory if it doesn't exist
mkdir -p .claude/{agents,commands,hooks,skills,mcp,scripts}

# Copy components you want to use
cp ~/projects/wythm-claude-workflows/.claude/agents/code-review-agents/*.md .claude/agents/
cp ~/projects/wythm-claude-workflows/.claude/commands/*.md .claude/commands/
```

### Step 4: Configure Settings

Create `.claude/settings.local.json` in your project:

```bash
# Copy template
cp ~/projects/wythm-claude-workflows/.claude/settings.template.json \
   .claude/settings.local.json

# Edit with your values
code .claude/settings.local.json
```

**Important**: Add `.claude/settings.local.json` to your `.gitignore`:

```bash
echo ".claude/settings.local.json" >> .gitignore
```

### Step 5: Make Hooks Executable

```bash
chmod +x .claude/hooks/*.py
chmod +x .claude/hooks/*.sh
chmod +x .claude/scripts/*.sh
```

## Configuration

### Basic Configuration

Edit `.claude/settings.local.json`:

```json
{
  "env": {
    "PUBLIC_REPO_PATH": "/path/to/your/public/repo"
  },
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)"
    ]
  },
  "hooks": {
    "PostToolUse": []
  }
}
```

### Hook Configuration

#### Enable Pre-Commit Validation

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-commit-validation.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

#### Enable Auto-Lint on Write

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint-on-write.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

#### Enable Auto-Sync to Public Repo

```json
{
  "env": {
    "PUBLIC_REPO_PATH": "/path/to/your/public/claude-workflows"
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

#### Enable Telegram Notifications

```json
{
  "env": {
    "CLAUDE_HOOK_BOT_TOKEN": "your-bot-token",
    "CLAUDE_HOOK_CHAT_ID": "your-chat-id"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR/.claude/hooks/telegram-notify.sh\""
          }
        ]
      }
    ]
  }
}
```

### MCP Server Configuration

For Linear integration, configure MCP in Claude Code's global settings:

```bash
# Edit global MCP config
code ~/.claude/mcp/linear.json
```

Add Linear API key:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your-linear-api-key"
      }
    }
  }
}
```

## Usage

### Using Agents

Agents are automatically available once placed in `.claude/agents/`:

```
# Code review with security focus
"Please review this code for security issues"
→ Claude will use the security-code-reviewer agent

# Architecture review
"Review this feature's architecture"
→ Claude will use the architect-reviewer agent
```

### Using Slash Commands

Commands in `.claude/commands/` are available via `/command-name`:

```bash
# Create a task
/ct

# Create a pull request
/cp

# Run quality gates
/qg

# Sync to public repo
/sync-public
```

### Using Hooks

Hooks run automatically when configured. View hook execution logs:

```bash
tail -f .claude/hook-debug.log
```

### Using Skills

Skills are invoked automatically when relevant or can be called explicitly:

```
# Git commit helper
"Help me write a commit message for these changes"

# Twitter assistant
"Help me write a tweet about this feature"
```

## Customization

### Creating Custom Agents

1. Create a new file in `.claude/agents/your-category/`:

```markdown
# Your Agent Name

You are a specialized agent for [specific task].

## Capabilities
- Capability 1
- Capability 2

## Process
1. Step 1
2. Step 2

## Output Format
Provide results in the following format:
...
```

2. Test the agent by requesting related tasks from Claude

### Creating Custom Commands

1. Create a new file in `.claude/commands/`:

```markdown
# /your-command

When the user runs this command:

1. Do task A
2. Do task B
3. Output result

**Usage:** `/your-command`
```

2. Test with `/your-command`

### Creating Custom Hooks

1. Create a Python script in `.claude/hooks/`:

```python
#!/usr/bin/env python3
import json
import sys

# Read hook input
input_data = json.load(sys.stdin)

# Your logic here
...

# Return success
sys.exit(0)
```

2. Make it executable:

```bash
chmod +x .claude/hooks/your-hook.py
```

3. Register in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "YourTool",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/your-hook.py"
          }
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Hooks Not Running

1. Check hook is executable:
   ```bash
   ls -la .claude/hooks/
   ```

2. Check settings.local.json syntax:
   ```bash
   python3 -m json.tool .claude/settings.local.json
   ```

3. Check hook logs:
   ```bash
   tail -f .claude/hook-debug.log
   ```

### Permission Errors

Add tool permissions in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(your-command:*)"
    ]
  }
}
```

### MCP Servers Not Working

1. Verify MCP server installation:
   ```bash
   npx -y @linear/mcp-server --version
   ```

2. Check MCP logs:
   ```bash
   tail -f ~/.claude/logs/mcp-*.log
   ```

3. Test MCP manually:
   ```bash
   LINEAR_API_KEY="your-key" npx -y @linear/mcp-server
   ```

### Sync Script Failing

1. Check rsync is installed:
   ```bash
   which rsync
   ```

2. Verify public repo path:
   ```bash
   echo $PUBLIC_REPO_PATH
   ls -la "$PUBLIC_REPO_PATH"
   ```

3. Check sync logs:
   ```bash
   tail -f .claude/sync-public.log
   ```

## Best Practices

1. **Start Small** - Copy individual components first, then expand
2. **Test Hooks** - Test hooks manually before enabling automation
3. **Backup Settings** - Keep a backup of your `.claude/settings.local.json`
4. **Review Logs** - Regularly check `hook-debug.log` for issues
5. **Customize Paths** - Update all absolute paths to match your system
6. **Secure Secrets** - Never commit `.claude/settings.local.json`

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/alexandrbasis/wythm-claude-workflows/issues)
- **Claude Code Docs**: [Official Documentation](https://docs.anthropic.com/en/docs/claude-code)
- **Main Project**: [Wythm Repository](https://github.com/alexandrbasis/wythm)

## Next Steps

1. Explore the agents in `.claude/agents/` to understand their capabilities
2. Try running slash commands to see the workflows in action
3. Review hooks to understand event-driven automation
4. Customize components for your project's specific needs
5. Share your own improvements and discoveries!

---

**Need more help?** Open an issue on GitHub or check the [main project documentation](https://github.com/alexandrbasis/wythm).
