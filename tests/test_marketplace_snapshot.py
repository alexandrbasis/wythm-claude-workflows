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
        self.assertEqual(result["version"], "1.2.3")
        self.assertEqual(snapshot.update_snapshot(self.root, check_only=True)["status"], "current")

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
        with mock.patch.object(snapshot.shutil, "copytree", side_effect=OSError("copy failed")):
            with self.assertRaisesRegex(OSError, "copy failed"):
                snapshot.update_snapshot(self.root)
        self.assertEqual(snapshot._artifact_snapshot(self.target), before)


if __name__ == "__main__":
    unittest.main()
