# Maintain the Claudops marketplaces

The public repository supplies two client catalogs and two generated packages:

| Client | Catalog | Package | Components |
|---|---|---|---|
| Claude Code | [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) | [`plugins/claudops`](../plugins/claudops/README.md) | 40 skills, 18 registered agents |
| Codex | [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) | [`plugins/claudops-agent`](../plugins/claudops-agent/README.md) | 40 skills, portable root manifest |

Both catalogs are named `claudops` and install `claudops@claudops`. Codex uses the
existing Agent Plugins v1 output; it needs no additional native manifest. Other
compatible clients can load the same portable package through their own installation
mechanism. The [quick start](../README.md#quick-start) covers ordinary installation.

The maintained skills remain under `.claude/`. Commit the source, matching manifests,
catalogs and generated packages together. Edit source rather than the snapshots.

The catalogs use documented relative sources for
[Claude Code](https://code.claude.com/docs/en/plugin-marketplaces#relative-paths) and
[Codex](https://developers.openai.com/plugins/build/plugins#marketplace-metadata).
Users add the Git repository. A catalog URL alone does not carry its package directory.

## Refresh the snapshots

Run from the source repository root:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python packaging/update_snapshot.py
.venv/bin/python packaging/update_snapshot.py --check
```

The updater validates both catalog identities and relative sources, including Codex
installation policy and category. Both source manifests must declare the same version.
It builds both formats at that version, runs both validators and checks reproducibility.
Every changed snapshot is copied and validated in a sibling staging directory before
any replacement. A failed promotion rolls both snapshots back; a rollback failure
preserves the previous packages at the reported backup path.

`--check` compares both snapshots with a fresh build without changing them. It rejects
missing or stale files, extra files and mode differences. CI also runs unit tests and
checks both development artifacts. The builder defaults to the paired source version,
so development builds and committed snapshots use the same release version.

Before publishing changed package contents, update `.claude-plugin/plugin.json` and
`plugin.json` together and regenerate. Keep the version for changes that do not alter
package contents, such as this maintainer guide or the root README. The bundled
`packaging/README.md` and `packaging/runtime-guidance.md` do affect package contents.
See [Claude Code version management](https://code.claude.com/docs/en/plugins-reference#version-management).

## Validate a local Claude Code installation

Use a temporary configuration from the repository root. This does not start a model
session or change the normal user profile:

```sh
CLAUDOPS_VALIDATION_CONFIG="$(mktemp -d)"
CLAUDOPS_MARKETPLACE_PATH="$PWD"
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin validate .
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin validate ./plugins/claudops
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin marketplace add "$CLAUDOPS_MARKETPLACE_PATH"
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin install claudops@claudops --scope user
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin list --json
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin details claudops@claudops
```

Confirm the installation path is under the temporary configuration, the plugin is
enabled, and it has 40 skills and 18 agents. There are no active hooks, MCP or LSP servers.

## Validate a local Codex installation

Use a current Codex CLI with portable plugin support. The publication check uses
Codex CLI 0.153.4. Set `CODEX_HOME` only for each validation command:

```sh
CLAUDOPS_CODEX_CONFIG="$(mktemp -d)"
CLAUDOPS_MARKETPLACE_PATH="$PWD"
CODEX_HOME="$CLAUDOPS_CODEX_CONFIG" codex plugin marketplace add "$CLAUDOPS_MARKETPLACE_PATH" --json
CODEX_HOME="$CLAUDOPS_CODEX_CONFIG" codex plugin add claudops@claudops --json
CODEX_HOME="$CLAUDOPS_CODEX_CONFIG" codex plugin list --marketplace claudops --json
```

Confirm `enabled: true`, the release version and an installation path under the temporary
configuration. Compare its files with `plugins/claudops-agent`. Native app-server
`skills/list` should report 40 enabled skills for `claudops@claudops` with no loading
errors, including `claudops:nf`, `claudops:quick` and `claudops:udoc`. This read-only
protocol check needs no thread or model invocation. The package has no registered agents,
hooks, MCP or LSP servers. Bundled role instructions are resources for supported workers.

## Verify publication and refresh

After publishing the reviewed commit, repeat both installations with fresh temporary
configurations and `alexandrbasis/claudops` as the marketplace source. Verify the fetched
commit, installed version, package bytes and component discovery. A local-path install
proves package resolution; the public Git source must be checked separately.

In each isolated installed profile, verify the documented refresh commands:

```sh
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin marketplace update claudops
CLAUDE_CONFIG_DIR="$CLAUDOPS_VALIDATION_CONFIG" claude plugin update claudops@claudops --scope user
CODEX_HOME="$CLAUDOPS_CODEX_CONFIG" codex plugin marketplace upgrade claudops --json
CODEX_HOME="$CLAUDOPS_CODEX_CONFIG" codex plugin add claudops@claudops --json
```

Codex marketplace upgrade refreshes a configured Git snapshot; use a Git source for
that test. Read the installed state again after refresh. A same-version refresh is not
proof of a version migration. For a release update, also exercise an existing previous
version in a temporary profile. Use the actual Claude installation scope if it differs.

Claude users load changed files with `/reload-plugins` or a new session. Codex users start
a new task. Report installation, discovery, update and actual workflow execution as
separate results; native discovery does not prove model behavior or optional integrations.
