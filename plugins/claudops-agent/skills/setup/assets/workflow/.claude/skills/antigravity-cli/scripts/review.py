#!/usr/bin/env python3
"""Run one bounded, read-only Antigravity (agy) review.

The adapter owns process execution and output validation.  It deliberately
does not authenticate, retry, alter provider settings, or grant permissions.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
from typing import Any, Sequence


PROVIDER_DEFAULT = "provider default (unverified)"


class ReviewInputError(ValueError):
    """An invocation argument or local input is invalid."""


@dataclass(frozen=True)
class ProcessResult:
    stdout: bytes
    stderr: bytes
    returncode: int | None
    timed_out: bool = False


def positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("timeout must be a positive number of seconds") from exc
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("timeout must be a positive number of seconds")
    return seconds


def model_value(value: str) -> str:
    """Validate a provider model token without imposing a provider family."""
    if not value or value.startswith("-") or any(character.isspace() for character in value):
        raise argparse.ArgumentTypeError("model must be one non-empty CLI token")
    if len(value) > 128:
        raise argparse.ArgumentTypeError("model is too long")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-file", required=True, help="verified local file containing the prompt")
    parser.add_argument(
        "--file",
        dest="source_files",
        action="append",
        default=[],
        help="verified local file to inline into the prompt; repeatable",
    )
    parser.add_argument("--model", type=model_value, help="optional agy model slug")
    parser.add_argument("--effort", choices=("low", "medium", "high"), help="optional reasoning effort")
    parser.add_argument("--timeout", type=positive_seconds, required=True, help="provider timeout in seconds")
    parser.add_argument("--output-dir", required=True, help="new directory for bounded run artifacts")
    return parser


def _read_verified_file(path_value: str, kind: str) -> str:
    path = Path(path_value)
    if not path.is_file():
        raise ReviewInputError(f"{kind} file is missing or not a regular file: {path_value}")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ReviewInputError(f"{kind} file cannot be read: {path_value}") from exc


def compose_prompt(prompt_file: str, source_files: Sequence[str]) -> str:
    prompt = _read_verified_file(prompt_file, "prompt")
    if not prompt.strip():
        raise ReviewInputError("prompt file is empty")

    parts = [prompt]
    for source_file in source_files:
        source = _read_verified_file(source_file, "source")
        parts.extend(
            (
                "",
                f"[BEGIN SOURCE: {source_file}]",
                source,
                f"[END SOURCE: {source_file}]",
            )
        )
    result = "\n".join(parts)
    if len(result.encode("utf-8")) > 96 * 1024:
        raise ReviewInputError("combined prompt exceeds 96 KiB; reduce the review scope")
    return result


def _new_output_dir(path_value: str) -> Path:
    output_dir = Path(path_value)
    if output_dir.exists():
        raise ReviewInputError(f"output directory must not already exist: {path_value}")
    if not output_dir.parent.is_dir():
        raise ReviewInputError(f"output directory parent is missing: {output_dir.parent}")
    try:
        output_dir.mkdir(mode=0o700)
    except OSError as exc:
        raise ReviewInputError(f"cannot create output directory: {path_value}") from exc
    return output_dir


def _kill_process_group(process: subprocess.Popen[bytes]) -> None:
    """Terminate the process and all descendants, without waiting unboundedly."""
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:  # pragma: no cover - the supported runtime is macOS/Linux
        try:
            process.kill()
        except ProcessLookupError:
            pass


def run_process(command: Sequence[str], timeout: float) -> ProcessResult:
    try:
        process = subprocess.Popen(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=(os.name == "posix"),
        )
    except OSError as exc:
        return ProcessResult(b"", str(exc).encode("utf-8", "replace"), None)

    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as expired:
        # TimeoutExpired carries any bytes read before the deadline.  Kill the
        # whole session before closing pipes so descendants cannot linger.
        partial_stdout = expired.output or b""
        partial_stderr = expired.stderr or b""
        _kill_process_group(process)
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                pass
        for stream in (process.stdout, process.stderr):
            if stream is not None:
                stream.close()
        return ProcessResult(partial_stdout, partial_stderr, process.returncode, True)
    return ProcessResult(stdout, stderr, process.returncode)


def _nonempty_field(payload: dict[str, Any], name: str) -> bool:
    value = payload.get(name)
    return value not in (None, "", [], {})


def validate_response(process_result: ProcessResult) -> str:
    if process_result.timed_out:
        raise RuntimeError("timeout")
    if process_result.returncode != 0:
        if process_result.returncode is None:
            raise RuntimeError("provider did not start")
        raise RuntimeError(f"exit code {process_result.returncode}")
    try:
        payload = json.loads(process_result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("malformed JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("malformed JSON")
    if payload.get("status") != "SUCCESS":
        raise RuntimeError("provider status is not SUCCESS")
    if _nonempty_field(payload, "error"):
        raise RuntimeError("provider error")
    if _nonempty_field(payload, "denied_actions"):
        raise RuntimeError("denied actions")
    response = payload.get("response")
    if not isinstance(response, str):
        raise RuntimeError("response is not a string")
    if not response.strip():
        raise RuntimeError("empty response")
    return response


def _write_artifact(path: Path, content: bytes | str) -> None:
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def _receipt(
    *,
    model: str,
    version: str,
    scope: dict[str, Any],
    prompt_purpose: str,
    output_dir: Path,
    timeout: float,
    status: str,
    returncode: int | None,
    failure: str | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "provider": "agy",
        "version": version,
        "model": model,
        "timeout_seconds": timeout,
        "status": status,
        "exit_code": returncode,
        "scope": scope,
        "prompt_purpose": prompt_purpose,
        "output_dir": str(output_dir.resolve()),
        "output_file": str((output_dir / "response.txt").resolve()) if status == "SUCCESS" else None,
        "verification_gaps": (["provider-selected model unverified"] if model == PROVIDER_DEFAULT else []),
    }
    if failure is not None:
        receipt["failure"] = failure
    return receipt


def run(args: argparse.Namespace) -> int:
    prompt = compose_prompt(args.prompt_file, args.source_files)
    output_dir = _new_output_dir(args.output_dir)
    model = args.model or PROVIDER_DEFAULT
    context = {
        "scope": {
            "repository": str(Path.cwd()),
            "files": [str(Path(path).resolve()) for path in args.source_files],
        },
        "prompt_purpose": prompt.strip().splitlines()[0][:200],
        "output_dir": output_dir,
    }
    command = ["agy", "-p", prompt]
    if args.model:
        command.extend(("--model", args.model))
    if args.effort:
        command.extend(("--effort", args.effort))
    command.extend(
        (
            "--output-format",
            "json",
            "--print-timeout",
            f"{args.timeout:g}s",
        )
    )

    version_result = run_process(["agy", "--version"], min(args.timeout, 5))
    version = version_result.stdout.decode("utf-8", "replace").strip()
    _write_artifact(output_dir / "version.stderr.log", version_result.stderr)
    if version_result.returncode != 0 or version_result.timed_out or not version:
        receipt = _receipt(
            model=model, version="unverified", timeout=args.timeout,
            status="FAILURE", returncode=version_result.returncode,
            failure="version preflight failed", **context,
        )
        _write_artifact(output_dir / "receipt.json", json.dumps(receipt, indent=2) + "\n")
        print(f"agy version preflight failed; artifacts: {output_dir}", file=sys.stderr)
        return 1
    process_result = run_process(command, args.timeout)
    _write_artifact(output_dir / "stdout.json", process_result.stdout)
    _write_artifact(output_dir / "stderr.log", process_result.stderr)
    try:
        response = validate_response(process_result)
    except RuntimeError as exc:
        failure = str(exc)
        _write_artifact(
            output_dir / "receipt.json",
            json.dumps(
                _receipt(
                    model=model,
                    version=version,
                    **context,
                    timeout=args.timeout,
                    status="FAILURE",
                    returncode=process_result.returncode,
                    failure=failure,
                ),
                indent=2,
            )
            + "\n",
        )
        print(f"agy review failed ({failure}); artifacts: {output_dir}", file=sys.stderr)
        return 1

    _write_artifact(output_dir / "response.txt", response)
    _write_artifact(
        output_dir / "receipt.json",
        json.dumps(
            _receipt(
                model=model,
                version=version,
                **context,
                timeout=args.timeout,
                status="SUCCESS",
                returncode=process_result.returncode,
            ),
            indent=2,
        )
        + "\n",
    )
    sys.stdout.write(response)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except ReviewInputError as exc:
        print(f"agy review input error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"agy review output error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
