"""Verify failed builds preserve inputs and stay inside the selected output tree."""

import json
import unittest
from pathlib import Path

from scripts.build_plugins import build, check
from scripts.validate_plugins import validate_outputs
from tests import test_plugins as fixtures


class PluginBoundaryTests(unittest.TestCase):
    _skill = fixtures.PluginBuildTests._skill
    setUp = fixtures.PluginBuildTests.setUp
    tearDown = fixtures.PluginBuildTests.tearDown

    def snapshot(self, root):
        return {
            str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mode & 0o777)
            for path in root.rglob("*") if path.is_file() and not path.is_symlink()
        }

    def assert_invalid_names_preserve_tree(self, path):
        output = self.root / "dist"
        build(self.source, output)
        original = path.read_text()
        for name in ("../../../../.claude/skills/setup", str(self.root / "escape"), "bad--name", 42):
            with self.subTest(name=name):
                text = original.splitlines()
                text = ["name: " + json.dumps(name) if line.startswith("name:") else line for line in text]
                path.write_text("\n".join(text) + "\n")
                before = self.snapshot(self.root)
                with self.assertRaisesRegex(ValueError, "name"):
                    build(self.source, output)
                self.assertEqual(before, self.snapshot(self.root))
                path.write_text(original)

    def test_skill_names_are_validated_before_writes(self):
        self.assert_invalid_names_preserve_tree(self.source_skills / "si-quick/SKILL.md")

    def test_agent_names_are_validated_before_writes(self):
        self.assert_invalid_names_preserve_tree(self.source_agents / "reviewer.md")

    def test_internal_file_symlink_cannot_copy_excluded_configuration(self):
        for target in (self.source / "settings.json", self.source / ".env"):
            with self.subTest(target=target.name):
                target.write_text("private fixture")
                link = self.source_skills / "si-quick/leak.txt"
                link.symlink_to(target)
                output = self.root / "dist"
                with self.assertRaisesRegex(ValueError, "symlink"):
                    build(self.source, output)
                self.assertFalse(output.exists())
                link.unlink()

    def test_internal_directory_symlink_fails_instead_of_dropping_content(self):
        directory = self.source_skills / "setup/references"
        directory.mkdir(exist_ok=True)
        (directory / "reference.md").write_text("reference")
        (self.source_skills / "si-quick/references").symlink_to(directory, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            build(self.source, self.root / "dist")
        self.assertFalse((self.root / "dist").exists())

    def test_both_output_parent_aliases_fail_before_any_cleanup(self):
        for kind in ("claude", "agent"):
            with self.subTest(kind=kind):
                output = self.root / (kind + "-dist")
                build(self.source, output)
                original = output / kind
                outside = self.root / (kind + "-outside")
                original.rename(outside)
                original.symlink_to(outside, target_is_directory=True)
                before = self.snapshot(self.root)
                with self.assertRaisesRegex(ValueError, "symlink"):
                    build(self.source, output)
                self.assertEqual(before, self.snapshot(self.root))
                self.assertTrue(any(validate_outputs(output, self.source).values()))

    def test_check_returns_existing_outputs_and_detects_executable_mode_drift(self):
        output = self.root / "dist"
        build(self.source, output)
        report = check(self.source, output)
        expected = ((output / "claude/claudops").resolve(), (output / "agent/claudops").resolve())
        self.assertEqual(report.outputs, expected)
        self.assertTrue(all(path.is_dir() for path in report.outputs))
        script = output / "claude/claudops/skills/quick/scripts/run.sh"
        script.chmod(0o644)
        with self.assertRaises(ValueError):
            check(self.source, output)

    def test_user_selected_parent_alias_is_supported(self):
        parent = self.root / "real-parent"
        parent.mkdir()
        alias = self.root / "parent-alias"
        alias.symlink_to(parent, target_is_directory=True)
        output = alias / "dist"
        report = build(self.source, output)
        self.assertTrue(all(path.is_dir() for path in report.outputs))
        self.assertEqual(check(self.source, output).outputs, report.outputs)


if __name__ == "__main__":
    unittest.main()
