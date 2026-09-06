#!/usr/bin/env python3
"""Validate generated Claudops artifacts before distribution."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import jsonschema

try:  # Works both as ``python scripts/validate_plugins.py`` and as a package import.
    from .build_plugins import (
        POINTER_MARKER,
        PLUGIN_NAME,
        _parse_frontmatter,
        _read_agents,
        _read_skills,
        _source_fingerprint,
    )
except ImportError:  # pragma: no cover - exercised by the CLI entry point.
    from build_plugins import (
        POINTER_MARKER,
        PLUGIN_NAME,
        _parse_frontmatter,
        _read_agents,
        _read_skills,
        _source_fingerprint,
    )


ROOT_FORBIDDEN = {"hooks", "mcp.json", ".mcp.json", "settings.json", "monitors"}
PORTABLE_SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|rk)-[A-Za-z0-9]{24,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def _schema_path(name: str) -> Path:
    return Path(__file__).resolve().parents[1] / "packaging" / "schemas" / name


def _error(errors: list[str], message: str) -> None:
    errors.append(message)


def _check_containment(root: Path, errors: list[str]) -> None:
    resolved_root = root.resolve()
    for path in root.rglob("*"):
        if not path.is_symlink():
            continue
        try:
            path.resolve().relative_to(resolved_root)
        except ValueError:
            _error(errors, f"symlink escapes artifact root: {path.relative_to(root)} -> {path.resolve()}")


def _check_artifact_ancestry(root: Path, errors: list[str]) -> None:
    current = root
    # Artifact paths produced by the builder are output/{claude,agent}/claudops.
    # Inspect only those components so ordinary macOS /var and /tmp aliases do not
    # become false positives while symlinked output descendants remain visible.
    for _ in range(3):
        if current.is_symlink():
            _error(errors, f"artifact path contains symlinked ancestor: {current}")
        current = current.parent


def _check_secrets(root: Path, errors: list[str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                _error(errors, f"secret-like value in generated artifact: {path.relative_to(root)}")
                break


def _validate_manifest(path: Path, kind: str, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        _error(errors, f"missing {kind} manifest: {path}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _error(errors, f"invalid JSON in {path}: {exc}")
        return None
    if kind == "agent":
        schema = json.loads(_schema_path("plugin.schema.json").read_text(encoding="utf-8"))
        try:
            jsonschema.Draft202012Validator(schema).validate(data)
        except jsonschema.ValidationError as exc:
            _error(errors, f"portable manifest schema error: {exc.message}")
    else:
        if data.get("name") != PLUGIN_NAME:
            _error(errors, f"Claude manifest name must be {PLUGIN_NAME!r}")
        if not isinstance(data.get("version"), str) or not data.get("version"):
            _error(errors, "Claude manifest version must be a non-empty string")
    return data if isinstance(data, dict) else None


def _validate_skills(root: Path, source_root: Path, kind: str, errors: list[str]) -> tuple[str, ...]:
    try:
        source_skills = _read_skills(source_root)
    except (OSError, ValueError) as exc:
        _error(errors, str(exc))
        return ()
    expected = {skill.output_name: skill for skill in source_skills}
    skills_root = root / "skills"
    if not skills_root.is_dir():
        _error(errors, f"missing skills directory: {skills_root}")
        return tuple(sorted(expected))
    actual = {path.name: path for path in skills_root.iterdir() if path.is_dir()}
    if set(actual) != set(expected):
        _error(errors, f"skill set mismatch: expected={sorted(expected)} actual={sorted(actual)}")
    for name, source in expected.items():
        skill_file = actual.get(name, Path()) / "SKILL.md"
        if not skill_file.is_file():
            _error(errors, f"missing bundled skill file: skills/{name}/SKILL.md")
            continue
        try:
            frontmatter, body = _parse_frontmatter(skill_file)
        except (OSError, ValueError) as exc:
            _error(errors, str(exc))
            continue
        if frontmatter.get("name") != name:
            _error(errors, f"skill folder/frontmatter mismatch: skills/{name} has name={frontmatter.get('name')!r}")
        if not isinstance(frontmatter.get("description"), str) or not frontmatter["description"].strip():
            _error(errors, f"skill {name} has no description")
        if len(name) > 64 or not SKILL_NAME_PATTERN.fullmatch(name):
            _error(errors, f"skill {name!r} violates portable naming rules")
        if len(str(frontmatter.get("description", ""))) > 1024:
            _error(errors, f"skill {name} description exceeds 1024 characters")
        if "compatibility" in frontmatter and len(str(frontmatter["compatibility"])) > 500:
            _error(errors, f"skill {name} compatibility exceeds 500 characters")
        if kind == "agent":
            unknown = sorted(set(frontmatter) - PORTABLE_SKILL_FIELDS)
            if unknown:
                _error(errors, f"portable skill {name} has unsupported frontmatter: {unknown}")
            if "allowed-tools" in frontmatter and not isinstance(frontmatter["allowed-tools"], str):
                _error(errors, f"portable skill {name} allowed-tools must be a string")
            metadata = frontmatter.get("metadata")
            if metadata is not None:
                if not isinstance(metadata, dict) or any(not isinstance(value, str) for value in metadata.values()):
                    _error(errors, f"portable skill {name} metadata values must be strings")
            if source.frontmatter.get("disable-model-invocation") is True:
                if not isinstance(metadata, dict) or not metadata.get("invocation_guard"):
                    _error(errors, f"portable skill {name} lost its explicit invocation guard metadata")
        elif kind == "claude":
            for key, value in source.frontmatter.items():
                if frontmatter.get(key) != value:
                    _error(errors, f"Claude skill {name} lost frontmatter field: {key}")
        if kind == "agent" and name != "setup":
            if POINTER_MARKER not in body:
                _error(errors, f"skill {name} is missing project configuration pointer")
        if kind == "agent" and name == "setup" and POINTER_MARKER in body:
            _error(errors, "setup skill must use its bundled body without a redirect pointer")
    return tuple(sorted(expected))


def _validate_agents(root: Path, source_root: Path, errors: list[str]) -> tuple[str, ...]:
    try:
        source_agents = _read_agents(source_root)
    except (OSError, ValueError) as exc:
        _error(errors, str(exc))
        return ()
    expected = {str(frontmatter.get("name", source.stem)) for source, frontmatter, _ in source_agents}
    known_skills = {skill.output_name for skill in _read_skills(source_root)}
    actual = {path.stem for path in (root / "agents").glob("*.md")} if (root / "agents").is_dir() else set()
    if actual != expected:
        _error(errors, f"agent set mismatch: expected={sorted(expected)} actual={sorted(actual)}")
    source_by_name = {str(frontmatter.get("name", source.stem)): frontmatter for source, frontmatter, _ in source_agents}
    for name in expected:
        path = root / "agents" / f"{name}.md"
        if not path.is_file():
            continue
        try:
            frontmatter, _ = _parse_frontmatter(path)
        except (OSError, ValueError) as exc:
            _error(errors, str(exc))
            continue
        if frontmatter.get("name") != name:
            _error(errors, f"agent filename/frontmatter mismatch: {path.name}")
        source_frontmatter = source_by_name[name]
        for key in source_frontmatter:
            if key == "skills":
                continue
            if frontmatter.get(key) != source_frontmatter[key]:
                _error(errors, f"agent {name} lost frontmatter field: {key}")
        dependencies = frontmatter.get("skills", [])
        dependency_values = dependencies if isinstance(dependencies, list) else [dependencies]
        for dependency in dependency_values:
            if isinstance(dependency, str) and dependency in known_skills:
                _error(errors, f"agent {name} has unqualified plugin skill dependency: {dependency}")
    return tuple(sorted(expected))


def _validate_runtime_boundary(root: Path, errors: list[str]) -> None:
    for child in root.iterdir():
        if child.name in ROOT_FORBIDDEN:
            _error(errors, f"runtime state/config must not be at artifact root: {child.name}")
    build_manifest = root / ".build-manifest.json"
    if not build_manifest.is_file():
        _error(errors, "missing .build-manifest.json")


def validate_artifact(root: Path, kind: str, source_root: Path | None = None) -> list[str]:
    root = root.absolute()
    errors: list[str] = []
    _check_artifact_ancestry(root, errors)
    if not root.is_dir():
        return [f"artifact directory does not exist: {root}"]
    source_root = (source_root or root.parents[2] / ".claude").resolve()
    _check_containment(root, errors)
    _check_secrets(root, errors)
    _validate_manifest(root / ("plugin.json" if kind == "agent" else ".claude-plugin/plugin.json"), kind, errors)
    _validate_skills(root, source_root, kind, errors)
    if kind == "claude":
        _validate_agents(root, source_root, errors)
    _validate_runtime_boundary(root, errors)
    build_manifest_path = root / ".build-manifest.json"
    if build_manifest_path.is_file():
        try:
            build_manifest = json.loads(build_manifest_path.read_text(encoding="utf-8"))
            if build_manifest.get("artifact") != kind:
                _error(errors, f"build manifest artifact mismatch: {build_manifest.get('artifact')!r}")
            expected_fingerprint = _source_fingerprint(source_root)
            if build_manifest.get("source_fingerprint") != expected_fingerprint:
                _error(errors, "generated artifact is stale relative to the maintained .claude source")
        except (OSError, json.JSONDecodeError) as exc:
            _error(errors, f"invalid build manifest: {exc}")
    return errors


def validate_outputs(output_root: Path, source_root: Path) -> dict[str, list[str]]:
    return {
        "claude": validate_artifact(output_root / "claude" / PLUGIN_NAME, "claude", source_root),
        "agent": validate_artifact(output_root / "agent" / PLUGIN_NAME, "agent", source_root),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo_root = Path(__file__).resolve().parents[1]
    parser.add_argument("--source", type=Path, default=repo_root / ".claude")
    parser.add_argument("--out", type=Path, default=repo_root / "dist")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = validate_outputs(args.out.absolute(), args.source.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        for kind, errors in result.items():
            print(f"{kind}: {'PASS' if not errors else 'FAIL'}")
            for error in errors:
                print(f"  - {error}")
    return 1 if any(result.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
