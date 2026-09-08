# Maintain the Claudops marketplace

The marketplace at [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json)
is named `claudops`. Its `claudops` entry points to the generated Claude package in
[`plugins/claudops`](../plugins/claudops/README.md), so users install `claudops@claudops`
through Claude Code without building it themselves. The
[quick start](../README.md#quick-start) contains the reader-facing installation steps.

The maintained skills remain under `.claude/`. Do not edit the generated snapshot
directly. Commit the catalog and generated package together when publishing a change.

This uses Claude Code's documented
[relative plugin source](https://code.claude.com/docs/en/plugin-marketplaces#relative-paths).
Users add the Git repository as the marketplace source. A direct URL to
`marketplace.json` alone does not carry the relative package directory.

## Refresh the snapshot

Run these commands from the source repository root. The Python environment needs
the dependencies in `requirements-dev.txt`.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python packaging/update_snapshot.py
.venv/bin/python packaging/update_snapshot.py --check
```

The updater first checks the catalog's identity and relative source and requires matching
versions in both source manifests. It passes that version to the existing builder, runs
both package validators and checks reproducibility. A replacement is copied and validated
in a sibling staging directory before switching the known generated `plugins/claudops`
directory. If the switch fails, the updater restores the previous package.

`--check` validates the same catalog and version contract, then compares the snapshot
with a fresh build without changing the snapshot. It rejects missing or stale files,
extra files and mode differences. CI runs this check for pushes and pull requests.

Before publishing changed package contents, update the version in both source manifests,
`.claude-plugin/plugin.json` and `plugin.json`, then regenerate the snapshot. Keep the
existing version for changes that do not alter the package, such as this maintainer
guide or root README. Review the source changes, catalog and generated diff together.
See [Claude Code version management](https://code.claude.com/docs/en/plugins-reference#version-management).

The builder also creates an Agent Plugins v1 artifact. For separate development
outputs and local loading, see the [package guide](README.md).

## Validate a local installation

Use a temporary Claude configuration to check the catalog and package from the
repository root. This leaves your normal Claude Code profile unchanged and does not
start a model session.

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

Catalog and package validation are separate checks. Confirm that the installation
path is under the temporary configuration, the plugin is enabled, and its component
inventory contains 40 skills and 18 agents. The package enables no hooks, MCP servers
or LSP servers. This local test verifies the relative source and installed package;
it does not verify GitHub publication or a workflow's runtime behavior.

## Verify publication

After publishing the reviewed catalog and snapshot to `alexandrbasis/claudops`, repeat
the installation check with a fresh temporary configuration, using the public source:

```sh
CLAUDOPS_PUBLIC_CONFIG="$(mktemp -d)"
CLAUDE_CONFIG_DIR="$CLAUDOPS_PUBLIC_CONFIG" claude plugin marketplace add alexandrbasis/claudops
CLAUDE_CONFIG_DIR="$CLAUDOPS_PUBLIC_CONFIG" claude plugin install claudops@claudops --scope user
CLAUDE_CONFIG_DIR="$CLAUDOPS_PUBLIC_CONFIG" claude plugin list --json
CLAUDE_CONFIG_DIR="$CLAUDOPS_PUBLIC_CONFIG" claude plugin details claudops@claudops
```

Check the published commit, installed version and component inventory. For a package
version update, also verify an existing installation through
`claude plugin marketplace update claudops` and
`claude plugin update claudops@claudops --scope user` in its temporary configuration.
Use the installation's actual scope if it differs.

Users load changed files with `/reload-plugins` or a new session. Report installation,
update and workflow execution as separate verification results.
