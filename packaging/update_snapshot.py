#!/usr/bin/env python3
"""Refresh or check the generated Claude and portable marketplace packages."""

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

from build_plugins import _artifact_snapshot, build, check, source_version
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
    return source_version(repository / ".claude")


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


def _validate_codex_catalog(repository: Path, target: Path) -> None:
    catalog = _read_object(repository / ".agents" / "plugins" / "marketplace.json")
    if catalog.get("name") != "claudops":
        raise ValueError("Codex marketplace name must be claudops.")
    entries = catalog.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        raise ValueError("Codex marketplace must contain exactly one Claudops plugin entry.")
    entry = entries[0]
    expected_source = {"source": "local", "path": "./plugins/claudops-agent"}
    if entry.get("name") != "claudops" or entry.get("source") != expected_source:
        raise ValueError("Codex marketplace entry must name claudops with local source ./plugins/claudops-agent.")
    if (repository / entry["source"]["path"]).resolve() != target:
        raise ValueError("Codex marketplace source must resolve to plugins/claudops-agent.")
    if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        raise ValueError("Codex marketplace must make the plugin AVAILABLE with ON_INSTALL authentication.")
    if entry.get("category") != "Productivity":
        raise ValueError("Codex marketplace category must be Productivity.")


def _replace_snapshots(generated: dict[str, Path], targets: dict[str, Path], source: Path) -> None:
    parent = next(iter(targets.values())).parent
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".claudops-snapshot-", dir=parent))
    promoted = []
    rollback_errors = []
    try:
        # Finish every copy and validation before changing either published tree.
        for kind, artifact in generated.items():
            replacement = staging / kind / "new"
            replacement.parent.mkdir()
            shutil.copytree(artifact, replacement)
            errors = validate_artifact(replacement, kind, source)
            if errors or _artifact_snapshot(replacement) != _artifact_snapshot(artifact):
                raise ValueError(f"Staged {kind} snapshot validation failed: {errors!r}.")
        for kind, target in targets.items():
            previous = staging / kind / "previous"
            if target.exists():
                target.rename(previous)
            (staging / kind / "new").rename(target)
            promoted.append(kind)
    except BaseException:
        for kind, target in reversed(list(targets.items())):
            previous = staging / kind / "previous"
            try:
                if kind in promoted:
                    shutil.rmtree(target)
                if previous.exists():
                    previous.rename(target)
            except OSError as error:
                rollback_errors.append(f"{target}: {error}")
        if rollback_errors:
            raise ValueError(f"Snapshot rollback failed; backups preserved at {staging}: {rollback_errors!r}.")
        raise
    finally:
        if not rollback_errors:
            shutil.rmtree(staging)


def update_snapshot(repository: Path, *, check_only: bool = False) -> dict:
    repository = repository.resolve()
    source = repository / ".claude"
    targets = {"claude": repository / "plugins" / "claudops",
               "agent": repository / "plugins" / "claudops-agent"}
    for target in targets.values():
        if target.parent.is_symlink() or target.is_symlink():
            raise ValueError("Refusing a symlink at the snapshot destination.")
    version = _source_version(repository)
    _validate_catalog(repository, targets["claude"], version)
    _validate_codex_catalog(repository, targets["agent"])
    for kind, target in targets.items():
        if target.exists():
            marker = target / ".build-manifest.json"
            if marker.is_symlink() or not marker.is_file():
                raise ValueError("Refusing to replace a directory without a regular build manifest.")
            identity = _read_object(marker)
            if identity.get("plugin") != "claudops" or identity.get("artifact") != kind:
                raise ValueError("Refusing to replace a different package.")

    with tempfile.TemporaryDirectory(prefix="claudops-snapshot-") as temporary:
        output = Path(temporary) / "dist"
        report = build(source, output, version=version)
        failures = validate_outputs(output, source)
        if any(failures.values()):
            raise ValueError(json.dumps(failures, indent=2))
        check(source, output, version=version)
        generated = {kind: output / kind / "claudops" for kind in targets}
        stale = [kind for kind, target in targets.items()
                 if not target.is_dir() or _artifact_snapshot(target) != _artifact_snapshot(generated[kind])]
        if check_only and stale:
            paths = ", ".join(str(targets[kind].relative_to(repository)) for kind in stale)
            raise ValueError(f"Snapshot {paths} is missing or stale; run packaging/update_snapshot.py.")
        if not check_only and stale:
            _replace_snapshots({kind: generated[kind] for kind in stale},
                               {kind: targets[kind] for kind in stale}, source)
        for kind, target in targets.items():
            errors = validate_artifact(target, kind, source)
            if errors:
                raise ValueError("\n".join(errors))
        return {"snapshots": [str(target.relative_to(repository)) for target in targets.values()],
                "status": "current" if check_only else "updated",
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
