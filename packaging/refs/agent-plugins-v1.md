# Packaging references

These are the primary specifications used by the builder and validator. They are
kept as links rather than copied prose so a future package refresh can recheck the
current contract.

## Agent Plugins v1

- [Specification](https://agent-plugins.org/specification)
- [Plugin manifest](https://agent-plugins.org/plugin-authors/manifest)
- [Skills](https://agent-plugins.org/plugin-authors/skills)
- [Plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
- [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)
- [Client implementation](https://agent-plugins.org/client-implementers/implement-an-agent-plugins-client)

The v1 portable surface is skills and MCP. A portable manifest uses a kebab-case
`name`, a description, and the v1 schema URL. Skill directories contain an immediate
`SKILL.md`; its `name` must match the directory and its `description` is required.
Agent and hook behavior is client-specific, so the Claude artifact retains those
components separately.

## Claude Code plugins

- [Plugin overview](https://code.claude.com/docs/en/plugins)
- [Plugin reference](https://code.claude.com/docs/en/plugins-reference)

Claude discovers `.claude-plugin/plugin.json` at the plugin root, `skills/` and
`agents/` directories, and optional hooks/MCP files. The package keeps hooks and MCP
out of the root so setup can materialize project configuration only after an explicit
user action. Claude-specific agent and skill frontmatter remains in the Claude
artifact; portable skills retain it as string metadata where the portable contract
does not define an equivalent field.

## Agent Skills format

- [Agent Skills specification](https://agentskills.io/specification)

The shared skill format requires `name` and `description`, limits names to lower-case
letters, numbers, and hyphens, and places the skill body in `SKILL.md`. The builder
normalizes the two maintained aliases (`si-quick` → `quick`, `update-docs` → `udoc`)
and rewrites plugin-local references while preserving project `.claude` paths.

## Vendored schema provenance

The schema files under `packaging/schemas/` were fetched from the canonical URLs on
2026-09-06 and are checked by SHA-256:

| File | Canonical URL | SHA-256 |
| --- | --- | --- |
| `plugin.schema.json` | [Agent Plugins manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) | `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883` |
| `mcp.schema.json` | [Agent Plugins MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) | `6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb` |
