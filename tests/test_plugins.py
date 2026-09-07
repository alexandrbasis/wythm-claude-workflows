from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build_plugins import build, check
from scripts.validate_plugins import validate_artifact, validate_outputs


class PluginBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="claudops-plugin-test-")
        self.root = Path(self.temp.name)
        self.source = self.root / ".claude"
        self.source_skills = self.source / "skills"
        self.source_agents = self.source / "agents" / "review"
        self.source_skills.mkdir(parents=True)
        self.source_agents.mkdir(parents=True)
        (self.root / "plugin.json").write_text(
            json.dumps({
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                "name": "claudops",
                "version": "1.0.0",
            }),
            encoding="utf-8",
        )
        (self.root / ".claude-plugin").mkdir()
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": "claudops", "version": "1.0.0"}), encoding="utf-8"
        )
        (self.root / "README.md").write_text("Package README.\n", encoding="utf-8")
        (self.root / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (self.root / "packaging" / "runtime-guidance.md").parent.mkdir(parents=True)
        (self.root / "packaging" / "runtime-guidance.md").write_text("Runtime guidance.\n", encoding="utf-8")
        (self.root / "packaging" / "README.md").write_text("Package README.\n", encoding="utf-8")
        self._skill("si-quick", "quick", """Use `/si-quick` for a small task. See [the reference](../si-quick/reference.md).\n""", extra="disable-model-invocation: true\n")
        self._skill("update-docs", "udoc", "See `skills/update-docs/SKILL.md`.\n", extra="allowed-tools: Read, Write\n")
        self._skill("setup", "setup", "Read [task context](references/task-context.md).\n")
        context = self.source_skills / "setup" / "references" / "task-context.md"
        context.parent.mkdir()
        context.write_text("Resolve an existing task before creating a record.\n", encoding="utf-8")
        (self.source_skills / "si-quick" / "reference.md").write_text("/update-docs\n", encoding="utf-8")
        script = self.source_skills / "si-quick" / "scripts" / "run.sh"
        script.parent.mkdir()
        script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        script.chmod(0o755)
        (self.source / "settings.json").write_text("{}", encoding="utf-8")
        (self.source / "hooks" / "logs").mkdir(parents=True)
        (self.source / "hooks" / "logs" / ".gitkeep").write_text("", encoding="utf-8")
        (self.source / "mcp").mkdir()
        (self.source / "mcp" / "private.json").write_text("{}", encoding="utf-8")
        (self.source / "skills" / "setup" / "claudops-upstream.lock.json").write_text("{}", encoding="utf-8")
        (self.source / "skills" / "setup" / "__pycache__").mkdir()
        (self.source / "skills" / "setup" / "__pycache__" / "runtime.pyc").write_bytes(b"runtime")
        (self.source_agents / "reviewer.md").write_text(
            """---\nname: reviewer\ndescription: Reviews code.\nskills:\n  - quick\n---\nUse /si-quick.\n""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _skill(self, source_name: str, name: str, body: str, extra: str = "") -> None:
        directory = self.source_skills / source_name
        directory.mkdir(parents=True, exist_ok=True)
        directory.joinpath("SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Use this skill for {name}.\n{extra}---\n\n{body}",
            encoding="utf-8",
        )

    def test_builds_both_layouts_and_aliases(self) -> None:
        output = self.root / "dist"
        report = build(self.source, output)
        self.assertEqual(set(report.skill_names), {"quick", "setup", "udoc"})
        for kind, manifest in (
            ("claude", output / "claude" / "claudops" / ".claude-plugin" / "plugin.json"),
            ("agent", output / "agent" / "claudops" / "plugin.json"),
        ):
            artifact = output / kind / "claudops"
            self.assertTrue(manifest.is_file())
            self.assertEqual({path.name for path in (artifact / "skills").iterdir()}, {"quick", "setup", "udoc"})
            self.assertFalse((artifact / "hooks").exists())
            self.assertFalse((artifact / "settings.json").exists())
            self.assertFalse((artifact / "mcp.json").exists())
            self.assertTrue((artifact / "skills" / "setup" / "assets" / "workflow" / ".claude").is_dir())
        self.assertTrue((output / "claude" / "claudops" / "agents" / "reviewer.md").is_file())
        agent_text = (output / "claude" / "claudops" / "agents" / "reviewer.md").read_text(encoding="utf-8")
        self.assertIn("claudops:quick", agent_text)
        self.assertNotIn("/si-quick", agent_text)

        portable = (output / "agent" / "claudops" / "skills" / "quick" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("claude_disable_model_invocation: 'true'", portable)
        self.assertIn("only when explicitly requested by the user", portable)
        self.assertIn(".claude/skills/si-quick/SKILL.md", portable)
        self.assertIn("SKILL.md.disabled` exists, stop", portable)
        self.assertIn("../quick/reference.md", portable)
        self.assertIn("/quick", portable)
        self.assertNotIn("Use `/si-quick`", portable)
        self.assertNotIn("disable-model-invocation:", portable)
        self.assertTrue((output / "agent" / "claudops" / "skills" / "quick" / "scripts" / "run.sh").stat().st_mode & 0o111)

        allowed_fields = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        from scripts.build_plugins import _parse_frontmatter
        udoc_frontmatter, _ = _parse_frontmatter(output / "agent" / "claudops" / "skills" / "udoc" / "SKILL.md")
        self.assertEqual(udoc_frontmatter["allowed-tools"], "Read Write")

        for skill_file in (output / "agent" / "claudops" / "skills").glob("*/SKILL.md"):
            frontmatter, _ = _parse_frontmatter(skill_file)
            self.assertTrue(set(frontmatter) <= allowed_fields)
            self.assertIsInstance(frontmatter.get("description"), str)
            if "allowed-tools" in frontmatter:
                self.assertIsInstance(frontmatter["allowed-tools"], str)
            if "metadata" in frontmatter:
                self.assertTrue(all(isinstance(value, str) for value in frontmatter["metadata"].values()))

    def test_setup_asset_is_pristine_and_runtime_is_excluded(self) -> None:
        output = self.root / "dist"
        build(self.source, output)
        for artifact in (output / "claude" / "claudops", output / "agent" / "claudops"):
            template = artifact / "skills" / "setup" / "assets" / "workflow" / ".claude"
            self.assertFalse((template / "settings.json").exists())
            self.assertFalse((template / "mcp").exists())
            self.assertFalse((template / "hooks" / "logs").exists())
            self.assertFalse((template / "skills" / "setup" / "claudops-upstream.lock.json").exists())
            self.assertFalse((template / "skills" / "setup" / "__pycache__").exists())
            self.assertTrue((template / "skills" / "si-quick" / "SKILL.md").is_file())
            self.assertTrue((artifact / "README.md").is_file())
            self.assertTrue((artifact / "LICENSE").is_file())
            self.assertTrue((artifact / "runtime-guidance.md").is_file())

    def test_shared_context_and_legacy_resources_work_without_project_copy(self) -> None:
        # Source-folder aliases change in packages, so shared references must resolve
        # from an installed skill, independently of the consuming project's cwd.
        template = self.source / "docs" / "templates" / "discovery-template.md"
        template.parent.mkdir(parents=True)
        template.write_text("Discovery fixture\n", encoding="utf-8")
        project = self.root / "empty consuming project"
        project.mkdir()
        output = self.root / "dist"
        build(self.source, output)
        for kind in ("claude", "agent"):
            artifact = output / kind / "claudops"
            for skill in (artifact / "skills").iterdir():
                text = (skill / "SKILL.md").read_text(encoding="utf-8")
                pointer = re.search(r"(?:`|\]\()([^`\s)]*task-context\.md)", text)
                self.assertIsNotNone(pointer, f"Missing task-context route in {skill.name}")
                context = (skill / pointer.group(1)).resolve()
                self.assertTrue(context.is_relative_to(artifact.resolve()))
                self.assertEqual(context.read_bytes(),
                                 (self.source_skills / "setup/references/task-context.md").read_bytes())
            fallback = artifact / "skills/setup/assets/workflow/.claude/docs/templates/discovery-template.md"
            self.assertEqual(fallback.read_bytes(), template.read_bytes())
            if (artifact / "agents").exists():
                for agent in (artifact / "agents").glob("*.md"):
                    pointer = re.search(r"`([^`]*task-context\.md)`", agent.read_text(encoding="utf-8"))
                    self.assertIsNotNone(pointer, f"Missing task-context route in {agent.name}")
                    context = (agent.parent / pointer.group(1)).resolve()
                    self.assertTrue(context.is_file())
                    self.assertTrue(context.is_relative_to(artifact.resolve()))
        self.assertEqual(list(project.iterdir()), [])

    def test_validation_schema_inventory_and_stale_detection(self) -> None:
        output = self.root / "dist"
        build(self.source, output)
        self.assertEqual(validate_outputs(output, self.source), {"claude": [], "agent": []})
        check(self.source, output)
        (self.source_skills / "si-quick" / "SKILL.md").write_text(
            "---\nname: quick\ndescription: Changed.\n---\n\nChanged.\n", encoding="utf-8"
        )
        with self.assertRaises(ValueError):
            check(self.source, output)

    def test_validator_rejects_escaping_symlink(self) -> None:
        output = self.root / "dist"
        build(self.source, output)
        artifact = output / "agent" / "claudops"
        outside = self.root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        (artifact / "escape.txt").symlink_to(outside)
        errors = validate_artifact(artifact, "agent", self.source)
        self.assertTrue(any("symlink escapes" in error for error in errors))

    def test_build_rejects_source_escape_and_unmarked_cleanup(self) -> None:
        outside = self.root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        (self.source_skills / "si-quick" / "escape.txt").symlink_to(outside)
        with self.assertRaises(ValueError):
            build(self.source, self.root / "dist")

        (self.source_skills / "si-quick" / "escape.txt").unlink()
        output = self.root / "dist"
        (output / "claude" / "claudops").mkdir(parents=True)
        (output / "claude" / "claudops" / "keep.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            build(self.source, output)

    def test_build_rejects_overlapping_source_and_output(self) -> None:
        with self.assertRaises(ValueError):
            build(self.source, self.source / "dist")

    def test_build_is_byte_reproducible(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        build(self.source, first)
        build(self.source, second)
        for kind in ("claude", "agent"):
            left = first / kind / "claudops"
            right = second / kind / "claudops"
            left_files = {path.relative_to(left): path.read_bytes() for path in left.rglob("*") if path.is_file()}
            right_files = {path.relative_to(right): path.read_bytes() for path in right.rglob("*") if path.is_file()}
            self.assertEqual(left_files, right_files)


class ProductionInventoryTests(unittest.TestCase):
    def test_source_inventory_is_complete(self) -> None:
        repository = Path(__file__).resolve().parents[1]
        source = repository / ".claude"
        if not source.is_dir():
            self.skipTest("repository source is not available")
        from scripts.build_plugins import _read_agents, _read_skills

        self.assertEqual(len(_read_skills(source)), 40)
        self.assertEqual(len(_read_agents(source)), 18)


if __name__ == "__main__":
    unittest.main()
