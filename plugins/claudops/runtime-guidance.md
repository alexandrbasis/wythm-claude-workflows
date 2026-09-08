# Runtime guidance

The plugin is a read-only source of workflow defaults and resources. Skills operate
in the selected repository without requiring a copied workflow. Read applicable project
instructions and real command configuration. The shared task
contract lives at `skills/setup/references/task-context.md` in either package.

A project's `.claude/skills/<source-folder>/SKILL.md` is an explicit local override.
A `.disabled` marker stops that capability. Preserve those choices. Missing local files
use bundled defaults; unresolved command placeholders require repository evidence or a
specific clarification, not installation of the whole workflow.

Relative resource links resolve from the active skill directory. Legacy `.claude/docs`,
`.claude/scripts` and agent resources have a fallback in the setup skill's
`assets/workflow/.claude` tree. The explicit copied-workflow bootstrap remains available
for users who want repository-owned instructions; it preserves existing files and excludes
settings, MCP configuration, logs, secrets and runtime state. Hook activation is separate.

Portable clients may not implement Claude Code's host invocation guards. Explicit-only
behavior remains in skill text and metadata, without a claim of portable enforcement.
Claude agents are flattened into `agents/` with qualified skill dependencies. Agent Plugins
v1 packages contain skills; each host must supply supported delegation/tool capabilities.
