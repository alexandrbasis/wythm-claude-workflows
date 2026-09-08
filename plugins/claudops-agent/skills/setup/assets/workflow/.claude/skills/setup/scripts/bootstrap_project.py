#!/usr/bin/env python3
"""Preview or materialize missing claudops project templates without overwrites."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


COMPONENTS = {"skills", "agents", "docs", "scripts", "hooks"}
EXCLUDED_DIRS = {"logs", "__pycache__", "node_modules", ".git"}


def template_root() -> Path:
    """Resolve from the loaded package, never from the target project's cwd."""
    script = Path(__file__).resolve()
    bundled = script.parents[1] / "assets" / "workflow" / ".claude"
    if bundled.is_dir():
        return bundled
    source = script.parents[3]
    if source.name == ".claude" and (source / "skills").is_dir():
        return source
    raise ValueError("Cannot locate the bundled claudops workflow templates")


def included(relative: Path) -> bool:
    return (
        relative.parts[0] in COMPONENTS
        and not any(part in EXCLUDED_DIRS for part in relative.parts)
        and relative.parts[:4] != ("skills", "setup", "assets", "workflow")
        and ".local." not in relative.name
        and relative.name != ".env"
        and not relative.name.startswith(".env.")
        and relative.name not in {".gitkeep", "claudops-upstream.lock.json"}
        and relative.suffix not in {".pyc", ".log"}
    )


def check_destination(path: Path, project: Path) -> None:
    for candidate in (path, *path.parents):
        if candidate == project:
            break
        if candidate.is_symlink():
            raise ValueError(f"Destination contains a symlink: {candidate}")
        if candidate != path and candidate.exists() and not candidate.is_dir():
            raise ValueError(f"Destination parent is not a directory: {candidate}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Destination is not a regular file: {path}")


def plan(source: Path, project: Path) -> tuple[list[tuple[Path, Path]], list[str]]:
    source = source.resolve()
    project = project.resolve()
    if not project.is_dir():
        raise ValueError(f"Project must be an existing directory: {project}")
    target = project / ".claude"
    if target == source or target.is_relative_to(source):
        raise ValueError("Project and template source must be separate directories")
    additions: list[tuple[Path, Path]] = []
    preserved: list[str] = []
    for src in sorted(source.rglob("*")):
        relative = src.relative_to(source)
        if not included(relative):
            continue
        if src.is_symlink():
            raise ValueError(f"Template contains a symlink: {relative}")
        if not src.is_file():
            continue
        dest = project / ".claude" / relative
        check_destination(dest, project)
        disabled = dest.with_name(dest.name + ".disabled")
        check_destination(disabled, project)
        if dest.exists():
            preserved.append(str(dest.relative_to(project)))
        elif disabled.exists():
            preserved.append(str(disabled.relative_to(project)))
        else:
            additions.append((src, dest))
    if not additions and not preserved:
        raise ValueError("No workflow templates found")
    return additions, preserved


def bootstrap(source: Path, project: Path, apply: bool = False) -> dict:
    project = project.resolve()
    additions, preserved = plan(source, project)
    written: list[str] = []
    try:
        if apply:
            for src, dest in additions:
                check_destination(dest, project)
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as stream:
                    written.append(str(dest.relative_to(project)))
                    stream.write(src.read_bytes())
                shutil.copymode(src, dest)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Bootstrap stopped: {exc}; files already created: {written}") from exc
    return {
        "mode": "apply" if apply else "preview",
        "project": str(project),
        "add": [str(dest.relative_to(project)) for _, dest in additions],
        "preserved": preserved,
        "written": written,
        "settings_changed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Create missing files after reviewing the preview")
    args = parser.parse_args()
    try:
        result = bootstrap(template_root(), args.project, args.apply)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
