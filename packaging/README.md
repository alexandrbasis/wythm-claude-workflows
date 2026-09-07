# Claudops package outputs

`scripts/build_plugins.py` produces two self-contained artifacts:

* `dist/claude/claudops` is a Claude Code plugin. It contains the Claude manifest,
  all 40 namespaced skills, and the 18 flattened project agents.
* `dist/agent/claudops` is an Agent Plugins v1 package. It contains the portable
  root manifest and the same skills with portable frontmatter.

Both artifacts contain the `setup` skill's pristine workflow templates under
`skills/setup/assets/workflow/.claude`. Templates are copied only when the explicit
setup bootstrap is run; package roots do not enable hooks, settings, or MCP servers.

## Load an extracted artifact

For Claude Code, start Claude in the target project and point it at the extracted
`claudops` directory:

```bash
claude --plugin-dir /absolute/path/to/claudops
```

Start the desired workflow directly; `/claudops:setup` is optional for project-specific
choices or copied-workflow maintenance. Task stages share
`skills/setup/references/task-context.md`: resolve the existing task, create a minimum
record when needed, and persist each stage's result there. No local workflow copy is
required. The portable artifact is loaded by the compatible Agent Plugins client;
its client determines the command and activation UI.

The portable root manifest and MCP schema follow Agent Plugins v1.0.0:

* [Plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
* [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)
* [Normative specification](https://agent-plugins.org/specification)

The checked-in schemas are the canonical v1.0.0 bytes fetched from those URLs on
2026-09-06. Their SHA-256 values are `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`
for `plugin.schema.json` and `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb`
for `mcp.schema.json`. Refresh and recheck them when the targeted Agent Plugins
version changes. Agent Plugins defines no registry or publishing service; distribution
remains client-owned.

Build and validate from the repository source checkout (these scripts are not part
of an extracted artifact):

```bash
python3 scripts/build_plugins.py --out dist
python3 scripts/validate_plugins.py --out dist
python3 scripts/build_plugins.py --check --out dist
```
