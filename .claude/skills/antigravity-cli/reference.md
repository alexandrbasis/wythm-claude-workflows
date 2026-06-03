# Antigravity CLI (agy) Command Reference

> **Canonical source**: `agy --help` (local binary) + https://antigravity.google/docs/cli-overview
> **Last verified**: 2026-05-22 (agy v1.0.1, flags captured from `agy --help`)

## Installation

```bash
# macOS / Linux
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Windows PowerShell
irm https://antigravity.google/cli/install.ps1 | iex

agy update          # update existing installation
agy install         # configure environment paths and shell settings
```

Binary resolves to `agy` (e.g. `~/.local/bin/agy`).

## Authentication

`agy` authenticates via the system keyring, falling back to Google Sign-In if no active session exists. **There is no API key and no `GEMINI_API_KEY`-style env var.**

- **Local**: first interactive run opens your default browser to sign in.
- **Remote / SSH**: detects SSH sessions and prints an authorization URL to complete login locally.
- **Sign out**: run `/logout` inside the interactive TUI.

If `agy -p` fails with an auth error, the user must run `agy` once interactively to sign in.

## Core Command: One-Shot

All commands from Claude Code use `-p` to force non-interactive mode. The model is the
persisted default (set via `/model` or settings.json) — there is **no `-m` flag**.

```bash
agy -p "prompt"
```

**Full flag set (from `agy --help`, v1.0.1):**

| Flag | Description |
|---|---|
| `-p`, `--print`, `--prompt` | Run a single prompt non-interactively and print the response (REQUIRED from Claude Code) |
| `--print-timeout DUR` | Timeout for print-mode wait (default `5m0s`). Accepts Go durations: `90s`, `4m`, `8m` |
| `--add-dir DIR` | Add a directory to the workspace (repeatable) |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests. **DO NOT USE from Claude Code** — blocked by the auto-mode classifier |
| `-i`, `--prompt-interactive` | Run an initial prompt, then continue interactively (TTY only — will hang a Bash call) |
| `-c`, `--continue` | Continue the most recent conversation |
| `--conversation ID` | Resume a previous conversation by ID |
| `--sandbox` | Run in a sandbox with terminal restrictions enabled |
| `--log-file PATH` | Override CLI log file path |

**Subcommands:** `changelog`, `help`, `install`, `plugin` (alias `plugins`), `update`.

## Output Format

`agy -p` prints the **final answer as plain text** directly to stdout. There is no
`-o` / `--output-format` flag and no JSON wrapper. The canonical capture is just a redirect:

```bash
agy -p "prompt" --print-timeout 5m > /tmp/agy-result.txt 2> /dev/null
```

No `jq`, no `.response` extraction. Read the file with the **Read tool**.

> Note: `agy` may render file references as markdown links (e.g. `[file.ts](file:///abs/path)`) in its prose. This is cosmetic — the content is correct.

## Model Selection

| Mechanism | How |
|---|---|
| Interactive | Type `/model` in the TUI to pick and persist the default reasoning model |
| Config | `~/.gemini/antigravity-cli/settings.json` |
| One-shot | Uses the persisted default — **no command-line model flag** |

The Antigravity agent harness handles model routing internally; you do not select a model per `agy -p` call.

## File Injection

Use `@path` to inject file or directory contents into the prompt context.

```bash
agy -p "Review this code @src/main.ts"
agy -p "Analyze @src/ for security issues"
```

- `@file.ts` — inject single file
- `@src/` — inject directory contents
- Multiple `@` references allowed in one prompt
- `@path` is prompt-context injection, **not** a tool call — works in `-p` mode with no permission flag
- For files outside the cwd workspace, also pass `--add-dir <dir>`

## Built-in Tools & Web Grounding

`agy` shares the Antigravity agent harness, which includes Google Search grounding and web fetch. In `-p` mode:

- **Read-only tools** (web search, web fetch, file reads via `@path`) run **without** `--dangerously-skip-permissions` — verified working.
- **Write/shell tools** (file writes, `run_shell_command`) require `--dangerously-skip-permissions`, which is **blocked by Claude Code's classifier**. For those, the user must drive `agy` interactively.

Nudge phrases like "search the web for…", "look up…", "fetch this URL…" activate grounding inside the prompt.

## Configuration

| File | Scope |
|---|---|
| `~/.gemini/antigravity-cli/settings.json` | User settings (model, status line, permissions, keybindings) |
| Plugins | Managed via `agy plugin install/list/enable/disable` |
| MCP / skills / hooks | Configured via `/mcp`, `/skills`, slash commands in the TUI |

> Antigravity CLI reuses the `~/.gemini/` parent directory but namespaces its config under `antigravity-cli/`. Gemini CLI customizations (skills, MCP servers) can be migrated — see the official docs.

## Interactive Slash Commands (TUI only — not usable from `agy -p`)

For reference; these are typed inside the interactive TUI, not passed as flags:

| Command | Purpose |
|---|---|
| `/model` | Select default reasoning model (persists) |
| `/permissions` | Agent autonomy: `request-review`, `always-proceed`, `strict` |
| `/agents` | Open the subagents panel (background async work) |
| `/tasks` | Monitor / view logs / terminate background tasks |
| `/skills` | Browse local and global agent skills |
| `/mcp` | Configure MCP servers |
| `/resume` (`/switch`) | Resume or switch conversations |
| `/rewind` (`/undo`) | Roll back to a checkpoint |
| `/logout` | Sign out, clear cached credentials |

## Timeout Expectations

| Task Type | Expected Duration | `--print-timeout` |
|---|---|---|
| Simple query | 15-45 seconds | `2m` |
| Code review (small) | 1-3 minutes | `4m` |
| Code review (large) | 3-7 minutes | `8m` |
| Web research | 30-90 seconds | `3m` |
| Complex analysis | 3-10 minutes | `8m` |

`--print-timeout` defaults to `5m0s`. macOS has no `timeout` shell command — use `--print-timeout` plus the Bash tool's `timeout` parameter, not a shell `timeout` wrapper.

## Error Handling & Troubleshooting

| Issue | Solution |
|---|---|
| Auth error / not signed in | Run `agy` once interactively to complete Google Sign-In (keyring) |
| `--dangerously-skip-permissions` denied | Expected — Claude Code blocks it. Use `@path` injection; or run `agy` interactively for write tasks |
| Command hangs | You omitted `-p` and it dropped into the TUI; always pass `-p` from Claude Code |
| Unknown flag (e.g. `-m`, `-o`) | `agy -p` has no model or output-format flag; remove it |
| Print-mode timeout | Raise `--print-timeout` (e.g. `8m`) and the Bash tool `timeout` |
| File not found in answer | `@path` pointed outside the workspace — add it with `--add-dir`, or verify the path exists |
| Command not found | `command -v agy`; reinstall via `curl -fsSL https://antigravity.google/cli/install.sh | bash` |

Debug logging:
```bash
agy -p "prompt" --log-file /tmp/agy-debug.log
```
