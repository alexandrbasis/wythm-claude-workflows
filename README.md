# Wythm Claude Code Workflows

> Production-ready Claude Code workflows, hooks, agents, and commands for AI-assisted software development

This repository showcases the complete Claude Code setup used in the [Wythm](https://github.com/alexandrbasis/wythm) project - an AI-powered vocabulary learning platform. These workflows demonstrate advanced Claude Code usage patterns, custom automation, and development best practices.

## What's Inside

### Custom Agents (15+)
Specialized agents for different development tasks:

**Code Review Agents** (`.claude/agents/code-review-agents/`)
- `architect-reviewer.md` - Architecture and SOLID principles review
- `code-quality-reviewer.md` - Code quality and maintainability
- `documentation-accuracy-reviewer.md` - Documentation completeness
- `performance-reviewer.md` - Performance optimization
- `security-code-reviewer.md` - Security vulnerability scanning
- `test-coverage-reviewer.md` - Test coverage analysis

**Task Validators** (`.claude/agents/tasks-validators-agents/`)
- `plan-reviewer.md` - Technical plan validation
- `task-pm-validator.md` - Project management validation
- `task-splitter.md` - Task breakdown evaluation

**Workflow Agents** (`.claude/agents/wf-agents/`)
- `changelog-generator.md` - Automated changelog creation
- `create-pr-agent.md` - Pull request automation with Linear integration
- `docs-updater.md` - Documentation synchronization
- `linear-task-manager.md` - Linear issue management

**Helper Agents** (`.claude/agents/helpful-agents/`)
- `comprehensive-researcher.md` - In-depth research tasks
- `meeting-task-syncer.md` - Meeting notes to Linear tasks

### Slash Commands
Custom commands for streamlined workflows (`.claude/commands/`):

**Development Workflow**
- `/asr` - Automated sprint review with specialized agents
- `/ct` - Create task documentation (JTBD-based)
- `/cb` - Create branch from task
- `/cp` - Create pull request with Linear integration

**Product Management** (`.claude/commands/product/`)
- `/product:cjtbd` - Jobs-to-be-Done analysis
- `/product:cprd` - Product Requirements Document creation

**Code Review**
- `/cr` - Comprehensive code review
- `/review-pr` - GitHub PR review

**Quality Gates**
- `/qg` - Run quality gates (format, lint, type check)
- `/fix-lint` - Auto-fix linting issues

### Hooks
Event-driven automation (`.claude/hooks/`):

**Quality Assurance**
- `pre-commit-validation.py` - Pre-commit quality checks
- `lint-on-write.py` - Auto-lint on file writes

**Synchronization**
- `auto-sync-claude-agents.py` - Sync agent configurations
- `claude-agents-sync.py` - Agent sync orchestration

**Integrations**
- `telegram-notify.sh` - Telegram notifications for events
- `ct-context-injector.py` - Task context injection

**Current Hook** (auto-sync to this repo)
- `auto-sync-public-repo.py` - Automatically syncs `.claude/` changes to this public repository

### Skills
Specialized capabilities (`.claude/skills/`):

- `git-commit-helper` - Generate descriptive commit messages
- `twitter-x-assistant` - Social media content optimization
- `skill-creator` - Guide for creating new skills
- `gemini-cli` - Google Gemini CLI integration

### MCP Servers
Model Context Protocol integrations (`.claude/mcp/`):

- Linear integration for issue management
- IDE integration for diagnostics
- Custom MCP server configurations

## Repository Structure

```
.claude/
├── agents/                    # 15+ specialized agents
│   ├── code-review-agents/   # Quality & security reviewers
│   ├── tasks-validators-agents/ # Task validation agents
│   ├── wf-agents/            # Workflow automation
│   └── helpful-agents/       # Research & meeting sync
├── commands/                  # Slash commands
│   ├── product/              # Product management commands
│   └── [development commands]
├── hooks/                     # Event-driven automation
├── skills/                    # Specialized capabilities
├── mcp/                      # MCP server configs
└── scripts/                  # Utility scripts

docs/
└── setup-guide.md            # Detailed setup instructions
```

## How to Use These Workflows

### Option 1: Full Setup (Recommended)
1. Clone this repository
2. Copy `.claude/` directory to your project root
3. Review and customize configuration for your needs
4. Install dependencies (see [Setup Guide](docs/setup-guide.md))
5. Configure MCP servers and hooks

### Option 2: Cherry-Pick Components
Pick specific agents, commands, or hooks:

```bash
# Copy specific agent
cp wythm-claude-workflows/.claude/agents/code-review-agents/security-code-reviewer.md \
   your-project/.claude/agents/

# Copy specific command
cp wythm-claude-workflows/.claude/commands/ct.md \
   your-project/.claude/commands/
```

### Option 3: Learn and Adapt
Study the patterns and create your own:
- Read agent prompts to understand specialization patterns
- Examine hooks for event-driven automation ideas
- Review commands for workflow optimization

## Key Features

### 1. Automated Code Review Pipeline
Multi-agent review system covering:
- Architecture patterns (SOLID, DDD)
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- Test coverage
- Documentation accuracy

### 2. Task-Driven Development
JTBD (Jobs-to-be-Done) based workflow:
- `/ct` - Create comprehensive task documentation
- `/cb` - Create feature branch from task
- `/cp` - Create PR with Linear integration
- Automatic traceability and audit trail

### 3. Quality Gates Integration
Automated checks before commits:
- Format validation (Black, isort)
- Linting (flake8, mypy)
- Type checking
- Test execution

### 4. Linear Integration
Seamless project management:
- Create/update issues from Claude
- Link PRs to Linear tasks
- Sync meeting notes to tasks
- Automated changelog generation

### 5. Hook-Based Automation
Event-driven workflows:
- Pre-commit validation
- Auto-sync configurations
- Telegram notifications
- Context injection for tasks

## Technology Stack

**Backend Project Context:**
- NestJS + TypeScript
- PostgreSQL + Prisma ORM
- Domain-Driven Design (DDD)
- Clean Architecture

**Development Tools:**
- Claude Code (AI-assisted development)
- Linear (Project management)
- GitHub Actions (CI/CD)
- MCP Servers (Integrations)

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.11+ (for hooks)
- Node.js 18+ (for project context)
- Git configured
- GitHub CLI (`gh`) installed
- Linear API access (optional, for full workflow)

## Configuration

### Required Environment Variables

Create `.claude/settings.local.json` (not tracked in this repo):

```json
{
  "hooks": {
    "PostToolUse": [...],
    "PreToolUse": [...]
  },
  "env": {
    "PUBLIC_REPO_PATH": "/path/to/wythm-claude-workflows",
    "TELEGRAM_BOT_TOKEN": "your-token-here",
    "TELEGRAM_CHAT_ID": "your-chat-id",
    "LINEAR_API_KEY": "your-linear-key"
  }
}
```

See [docs/setup-guide.md](docs/setup-guide.md) for detailed configuration.

## Security & Privacy

**What's NOT Included:**
- `settings.local.json` - Contains sensitive tokens and IDs
- `history.jsonl` - Conversation history
- `hook-debug.log` - May contain sensitive paths
- Runtime directories (`session-env/`, `todos/`, etc.)

**Safe to Share:**
- Agent definitions
- Command templates
- Hook scripts (sanitized)
- MCP configurations (anonymized)
- Skills and workflows

## Real-World Usage

This setup powers the development of [Wythm](https://github.com/alexandrbasis/wythm), a production NestJS application with:
- 15+ custom agents for specialized reviews
- Automated task creation and PR workflows
- Linear integration for project tracking
- Multi-stage code review pipeline
- JTBD-based feature development

**Development Metrics:**
- 40+ completed tasks with full traceability
- 100+ agent-reviewed PRs
- Automated quality gates on every commit
- Real-time Telegram notifications
- Automated changelog generation

## Contributing

Found a better pattern? Have suggestions?
- Open an issue with your idea
- Share your own Claude Code workflows
- Contribute improvements via PR

## License

MIT License - See [LICENSE](LICENSE) for details

## Links & Resources

- **Main Project:** [Wythm Repository](https://github.com/alexandrbasis/wythm)
- **Claude Code Docs:** [Official Documentation](https://docs.anthropic.com/en/docs/claude-code)
- **Linear:** [Project Management Tool](https://linear.app)
- **Blog Posts:** Coming soon on social media

## Acknowledgments

Built with [Claude Code](https://claude.com/claude-code) - AI-assisted software development by Anthropic.

---

**Auto-synced from main repository** | Last update: 2025-01-20 | [View Sync Hook](.claude/hooks/auto-sync-public-repo.py)
