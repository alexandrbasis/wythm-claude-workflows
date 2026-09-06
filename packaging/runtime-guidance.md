# Runtime guidance

The plugin is a read-only source of workflow defaults. The `setup` skill owns explicit
project bootstrap and copies missing files from
`skills/setup/assets/workflow/.claude`; it excludes settings, MCP configuration, logs,
secrets, and other runtime state. Existing project files are preserved.

Skills prepend a project-configuration pointer. When a project contains the referenced
`.claude/skills/<source-folder>/SKILL.md`, that configured file is the capability source
of truth. A `.disabled` marker stops the skill. Unresolved placeholders route to setup.
Portable Agent Plugins clients may not implement Claude Code's host-level invocation
guards, so explicit-only behavior is repeated in the skill instructions and recorded as
metadata rather than claimed as a portable enforcement guarantee.

Claude-only agents are flattened into the plugin's `agents/` directory and their skill
dependencies are qualified as `claudops:<skill-name>`. Agent Plugins v1 standardizes
skills and MCP only; agents and hooks remain client-specific.
