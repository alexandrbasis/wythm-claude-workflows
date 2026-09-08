import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

from tests import test_plugins as plugin_fixtures


_SPEC = importlib.util.spec_from_file_location(
    "claudops_snapshot", Path(__file__).resolve().parents[1] / "packaging" / "update_snapshot.py"
)
snapshot = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(snapshot)


class MarketplaceSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.fixture = plugin_fixtures.PluginBuildTests("test_builds_both_layouts_and_aliases")
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.root = self.fixture.root
        self.catalog_path = self.root / ".claude-plugin" / "marketplace.json"
        self.catalog = {
            "name": "claudops",
            "owner": {"name": "Alex Basis"},
            "plugins": [{"name": "claudops", "source": "./plugins/claudops"}],
        }
        self.catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")
        self.target = self.root / "plugins" / "claudops"
        self.portable_target = self.root / "plugins" / "claudops-agent"
        self.codex_catalog_path = self.root / ".agents" / "plugins" / "marketplace.json"
        self.codex_catalog_path.parent.mkdir(parents=True)
        self.codex_catalog = {
            "name": "claudops",
            "plugins": [{
                "name": "claudops",
                "source": {"source": "local", "path": "./plugins/claudops-agent"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity",
            }],
        }
        self.codex_catalog_path.write_text(json.dumps(self.codex_catalog), encoding="utf-8")

    def set_versions(self, claude, portable=None):
        for relative, version in ((".claude-plugin/plugin.json", claude),
                                  ("plugin.json", portable if portable is not None else claude)):
            path = self.root / relative
            manifest = json.loads(path.read_text())
            manifest["version"] = version
            path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_source_version_is_published_and_remains_current(self):
        self.set_versions("1.2.3")
        result = snapshot.update_snapshot(self.root)
        installed = json.loads((self.target / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(installed["version"], "1.2.3")
        portable = json.loads((self.portable_target / "plugin.json").read_text())
        self.assertEqual(portable["version"], "1.2.3")
        self.assertEqual(result["version"], "1.2.3")
        self.assertEqual(snapshot.update_snapshot(self.root, check_only=True)["status"], "current")

    def test_default_development_build_uses_matching_source_version(self):
        self.set_versions("1.2.3")
        output = self.root / "development-build"
        snapshot.build(self.root / ".claude", output)
        for kind, relative in (("claude", ".claude-plugin/plugin.json"), ("agent", "plugin.json")):
            manifest = json.loads((output / kind / "claudops" / relative).read_text())
            self.assertEqual(manifest["version"], "1.2.3")
        snapshot.check(self.root / ".claude", output)
        self.set_versions("1.2.3", "1.2.4")
        with self.assertRaisesRegex(ValueError, "versions differ"):
            snapshot.build(self.root / ".claude", output)

    def test_later_source_version_makes_previous_snapshot_stale(self):
        snapshot.update_snapshot(self.root)
        self.set_versions("1.1.0")
        with self.assertRaisesRegex(ValueError, "missing or stale"):
            snapshot.update_snapshot(self.root, check_only=True)
        installed = json.loads((self.target / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(installed["version"], "1.0.0")

    def test_mismatched_source_versions_preserve_existing_snapshot(self):
        snapshot.update_snapshot(self.root)
        before = snapshot._artifact_snapshot(self.target)
        self.set_versions("1.1.0", "1.0.0")
        with self.assertRaisesRegex(ValueError, "versions differ"):
            snapshot.update_snapshot(self.root)
        self.assertEqual(snapshot._artifact_snapshot(self.target), before)

    def test_catalog_errors_fail_even_when_package_is_current(self):
        snapshot.update_snapshot(self.root)
        before = snapshot._artifact_snapshot(self.target)
        cases = [
            "{ invalid JSON",
            json.dumps({**self.catalog, "name": "different-marketplace"}),
            json.dumps({**self.catalog, "owner": {}}),
            json.dumps({**self.catalog, "plugins": []}),
            json.dumps({**self.catalog, "plugins": [{"name": "wrong", "source": "./plugins/claudops"}]}),
            json.dumps({**self.catalog, "plugins": [{"name": "claudops", "source": "../outside"}]}),
            json.dumps({**self.catalog, "plugins": [{"name": "claudops", "source": "./missing"}]}),
            json.dumps({**self.catalog, "plugins": [{**self.catalog["plugins"][0], "version": "9.0.0"}]}),
        ]
        for text in cases:
            with self.subTest(catalog=text):
                self.catalog_path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    snapshot.update_snapshot(self.root, check_only=True)
                self.assertEqual(snapshot._artifact_snapshot(self.target), before)

    def test_failed_staging_copy_preserves_previous_snapshot(self):
        snapshot.update_snapshot(self.root)
        before = snapshot._artifact_snapshot(self.target)
        self.set_versions("1.1.0")
        with mock.patch.object(snapshot.shutil, "copytree", side_effect=OSError("copy failed")):
            with self.assertRaisesRegex(OSError, "copy failed"):
                snapshot.update_snapshot(self.root)
        self.assertEqual(snapshot._artifact_snapshot(self.target), before)

    def test_failed_second_promotion_restores_both_previous_snapshots(self):
        snapshot.update_snapshot(self.root)
        before = {target: snapshot._artifact_snapshot(target)
                  for target in (self.target, self.portable_target)}
        self.set_versions("1.1.0")
        original_rename = Path.rename

        def fail_portable_promotion(path, destination):
            if path.name == "new" and path.parent.name == "agent":
                raise OSError("portable promotion failed")
            return original_rename(path, destination)

        with mock.patch.object(Path, "rename", fail_portable_promotion):
            with self.assertRaisesRegex(OSError, "portable promotion failed"):
                snapshot.update_snapshot(self.root)
        for target, previous in before.items():
            self.assertEqual(snapshot._artifact_snapshot(target), previous)
        self.assertEqual(list((self.root / "plugins").glob(".claudops-snapshot-*")), [])

    def test_portable_drift_fails_check_without_modifying_claude(self):
        snapshot.update_snapshot(self.root)
        before = snapshot._artifact_snapshot(self.target)
        (self.portable_target / "skills" / "quick" / "SKILL.md").write_text("stale skill\n")
        with self.assertRaisesRegex(ValueError, "claudops-agent is missing or stale"):
            snapshot.update_snapshot(self.root, check_only=True)
        self.assertEqual(snapshot._artifact_snapshot(self.target), before)
        snapshot.update_snapshot(self.root)
        self.assertEqual(snapshot.update_snapshot(self.root, check_only=True)["status"], "current")
        self.assertEqual(snapshot._artifact_snapshot(self.target), before)

    def test_codex_catalog_errors_fail_before_replacing_either_package(self):
        snapshot.update_snapshot(self.root)
        before = {target: snapshot._artifact_snapshot(target)
                  for target in (self.target, self.portable_target)}
        entry = self.codex_catalog["plugins"][0]
        cases = [
            "{ invalid JSON",
            json.dumps({**self.codex_catalog, "name": "different-marketplace"}),
            json.dumps({**self.codex_catalog, "plugins": []}),
        ]
        for changes in ({"name": "wrong"}, {"source": "./plugins/claudops-agent"},
                        {"source": {"source": "local", "path": "../outside"}},
                        {"source": {"source": "local", "path": "./plugins/claudops"}},
                        {"policy": {}}, {"category": ""}):
            cases.append(json.dumps({**self.codex_catalog, "plugins": [{**entry, **changes}]}))
        self.set_versions("1.1.0")
        for text in cases:
            with self.subTest(catalog=text):
                self.codex_catalog_path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    snapshot.update_snapshot(self.root)
                for target, previous in before.items():
                    self.assertEqual(snapshot._artifact_snapshot(target), previous)


if __name__ == "__main__":
    unittest.main()
