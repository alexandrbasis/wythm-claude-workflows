"""Exercise setup's project boundary using disposable source and target trees."""

import importlib.util
from contextlib import chdir
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / ".claude/skills/setup/scripts/bootstrap_project.py"
spec = importlib.util.spec_from_file_location("bootstrap_project", SCRIPT)
bootstrap_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap_project)


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "plugin" / ".claude"
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        self.file("skills/example/SKILL.md", "template")
        self.file("skills/example/assets/example.json", "{}")
        self.file("hooks/guard.sh", "#!/bin/sh\nexit 0\n")

    def file(self, relative, content):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_preview_does_not_write_and_apply_preserves_custom_files(self):
        existing = self.project / ".claude/skills/example/SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("project customizations")
        before = sorted(self.project.rglob("*"))
        preview = bootstrap_project.bootstrap(self.source, self.project)
        self.assertEqual(before, sorted(self.project.rglob("*")))
        self.assertIn(".claude/skills/example/SKILL.md", preview["preserved"])
        applied = bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertEqual(existing.read_text(), "project customizations")
        self.assertEqual(applied["add"], applied["written"])
        self.assertTrue((self.project / ".claude/skills/example/assets/example.json").is_file())
        self.assertEqual(bootstrap_project.bootstrap(self.source, self.project, True)["written"], [])

    def test_settings_secrets_runtime_and_recursive_bundle_are_excluded(self):
        for name in ["settings.json", "settings.local.json", "mcp/auth.json", "hooks/logs/private.jsonl",
                     "skills/example/config.local.json", "skills/example/__pycache__/helper.pyc",
                     "skills/example/.env", "skills/example/.env.production",
                     "skills/update-setup/claudops-upstream.lock.json",
                     "skills/setup/assets/workflow/.claude/skills/nested/SKILL.md"]:
            self.file(name, "must stay in source")
        result = bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertEqual(len(result["written"]), 3)
        self.assertFalse(result["settings_changed"])
        self.assertFalse((self.project / ".claude/settings.json").exists())

    def test_disabled_local_skill_is_not_reenabled(self):
        disabled = self.project / ".claude/skills/example/SKILL.md.disabled"
        disabled.parent.mkdir(parents=True)
        disabled.write_text("disabled customization")
        result = bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertIn(".claude/skills/example/SKILL.md.disabled", result["preserved"])
        self.assertFalse(disabled.with_name("SKILL.md").exists())
        self.assertEqual(disabled.read_text(), "disabled customization")

    def test_destination_symlink_is_rejected_before_any_write(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".claude").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_source_symlink_is_rejected_before_any_write(self):
        (self.source / "skills/alias").symlink_to(self.source / "skills/example", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertFalse((self.project / ".claude").exists())

    def test_file_instead_of_parent_is_rejected_before_any_write(self):
        (self.project / ".claude").write_text("existing user file")
        with self.assertRaisesRegex(ValueError, "not a directory"):
            bootstrap_project.bootstrap(self.source, self.project, True)
        self.assertEqual((self.project / ".claude").read_text(), "existing user file")

    def test_source_install_cannot_copy_onto_itself(self):
        with self.assertRaisesRegex(ValueError, "separate"):
            bootstrap_project.bootstrap(self.source, self.source.parent, True)

    def test_project_scoped_plugin_can_materialize_sibling_project_files(self):
        source = self.project / ".claude/skills/claudops/skills/setup/assets/workflow/.claude"
        path = source / "skills/example/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("template")
        bootstrap_project.bootstrap(source, self.project, True)
        self.assertEqual((self.project / ".claude/skills/example/SKILL.md").read_text(), "template")

    def test_template_root_uses_source_or_bundle_independently_of_consuming_cwd(self):
        source_script = self.source / "skills/setup/scripts/bootstrap_project.py"
        source_script.parent.mkdir(parents=True)
        source_script.write_text("# source fixture\n")
        bundled_setup = self.root / "package/skills/setup"
        bundled_script = bundled_setup / "scripts/bootstrap_project.py"
        bundled_script.parent.mkdir(parents=True)
        bundled_script.write_text("# package fixture\n")
        bundled_source = bundled_setup / "assets/workflow/.claude"
        bundled_source.mkdir(parents=True)
        for script, expected in ((source_script, self.source), (bundled_script, bundled_source)):
            with self.subTest(script=script), chdir(self.project):
                with patch.object(bootstrap_project, "__file__", str(script)):
                    self.assertEqual(bootstrap_project.template_root(), expected.resolve())
        self.assertFalse((self.project / ".claude").exists())


if __name__ == "__main__":
    unittest.main()
