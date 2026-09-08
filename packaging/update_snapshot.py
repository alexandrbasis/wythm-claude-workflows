#!/usr/bin/env python3
"""Refresh or check the generated Claude package used by the local marketplace."""

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

from build_plugins import _artifact_snapshot, build, check
from validate_plugins import validate_artifact, validate_outputs


def _read_object(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}.")
    return value


def _source_version(repository: Path) -> str:
    versions = [_read_object(repository / path).get("version") for path in
                (".claude-plugin/plugin.json", "plugin.json")]
    if any(not isinstance(version, str) or not version.strip() for version in versions):
        raise ValueError("Both source manifests must declare a nonempty version.")
    if versions[0] != versions[1]:
        raise ValueError(f"Source manifest versions differ: {versions!r}.")
    return versions[0]


def _validate_catalog(repository: Path, target: Path, version: str) -> None:
    catalog = _read_object(repository / ".claude-plugin" / "marketplace.json")
    if catalog.get("name") != "claudops":
        raise ValueError("Marketplace name must be claudops.")
    owner = catalog.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str) or not owner["name"].strip():
        raise ValueError("Marketplace owner.name must be a nonempty string.")
    entries = catalog.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        raise ValueError("Marketplace must contain exactly one Claudops plugin entry.")
    entry = entries[0]
    if entry.get("name") != "claudops" or entry.get("source") != "./plugins/claudops":
        raise ValueError("Marketplace entry must name claudops with source ./plugins/claudops.")
    if (repository / entry["source"]).resolve() != target:
        raise ValueError("Marketplace source must resolve to the repository's plugins/claudops directory.")
    if entry.get("version", version) != version:
        raise ValueError("Marketplace entry version must match the source manifests.")


def _replace_snapshot(generated: Path, target: Path, source: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".claudops-snapshot-", dir=target.parent))
    replacement, previous = staging / "new", staging / "previous"
    promoted = False
    try:
        shutil.copytree(generated, replacement)
        errors = validate_artifact(replacement, "claude", source)
        if errors or _artifact_snapshot(replacement) != _artifact_snapshot(generated):
            raise ValueError(f"Staged snapshot validation failed: {errors!r}.")
        if target.exists():
            target.rename(previous)
        try:
            replacement.rename(target)
            promoted = True
        except BaseException:
            if previous.exists():
                try:
                    previous.rename(target)
                except OSError as error:
                    raise ValueError(f"Snapshot replacement failed; previous package preserved at {previous}.") from error
            raise
    finally:
        if promoted or not previous.exists():
            shutil.rmtree(staging)


def update_snapshot(repository: Path, *, check_only: bool = False) -> dict:
    repository = repository.resolve()
    source = repository / ".claude"
    target = repository / "plugins" / "claudops"
    if target.parent.is_symlink() or target.is_symlink():
        raise ValueError("Refusing a symlink at the snapshot destination.")
    version = _source_version(repository)
    _validate_catalog(repository, target, version)
    if target.exists():
        marker = target / ".build-manifest.json"
        if marker.is_symlink() or not marker.is_file():
            raise ValueError("Refusing to replace a directory without a regular build manifest.")
        identity = _read_object(marker)
        if identity.get("plugin") != "claudops" or identity.get("artifact") != "claude":
            raise ValueError("Refusing to replace a different package.")

    with tempfile.TemporaryDirectory(prefix="claudops-snapshot-") as temporary:
        output = Path(temporary) / "dist"
        report = build(source, output, version=version)
        failures = validate_outputs(output, source)
        if any(failures.values()):
            raise ValueError(json.dumps(failures, indent=2))
        check(source, output, version=version)
        generated = output / "claude" / "claudops"
        if check_only:
            if not target.is_dir() or _artifact_snapshot(target) != _artifact_snapshot(generated):
                raise ValueError("Snapshot is missing or stale; run packaging/update_snapshot.py.")
        else:
            _replace_snapshot(generated, target, source)
        errors = validate_artifact(target, "claude", source)
        if errors:
            raise ValueError("\n".join(errors))
        return {"snapshot": "plugins/claudops", "status": "current" if check_only else "updated",
                "version": version, "skills": len(report.skill_names), "agents": len(report.agent_names)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the tracked snapshot is stale")
    args = parser.parse_args()
    try:
        result = update_snapshot(REPOSITORY, check_only=args.check)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
    print(json.dumps(result))


if __name__ == "__main__":
    main()
