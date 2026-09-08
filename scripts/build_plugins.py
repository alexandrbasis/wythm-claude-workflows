#!/usr/bin/env python3
"""Build self-contained Claude Code and Agent Plugins artifacts.

The repository keeps the maintained workflow under ``.claude``.  This builder
turns that source into two deterministic packages:

* ``dist/claude/claudops``: Claude's manifest, skills, and flattened agents.
* ``dist/agent/claudops``: the portable Agent Plugins manifest and skills.

The source tree is never modified.  Project-specific configuration is copied
only into the setup skill's bundled bootstrap templates; hooks, settings, MCP
configuration, and runtime logs are deliberately excluded from package roots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


BUILD_FORMAT = 1
PLUGIN_NAME = "claudops"
SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".toml",
    ".js",
    ".ts",
    ".xml",
}
POINTER_MARKER = "<!-- claudops-build: project-config-pointer -->"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RUNTIME_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "logs",
    "cache",
    "caches",
    "history",
    "file-history",
    "todos",
    "debug",
    ".state",
    "mcp",
}
RUNTIME_FILE_NAMES = {
    ".mcp.json",
    "mcp.json",
    "settings.json",
    "history.jsonl",
    "session-env",
}


@dataclass(frozen=True)
class SkillSource:
    source_dir: str
    output_name: str
    directory: Path
    frontmatter: dict[str, Any]
    body: str


@dataclass(frozen=True)
class BuildReport:
    source_root: Path
    outputs: tuple[Path, Path]
    skill_names: tuple[str, ...]
    agent_names: tuple[str, ...]
    source_fingerprint: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _validate_component_name(value: Any, kind: str, path: Path) -> str:
    if not isinstance(value, str) or not value or len(value) > 64 or not NAME_PATTERN.fullmatch(value):
        raise ValueError(
            f"{path}: {kind} name must be a lower-case alphanumeric name with single hyphens, max 64 characters: {value!r}"
        )
    return value


def _parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: frontmatter must begin on the first line")
    match = re.search(r"^---\s*$", text[4:], flags=re.MULTILINE)
    if match is None:
        raise ValueError(f"{path}: closing frontmatter delimiter is missing")
    end = 4 + match.end()
    raw = text[4 : 4 + match.start()]
    frontmatter = yaml.safe_load(raw) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    body = text[end:]
    if body.startswith("\n"):
        body = body[1:]
    return frontmatter, body


def _render_document(frontmatter: dict[str, Any], body: str) -> str:
    header = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=120,
    ).rstrip()
    return f"---\n{header}\n---\n\n{body.lstrip(chr(10))}"


def _stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def _normalize_allowed_tools(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(_stringify(item) for item in value)
    text = _stringify(value).strip()
    chunks: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            chunks.append(text[start:index].strip())
            start = index + 1
    chunks.append(text[start:].strip())
    return " ".join(chunk for chunk in chunks if chunk)


def _metadata_key(prefix: str, key: str, used: set[str]) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_") or "field"
    candidate = f"{prefix}{base}"
    index = 2
    while candidate in used:
        candidate = f"{prefix}{base}_{index}"
        index += 1
    used.add(candidate)
    return candidate


def _portable_frontmatter(source: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("name", "description", "license"):
        if key in source:
            result[key] = source[key]

    allowed_tools = source.get("allowed-tools")
    if allowed_tools is not None:
        result["allowed-tools"] = _normalize_allowed_tools(allowed_tools)

    metadata: dict[str, str] = {}
    source_metadata = source.get("metadata")
    if source_metadata is not None and not isinstance(source_metadata, dict):
        raise ValueError("portable skill metadata must be a mapping")
    if isinstance(source_metadata, dict):
        used: set[str] = set()
        for key, value in source_metadata.items():
            key_text = str(key)
            if key_text in used:
                key_text = _metadata_key("source_", key_text, used)
            else:
                used.add(key_text)
            metadata[key_text] = _stringify(value)

    used = set(metadata)
    for key, value in source.items():
        if key in SKILL_FIELDS:
            continue
        metadata[_metadata_key("claude_", str(key), used)] = _stringify(value)

    explicit_only = source.get("disable-model-invocation") is True
    if explicit_only:
        metadata[_metadata_key("", "invocation_guard", used)] = (
            "explicit-only; portable clients may not enforce Claude Code host-level invocation restrictions"
        )

    if metadata:
        result["metadata"] = metadata

    compatibility = source.get("compatibility")
    limitation = "Portable clients may not enforce Claude Code invocation guards or project setup behavior."
    if compatibility:
        if limitation not in str(compatibility):
            compatibility = f"{compatibility} {limitation}"
        if len(str(compatibility)) > 500:
            raise ValueError("portable skill compatibility exceeds the 500-character limit")
        result["compatibility"] = str(compatibility)
    else:
        result["compatibility"] = limitation

    description = str(result.get("description", "")).strip()
    if explicit_only:
        guard = " Use as a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients may not enforce this host-level restriction."
        if guard.strip() not in description:
            description = f"{description}{guard}".strip()
    if len(description) > 1024:
        raise ValueError("portable skill description exceeds the 1024-character limit")
    result["description"] = description
    return result


def _alias_map(skills: Iterable[SkillSource]) -> dict[str, str]:
    return {skill.source_dir: skill.output_name for skill in skills if skill.source_dir != skill.output_name}


def _rewrite_aliases(text: str, aliases: dict[str, str]) -> str:
    """Rewrite invocations and plugin-relative paths, preserving project source paths."""

    for source, target in sorted(aliases.items(), key=lambda item: -len(item[0])):
        # A project path intentionally keeps its source directory name: setup
        # materializes that path in the consuming repository.
        text = re.sub(
            rf"(?<!/skills)/{re.escape(source)}(?=$|[\s,.)`])",
            f"/{target}",
            text,
        )
        text = re.sub(
            rf"(?<!\.claude/)skills/{re.escape(source)}(?=$|[/\s,.)`])",
            f"skills/{target}",
            text,
        )
        text = re.sub(
            rf"\.\./{re.escape(source)}(?=$|[/\s,.)`])",
            f"../{target}",
            text,
        )
    return text


def _pointer(source_dir: str, explicit_only: bool) -> str:
    lines = [
        POINTER_MARKER,
        f"> If `.claude/skills/{source_dir}/SKILL.md.disabled` exists, stop before reading a fallback.",
        f"> **Project configuration:** If the current project contains `.claude/skills/{source_dir}/SKILL.md`, read and apply it instead of this bundled default. The project copy is the capability source of truth.",
        "> **Repository context:** Read `../setup/references/task-context.md` when resolving a task, project commands, named agent roles, or legacy `.claude/` resource paths. Use repository evidence and applicable project instructions; a missing local workflow copy does not require setup. Resolve bundled resources from the installed skill, never from the target cwd.",
    ]
    if explicit_only:
        lines.append("> **Invocation guard:** use this as a standalone skill only when explicitly requested by the user; automatic selection is not authorization. Portable clients may not enforce Claude Code host-level invocation restrictions.")
    return "\n".join(lines) + "\n\n"


def _read_skills(source_root: Path) -> list[SkillSource]:
    skills_root = source_root / "skills"
    if not skills_root.is_dir():
        raise ValueError(f"missing skills directory: {skills_root}")
    found: list[SkillSource] = []
    names: set[str] = set()
    for directory in sorted(skills_root.iterdir()):
        skill_file = directory / "SKILL.md"
        if not directory.is_dir() or not skill_file.is_file():
            continue
        frontmatter, body = _parse_frontmatter(skill_file)
        name = _validate_component_name(frontmatter.get("name", directory.name), "skill", skill_file)
        if name in names:
            raise ValueError(f"duplicate skill name: {name}")
        names.add(name)
        found.append(SkillSource(directory.name, name, directory, frontmatter, body))
    if not found:
        raise ValueError(f"no skills found under {skills_root}")
    return found


def _copy_text_or_binary(source: Path, destination: Path, aliases: dict[str, str]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() in TEXT_SUFFIXES:
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(source, destination)
            shutil.copymode(source, destination)
            return
        destination.write_text(_rewrite_aliases(content, aliases), encoding="utf-8")
        shutil.copymode(source, destination)
    else:
        shutil.copy2(source, destination)
        shutil.copymode(source, destination)


def _should_exclude_path(relative: Path) -> bool:
    parts = relative.parts
    name = relative.name
    if any(part in RUNTIME_DIR_NAMES for part in parts):
        return True
    if name in RUNTIME_FILE_NAMES:
        return True
    if name.startswith(".env") or name.endswith((".lock", ".lock.json")):
        return True
    if name.endswith((".pem", ".key", ".p12", ".pfx")):
        return True
    if name == ".DS_Store" or name.endswith(".local.json") or name.endswith(".local.json.backup"):
        return True
    return False


def _assert_no_symlink_ancestors(path: Path, stop: Path | None = None, label: str = "path") -> None:
    current = path
    stop = stop.absolute() if stop is not None else None
    while True:
        if stop is not None and current == stop:
            break
        if current.is_symlink():
            raise ValueError(f"{label} contains a symlinked path component: {current}")
        if current.parent == current:
            break
        current = current.parent


def _assert_source_inputs(source_root: Path) -> None:
    root = source_root.resolve()
    for path in [root, *root.rglob("*")]:
        if path.is_symlink():
            raise ValueError(f"source symlinks are not supported: {path}")
    repo_root = root.parent
    tracked = (
        repo_root / "plugin.json",
        repo_root / ".claude-plugin" / "plugin.json",
        repo_root / "packaging" / "README.md",
        repo_root / "packaging" / "runtime-guidance.md",
        repo_root / "LICENSE",
    )
    for path in tracked:
        _assert_no_symlink_ancestors(path, stop=repo_root, label="source input")


def _assert_output_tree_safe(output_root: Path) -> None:
    targets = (
        output_root,
        output_root / "claude" / PLUGIN_NAME,
        output_root / "agent" / PLUGIN_NAME,
    )
    for target in targets:
        _assert_no_symlink_ancestors(target, stop=output_root.parent, label="output")


def _copy_skill(skill: SkillSource, output_root: Path, aliases: dict[str, str], portable: bool) -> None:
    destination = output_root / "skills" / skill.output_name
    destination.mkdir(parents=True, exist_ok=True)
    explicit_only = skill.frontmatter.get("disable-model-invocation") is True
    if portable:
        frontmatter = _portable_frontmatter(skill.frontmatter)
        body = _pointer(skill.source_dir, explicit_only) + _rewrite_aliases(skill.body, aliases)
        if skill.output_name == "setup":
            body = _rewrite_aliases(skill.body, aliases)
        (destination / "SKILL.md").write_text(_render_document(frontmatter, body), encoding="utf-8")
    else:
        body = skill.body if skill.output_name == "setup" else _pointer(skill.source_dir, explicit_only) + skill.body
        body = _rewrite_aliases(body, aliases)
        (destination / "SKILL.md").write_text(_render_document(skill.frontmatter, body), encoding="utf-8")

    for source in sorted(skill.directory.rglob("*")):
        relative = source.relative_to(skill.directory)
        if source == skill.directory / "SKILL.md" or source.is_dir() or _should_exclude_path(relative):
            continue
        _copy_text_or_binary(source, destination / relative, aliases)


def _should_exclude_template(path: Path) -> bool:
    return _should_exclude_path(path) or "mcp" in path.parts


def _copy_workflow_templates(source_root: Path, setup_destination: Path) -> None:
    target = setup_destination / "assets" / "workflow" / ".claude"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for source in sorted(source_root.rglob("*")):
        relative = source.relative_to(source_root)
        if _should_exclude_template(relative):
            continue
        destination = target / relative
        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        else:
            _copy_text_or_binary(source, destination, {})


def _copy_package_docs(source_root: Path, output_root: Path) -> None:
    repo_root = source_root.parent
    required = {
        "README.md": repo_root / "packaging" / "README.md",
        "LICENSE": repo_root / "LICENSE",
        "runtime-guidance.md": repo_root / "packaging" / "runtime-guidance.md",
    }
    for name, source in required.items():
        if not source.is_file():
            raise ValueError(f"required package document is missing: {source}")
        _copy_text_or_binary(source, output_root / name, {})


def _read_agents(source_root: Path) -> list[tuple[Path, dict[str, Any], str]]:
    agents: list[tuple[Path, dict[str, Any], str]] = []
    seen: set[str] = set()
    for path in sorted((source_root / "agents").rglob("*.md")):
        frontmatter, body = _parse_frontmatter(path)
        name = _validate_component_name(frontmatter.get("name", path.stem), "agent", path)
        if name in seen:
            raise ValueError(f"duplicate agent name: {name}")
        seen.add(name)
        agents.append((path, frontmatter, body))
    return agents


def _copy_agents(source_root: Path, output_root: Path, aliases: dict[str, str]) -> dict[str, list[str]]:
    destination_root = output_root / "agents"
    destination_root.mkdir(parents=True, exist_ok=True)
    dependencies: dict[str, list[str]] = {}
    for source, frontmatter, body in _read_agents(source_root):
        name = _validate_component_name(frontmatter.get("name", source.stem), "agent", source)
        rewritten = dict(frontmatter)
        raw_skills = rewritten.get("skills")
        original_dependencies: list[str] = []
        if isinstance(raw_skills, list):
            original_dependencies = [str(value) for value in raw_skills]
            rewritten["skills"] = [value if ":" in value else f"{PLUGIN_NAME}:{value}" for value in original_dependencies]
        elif isinstance(raw_skills, str) and raw_skills.strip():
            original_dependencies = [raw_skills]
            rewritten["skills"] = raw_skills if ":" in raw_skills else f"{PLUGIN_NAME}:{raw_skills}"
        if original_dependencies:
            dependencies[name] = original_dependencies
        path = destination_root / f"{name}.md"
        body = (
            "> Read `../skills/setup/references/task-context.md` for repository and bundled-resource "
            "resolution. Reuse the task and write ownership passed by the orchestrator.\n\n"
            + body
        )
        path.write_text(_render_document(rewritten, _rewrite_aliases(body, aliases)), encoding="utf-8")
    return dependencies


def _iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() or path.is_symlink():
            yield path


def _artifact_snapshot(root: Path) -> dict[str, tuple[Any, ...]]:
    snapshot: dict[str, tuple[Any, ...]] = {}
    for path in _iter_files(root):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            snapshot[relative] = ("symlink", path.readlink().as_posix())
        else:
            snapshot[relative] = ("file", path.read_bytes(), stat.S_IMODE(path.stat().st_mode))
    return snapshot


def _tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in _iter_files(root):
        relative = path.relative_to(root).as_posix()
        if relative == ".build-manifest.json":
            continue
        if _should_exclude_path(Path(relative)):
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        if path.is_symlink():
            digest.update(b"symlink:")
            digest.update(path.readlink().as_posix().encode("utf-8"))
        else:
            digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _source_fingerprint(source_root: Path) -> str:
    digest = hashlib.sha256()
    digest.update(_tree_fingerprint(source_root).encode("ascii"))
    repo_root = source_root.parent
    tracked_files = (
        repo_root / "plugin.json",
        repo_root / ".claude-plugin" / "plugin.json",
        repo_root / "packaging" / "README.md",
        repo_root / "packaging" / "runtime-guidance.md",
        repo_root / "LICENSE",
    )
    for manifest in tracked_files:
        if manifest.is_file():
            digest.update(manifest.relative_to(repo_root).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(manifest.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def _write_build_manifest(output_root: Path, artifact: str, source_fingerprint: str, dependencies: dict[str, list[str]]) -> None:
    manifest = {
        "format": BUILD_FORMAT,
        "artifact": artifact,
        "plugin": PLUGIN_NAME,
        "source_fingerprint": source_fingerprint,
        "agent_skill_dependencies": dependencies,
    }
    (output_root / ".build-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _clean_output(path: Path, artifact: str) -> None:
    if path.exists() or path.is_symlink():
        if path.is_symlink() or path.is_file():
            raise ValueError(f"refusing to remove non-directory generated output: {path}")
        else:
            marker = path / ".build-manifest.json"
            if not marker.is_file():
                raise ValueError(f"refusing to remove unmarked output directory: {path}")
            try:
                manifest = json.loads(marker.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid generated output marker: {marker}") from exc
            if manifest.get("plugin") != PLUGIN_NAME or manifest.get("artifact") != artifact:
                raise ValueError(f"generated output marker does not belong to {PLUGIN_NAME}/{artifact}: {marker}")
            shutil.rmtree(path)


def _build_one(source_root: Path, output_root: Path, artifact: str, version: str, skills: list[SkillSource], aliases: dict[str, str], source_fingerprint: str) -> tuple[list[str], dict[str, list[str]]]:
    _clean_output(output_root, artifact)
    output_root.mkdir(parents=True, exist_ok=True)
    if artifact == "claude":
        manifest = json.loads((source_root.parent / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        dependencies: dict[str, list[str]] = {}
    else:
        manifest = json.loads((source_root.parent / "plugin.json").read_text(encoding="utf-8"))
        dependencies = {}
    manifest["version"] = version
    if artifact == "claude":
        (output_root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
        (output_root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
    else:
        (output_root / "plugin.json").write_text(
            json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
    for skill in skills:
        _copy_skill(skill, output_root, aliases, portable=artifact == "agent")
    _copy_workflow_templates(source_root, output_root / "skills" / "setup")
    _copy_package_docs(source_root, output_root)
    if artifact == "claude":
        dependencies = _copy_agents(source_root, output_root, aliases)
    _write_build_manifest(output_root, artifact, source_fingerprint, dependencies)
    return [skill.output_name for skill in skills], dependencies


def source_version(source_root: Path) -> str:
    versions = []
    for relative in (".claude-plugin/plugin.json", "plugin.json"):
        path = source_root.parent / relative
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON in {path}: {error}") from error
        version = manifest.get("version") if isinstance(manifest, dict) else None
        if not isinstance(version, str) or not version.strip():
            raise ValueError("Both source manifests must declare a nonempty version.")
        versions.append(version)
    if versions[0] != versions[1]:
        raise ValueError(f"Source manifest versions differ: {versions!r}.")
    return versions[0]


def build(source_root: Path | str, output_root: Path | str, version: str | None = None) -> BuildReport:
    source_input = Path(source_root).expanduser().absolute()
    output_input = Path(output_root).expanduser().absolute()
    if source_input.is_symlink():
        raise ValueError(f"source root must not be a symlink: {source_input}")
    _assert_source_inputs(source_input.resolve())
    _assert_output_tree_safe(output_input)
    source_root = source_input.resolve()
    output_root = output_input.resolve()
    version = version if version is not None else source_version(source_root)
    if output_root == source_root or output_root.is_relative_to(source_root) or source_root.is_relative_to(output_root):
        raise ValueError("source and output trees must not overlap")
    skills = _read_skills(source_root)
    aliases = _alias_map(skills)
    agents = _read_agents(source_root)
    fingerprint = _source_fingerprint(source_root)
    claude_output = output_root / "claude" / PLUGIN_NAME
    agent_output = output_root / "agent" / PLUGIN_NAME
    _build_one(source_root, claude_output, "claude", version, skills, aliases, fingerprint)
    _build_one(source_root, agent_output, "agent", version, skills, aliases, fingerprint)
    return BuildReport(source_root, (claude_output, agent_output), tuple(skill.output_name for skill in skills), tuple(name for name, _, _ in agents), fingerprint)


def check(source_root: Path | str, output_root: Path | str, version: str | None = None) -> BuildReport:
    output_input = Path(output_root).expanduser().absolute()
    _assert_output_tree_safe(output_input)
    output_root = output_input.resolve()
    with tempfile.TemporaryDirectory(prefix="claudops-build-check-") as temp:
        expected = build(source_root, Path(temp) / "dist", version=version)
        for actual, expected_path in zip(
            (output_root / "claude" / PLUGIN_NAME, output_root / "agent" / PLUGIN_NAME),
            expected.outputs,
        ):
            if not actual.exists():
                raise ValueError(f"missing generated artifact: {actual}")
            actual_files = _artifact_snapshot(actual)
            expected_files = _artifact_snapshot(expected_path)
            if actual_files != expected_files:
                missing = sorted(set(expected_files) - set(actual_files))
                extra = sorted(set(actual_files) - set(expected_files))
                changed = sorted(key for key in set(actual_files) & set(expected_files) if actual_files[key] != expected_files[key])
                raise ValueError(f"stale artifact {actual}: missing={missing[:3]} extra={extra[:3]} changed={changed[:3]}")
    return BuildReport(
        expected.source_root,
        (output_root / "claude" / PLUGIN_NAME, output_root / "agent" / PLUGIN_NAME),
        expected.skill_names,
        expected.agent_names,
        expected.source_fingerprint,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=_repo_root() / ".claude")
    parser.add_argument("--out", type=Path, default=_repo_root() / "dist")
    parser.add_argument("--version", default=None)
    parser.add_argument("--check", action="store_true", help="fail when generated output is stale")
    args = parser.parse_args(argv)
    report = check(args.source, args.out, args.version) if args.check else build(args.source, args.out, args.version)
    print(json.dumps({"outputs": [str(path) for path in report.outputs], "skills": len(report.skill_names), "agents": len(report.agent_names), "source_fingerprint": report.source_fingerprint}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
