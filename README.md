# claudops

> Development workflows for Claude Code, also packaged as Agent Plugins v1 skills.

**Author:** [@alexandrbasis](https://x.com/alexandrbasis) | [@MishkaKey](https://x.com/MishkaKey)

[![Live Site](https://img.shields.io/badge/Live_Site-claudops-0d9488?style=flat-square)](https://alexandrbasis.com/claudops/workflows/)

<a href="https://alexandrbasis.com/claudops/workflows/">
  <img src="docs/workflow-overview.png" alt="Claudops AI Development Pipeline — 7 stages from feature discovery to deployment" width="100%">
</a>

---

Workflow skills for feature discovery, planning, implementation and review, available as a plugin or a repository-owned `.claude/` copy. Task stages share a durable record and adapt to the repository's existing conventions.

Works with any language, framework, and architecture — TypeScript, Python, Go, Ruby, Java, and more.

## Philosophy

This is a **human-in-the-loop pipeline**, not a fully autonomous agent. You choose the work and review the required artifacts. Once a bounded stage is approved, the agent completes that scope without asking again for the same decision. Nothing ships without your explicit sign-off.

- **You trigger** each stage — `/nf` for discovery, `/ct` for planning, `/si` for implementation, `/sr` for review
- **You validate** between stages — review the discovery doc before planning, review the plan before coding
- **You control the gates** — quality checks run automatically, but merging is always your decision
- **Agents assist, not replace** — 18 agents handle the grunt work (linting, testing, architecture checks), you make the calls

The result: AI speed with human judgment. Full context at every step, no black-box automation.

## Highlights

- **`/setup` wizard** — records necessary project choices; plugin workflows discover repository commands without copying all instructions
- **`/update-setup`** — pulls upstream changes from claudops, shows a diff, lets you cherry-pick updates while preserving your local customizations
- **18 specialized agents** — TDD, code review, task validation, research
- **40 skills** — full dev lifecycle, dev server monitoring, and cross-AI helpers (Antigravity, Codex CLI, Cursor CLI)
- **Skills ↔ Agents composability** — agents preload shared convention skills via `skills:` frontmatter
- **Cross-AI plan review** — optional Gemini verification of plans (see `review-plan-gemini.sh`)
- **Hooks** — lint on write, sync, validation, guards, metrics
- **Linear integration** — project management from your terminal (`cc-linear` skill)

---

## What's Inside

### Agents (18)

**Automation** (`.claude/agents/automation-agents/`)
| Agent | Purpose |
|-------|---------|
| `automated-quality-gate` | Runs lint, types, tests before review |
| `developer-agent` | Universal agent for scoped work items |
| `integration-test-runner` | E2E and integration test execution |
| `senior-architecture-reviewer` | Reviews approach, architecture, TDD compliance |

**Code review** (`.claude/agents/code-review-agents/`)
| Agent | Focus |
|-------|-------|
| `code-quality-reviewer` | SOLID, maintainability, code smells |
| `documentation-accuracy-reviewer` | Docs completeness and accuracy |
| `performance-reviewer` | N+1 queries, caching, optimization |
| `security-code-reviewer` | OWASP Top 10, injection, auth issues |
| `spec-compliance-reviewer` | Spec and requirements alignment |
| `test-coverage-reviewer` | Coverage gaps, test quality |
| `structural-quality-reviewer` | Structural patterns across changed surfaces |

**Task validators** (`.claude/agents/tasks-validators-agents/`)
| Agent | Purpose |
|-------|---------|
| `plan-reviewer` | Technical plan validation |
| `task-splitter` | Evaluates if a task needs breakdown |
| `task-decomposer` | Phase structure for split tasks |

**Workflow** (`.claude/agents/wf-agents/`)
| Agent | Purpose |
|-------|---------|
| `changelog-generator` | Changelog from task docs |
| `create-pr-agent` | PR automation with Linear integration |
| `docs-updater` | Documentation synchronization |

**Helpers** (`.claude/agents/helpful-agents/`)
| Agent | Purpose |
|-------|---------|
| `comprehensive-researcher` | In-depth research tasks |

---

### Skills (40)

See [`.claude/skills/README.md`](.claude/skills/README.md) for the full index. Summary:

| Area | Examples |
|------|----------|
| Setup & conventions | `setup`, `update-setup`, `coding-conventions`, `review-conventions` |
| Core workflow | `ct`, `si`, `si-quick`, `sr`, `prc`, `ph`, `nf`, `product`, `vp`, `blueprint` |
| Discovery & design | `brainstorm`, `design-exploration`, `analyze`, `grill-me`, `rip` |
| Quality & debugging | `dev-server`, `code-analysis`, `dbg`, `fci` |
| Cross-AI | `antigravity-cli`, `codex-cli`, `cursor-cli` |
| Integrations & meta | `cc-linear`, `deep-research`, `parallelization`, `sbs`, `update-docs` |

---

### Skills ↔ Agents Composability

Review agents and the developer agent preload shared convention skills via `skills:` frontmatter — no per-agent duplication:

```yaml
# In agent frontmatter
skills:
  - review-conventions   # preloaded into all 7 review agents
  - coding-conventions   # preloaded into developer-agent
```

Plugin workflows read project instructions, command sources and optional `CLAUDOPS.md`. For repository-owned installations, `/setup` can configure the local convention skills; existing customizations remain authoritative.

---

### Cross-AI plan review

Optional flow when Gemini CLI is configured — see `.claude/scripts/review-plan-gemini.sh` and hook wiring in `.claude/settings.json`.

**What Gemini can check:** security, architecture, performance, edge cases, testability.

---

### Hooks

Python/shell hooks under `.claude/hooks/` — lint on write, agent sync, pre-commit checks, bash/file guards, cost tracking, etc. Details: [`.claude/hooks/README.md`](.claude/hooks/README.md).

---

## Repository structure

```
plugin.json                  # Agent Plugins manifest source
.claude-plugin/plugin.json   # Claude manifest source
scripts/                    # Reproducible build and validation
dist/                       # Generated packages (not source)
.claude/
├── agents/           # Specialized subagents
├── docs/
│   ├── templates/    # PRD, JTBD, decomposition, review templates
│   └── references/
├── hooks/            # Claude Code hooks (see hooks/README.md)
├── scripts/          # e.g. review-plan-gemini.sh, linear-api.sh
├── skills/           # Slash-command skills (see skills/README.md)
└── settings.json     # Hook and project settings (copy & customize)

workflow-visualization.html   # Interactive workflow map (open in browser)
```

---

## Use as a plugin

Build both packages from the maintained `.claude/` source:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/build_plugins.py
.venv/bin/python scripts/validate_plugins.py
```

For **Claude Code**, launch it in your target project with the built directory:

```bash
claude --plugin-dir /absolute/path/to/claudops/dist/claude/claudops
```

Start `/claudops:nf`, `/claudops:ct`, `/claudops:si` or `/claudops:sr` in the target
repository. The package contains all 40 skills and 18 agents. Setup is optional: use
it for durable project choices or to maintain an explicitly requested local workflow
copy. Shared plugin files stay unchanged, and hook activation requires its own
authorized settings change.

Each task stage resolves the same task entrypoint. Existing layouts and documents are
reused; the fallback is `tasks/task-YYYY-MM-DD-<slug>/TASK.md`. A small task can keep its
requirements, plan and verification in that one file. Discovery, prototypes, phase
plans and reviews become separate linked artifacts when needed. See the
[shared task contract](.claude/skills/setup/references/task-context.md).

For **Agent Plugins v1**, use `dist/agent/claudops` with a compatible client.
The portable package has `plugin.json` and all 40 skills; its format does not provide
Claude's agent execution or invocation controls. Clients must supply the capabilities
a selected workflow needs. Explicit-only policies are retained as metadata and text;
portable clients must enforce those policies for equivalent discovery behavior.
See [package architecture and validation](packaging/README.md) for the precise limits.

These are generated packages, ready for local loading or distribution after review.
Building does not install, publish, enable hooks, or change account settings.
Agent Plugins is a [package format](https://agent-plugins.org/specification);
installation and publication belong to each client. Claude's local loader is documented
in its [plugin reference](https://code.claude.com/docs/en/plugins-reference).

## Use the copied workflow

### 1. Clone the source and preview project templates
```bash
git clone https://github.com/alexandrbasis/claudops.git
python3 claudops/.claude/skills/setup/scripts/bootstrap_project.py --project /absolute/your-project
# Review the listed additions, then materialize them:
python3 claudops/.claude/skills/setup/scripts/bootstrap_project.py --project /absolute/your-project --apply
cd /absolute/your-project
```

### 2. Run the setup wizard
```
/setup
```

The wizard will:
1. **Inspect your codebase** for stack, structure, commands, and architecture
2. **Resolve** relevant settings from evidence and ask about material unknown choices
3. **Apply** the requested local configuration, reporting unresolved values and previewing hook activation

Configured values live in your local `.claude/` files. Unknown values remain visible for follow-up; a copied hook is not active until it is wired into settings.

### 3. Keep it updated
```
/update-setup
```

Pulls latest changes from the upstream claudops repo, shows what's new or modified, and lets you cherry-pick what to apply. Local-only files are excluded; updates to customized upstream files require an explicit conflict decision.

### 4. Start using workflows
```
/ct    — create a technical decomposition
/si    — start implementation from a task
/sr    — run multi-agent code review
```

### Cherry-pick individual skills
```bash
cp -r claudops/.claude/skills/si your-project/.claude/skills/
cp claudops/.claude/scripts/review-plan-gemini.sh your-project/.claude/scripts/
```

### As reference
Study the patterns and adapt them to your own workflows.

---

## Key workflows

### TDD pipeline
```
/ct → /si → automated-quality-gate → senior-architecture-reviewer
```

### Multi-agent code review
```
code-quality + security + performance + test-coverage + documentation
```

### Task-driven flow
```
/nf → /vp (optional) → /ct (split when needed) → /si → /sr → /prc → authorized delivery
```

### Cross-AI
- Gemini CLI — plan review, web-grounded research
- Codex / Cursor CLI — second-opinion review (see `cross-ai-protocol` template)

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Git + GitHub CLI (`gh`)
- Optional: Gemini CLI (`npm i -g @google/gemini-cli`)
- Optional: Linear API access

---

## Security & privacy

**Not included (sensitive):** `settings.local.json`, API keys, MCP credentials, log files

**Safe to share:** Agents, skills, hook scripts, and templates in this repo (exclude local overrides)

---

## Contributing

Found a better pattern? Have suggestions?
- Open an issue with your idea
- Share your own workflows
- Contribute improvements via PR

---

## License

MIT — See [LICENSE](LICENSE)
