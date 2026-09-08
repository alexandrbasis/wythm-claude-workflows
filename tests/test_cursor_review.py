#!/usr/bin/env python3
"""Behavioral tests for the bounded Cursor Agent review adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / ".claude/skills/cursor-cli/scripts/review.py"


FAKE_AGENT = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json
    import os
    from pathlib import Path
    import subprocess
    import sys
    import time

    if sys.argv[1:] == ["--version"]:
        print(os.environ.get("FAKE_AGENT_VERSION", "2026.09.02-test"))
        sys.exit(int(os.environ.get("FAKE_AGENT_VERSION_EXIT", "0")))

    invocation_file = os.environ.get("FAKE_AGENT_INVOCATION")
    if invocation_file:
        Path(invocation_file).write_text(json.dumps(sys.argv[1:]), encoding="utf-8")

    child_marker = os.environ.get("FAKE_AGENT_CHILD_MARKER")
    if child_marker:
        child_delay = os.environ.get("FAKE_AGENT_CHILD_DELAY", "1")
        child = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import os,pathlib,time; time.sleep(float(os.environ['DELAY'])); pathlib.Path(os.environ['MARKER']).write_text('late')",
            ],
            env={**os.environ, "MARKER": child_marker, "DELAY": child_delay},
        )
        child_pid_file = os.environ.get("FAKE_AGENT_CHILD_PID")
        if child_pid_file:
            Path(child_pid_file).write_text(str(child.pid), encoding="utf-8")

    sys.stderr.write(os.environ.get("FAKE_AGENT_STDERR", ""))
    if os.environ.get("FAKE_AGENT_SLEEP"):
        time.sleep(float(os.environ["FAKE_AGENT_SLEEP"]))
    sys.stdout.write(os.environ.get("FAKE_AGENT_STDOUT", ""))
    sys.exit(int(os.environ.get("FAKE_AGENT_EXIT", "0")))
    """
)


def success_payload(result: str = "Looks good.") -> str:
    return json.dumps(
        {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "duration_ms": 12,
            "result": result,
            "session_id": "test-session",
        }
    )


class CursorReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.fake_agent = self.fake_bin / "agent"
        self.fake_agent.write_text(FAKE_AGENT, encoding="utf-8")
        self.fake_agent.chmod(self.fake_agent.stat().st_mode | stat.S_IXUSR)

        self.prompt_file = self.root / "prompt.md"
        self.prompt_file.write_text("Review the change.\nAnswer with findings.", encoding="utf-8")
        self.source_file = self.root / "source.py"
        self.source_file.write_text("print('source')\n", encoding="utf-8")

        self.env = os.environ.copy()
        self.env["PATH"] = f"{self.fake_bin}{os.pathsep}{self.env['PATH']}"
        self.invocation_file = self.root / "invocation.json"
        self.env["FAKE_AGENT_INVOCATION"] = str(self.invocation_file)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_runner(
        self,
        *extra_args: str,
        stdout: str | None = None,
        stderr: str = "diagnostic warning\n",
        exit_code: int = 0,
        timeout: str = "3",
        sleep: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        output_dir = self.root / "artifacts"
        self.env["FAKE_AGENT_STDOUT"] = success_payload() if stdout is None else stdout
        self.env["FAKE_AGENT_STDERR"] = stderr
        self.env["FAKE_AGENT_EXIT"] = str(exit_code)
        if sleep is None:
            self.env.pop("FAKE_AGENT_SLEEP", None)
        else:
            self.env["FAKE_AGENT_SLEEP"] = sleep
        command = [
            sys.executable,
            str(RUNNER),
            "--prompt-file",
            str(self.prompt_file),
            "--file",
            str(self.source_file),
            "--output-dir",
            str(output_dir),
            "--timeout",
            timeout,
            *extra_args,
        ]
        return subprocess.run(
            command,
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def read_invocation(self) -> list[str]:
        return json.loads(self.invocation_file.read_text(encoding="utf-8"))

    def read_receipt(self) -> dict[str, object]:
        return json.loads((self.root / "artifacts" / "receipt.json").read_text(encoding="utf-8"))

    def test_valid_response_is_printed_and_sources_are_inlined(self) -> None:
        result = self.run_runner("--model", "composer-2.5")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Looks good.")
        invocation = self.read_invocation()
        self.assertEqual(invocation[:7], ["-p", "--mode", "ask", "--output-format", "json", "--model", "composer-2.5"])
        self.assertIn("Review the change.", invocation[-1])
        self.assertIn(f"[BEGIN SOURCE: {self.source_file}]", invocation[-1])
        self.assertIn("print('source')", invocation[-1])

        artifacts = self.root / "artifacts"
        self.assertEqual(json.loads((artifacts / "stdout.json").read_text(encoding="utf-8")), json.loads(success_payload()))
        self.assertEqual((artifacts / "stderr.log").read_text(encoding="utf-8"), "diagnostic warning\n")
        self.assertEqual((artifacts / "response.txt").read_text(encoding="utf-8"), "Looks good.")
        receipt = self.read_receipt()
        self.assertEqual(receipt["provider"], "Cursor")
        self.assertEqual(receipt["version"], "2026.09.02-test")
        self.assertEqual(receipt["model"], "composer-2.5")
        self.assertEqual(receipt["model_source"], "requested")
        self.assertEqual(receipt["actual_model"], "unverified")
        self.assertEqual(receipt["status"], "SUCCESS")
        self.assertEqual(receipt["exit_code"], 0)
        self.assertEqual(receipt["scope"]["files"], [str(self.source_file.resolve())])  # type: ignore[index]
        self.assertEqual(receipt["prompt_purpose"], "Review the change.")
        self.assertEqual(receipt["output_dir"], str(artifacts.resolve()))

    def test_provider_default_omits_model_and_marks_identity_unverified(self) -> None:
        result = self.run_runner()

        self.assertEqual(result.returncode, 0, result.stderr)
        invocation = self.read_invocation()
        self.assertEqual(invocation[:5], ["-p", "--mode", "ask", "--output-format", "json"])
        self.assertNotIn("--model", invocation)
        receipt = self.read_receipt()
        self.assertEqual(receipt["model"], "provider default (unverified)")
        self.assertEqual(receipt["model_source"], "provider default (unverified)")
        self.assertEqual(receipt["actual_model"], "unverified")
        self.assertIn("unverified", receipt["verification_gaps"][0])  # type: ignore[index]

    def test_soft_error_with_nonempty_result_fails_closed(self) -> None:
        result = self.run_runner(
            stdout=json.dumps(
                {
                    "type": "result",
                    "subtype": "success",
                    "is_error": False,
                    "result": "There was an error, but here is a partial answer.",
                    "error": "quota",
                }
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("provider error", result.stderr)
        self.assertEqual(self.read_receipt()["failure"], "provider error")

    def test_errors_and_denied_actions_are_failures_even_with_success_envelope(self) -> None:
        for field, value, expected in (
            ("errors", ["tool failed"], "provider errors"),
            ("denied_actions", ["read_file"], "denied actions"),
        ):
            with self.subTest(field=field):
                result = self.run_runner(
                    stdout=json.dumps(
                        {
                            "type": "result",
                            "subtype": "success",
                            "is_error": False,
                            "result": "Partial answer",
                            field: value,
                        }
                    )
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.read_receipt()["failure"], expected)
                # Each subtest gets a fresh output directory only when the
                # previous one is removed; retain the same fixture but clean
                # up the artifact directory before the next iteration.
                import shutil

                shutil.rmtree(self.root / "artifacts")

    def test_timeout_kills_process_group_and_preserves_partial_artifacts(self) -> None:
        marker = self.root / "child-finished"
        child_pid_file = self.root / "child.pid"
        self.env["FAKE_AGENT_CHILD_MARKER"] = str(marker)
        self.env["FAKE_AGENT_CHILD_PID"] = str(child_pid_file)
        self.env["FAKE_AGENT_CHILD_DELAY"] = "4"
        result = self.run_runner(sleep="20", timeout="3", stderr="timed out\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timeout", result.stderr.lower())
        self.assertEqual((self.root / "artifacts" / "stderr.log").read_text(encoding="utf-8"), "timed out\n")
        self.assertEqual(self.read_receipt()["failure"], "timeout")
        # The child is in the same process group and must not outlive the
        # bounded review to write its delayed marker.
        time.sleep(4.5)
        self.assertFalse(marker.exists())

    def test_nonzero_exit_is_failure_even_with_valid_json(self) -> None:
        result = self.run_runner(exit_code=7)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_receipt()["failure"], "exit code 7")

    def test_malformed_json_is_failure(self) -> None:
        result = self.run_runner(stdout="not json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed", result.stderr.lower())
        self.assertEqual(self.read_receipt()["failure"], "malformed JSON")

    def test_envelope_shape_and_empty_result_are_rejected(self) -> None:
        cases = (
            ({"subtype": "success", "is_error": False, "result": "answer"}, "provider type is not result"),
            ({"type": "result", "is_error": False, "result": "answer"}, "provider subtype is not success"),
            ({"type": "result", "subtype": "success", "result": "answer"}, "provider result is marked as error"),
            ({"type": "result", "subtype": "success", "is_error": True, "result": "answer"}, "provider result is marked as error"),
            ({"type": "result", "subtype": "success", "is_error": False, "result": "   "}, "empty result"),
            ({"type": "result", "subtype": "success", "is_error": False, "result": {"text": "answer"}}, "result is not a string"),
        )
        for payload, failure in cases:
            with self.subTest(payload=payload):
                result = self.run_runner(stdout=json.dumps(payload))
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.read_receipt()["failure"], failure)
                import shutil

                shutil.rmtree(self.root / "artifacts")

    def test_version_failure_retains_complete_receipt_without_review_launch(self) -> None:
        self.env["FAKE_AGENT_VERSION_EXIT"] = "3"
        result = self.run_runner("--model", "composer-test")

        self.assertEqual(result.returncode, 1)
        self.assertIn("version preflight", result.stderr)
        receipt = self.read_receipt()
        self.assertEqual(receipt["model"], "composer-test")
        self.assertEqual(receipt["version"], "unverified")
        self.assertEqual(receipt["scope"]["files"], [str(self.source_file.resolve())])  # type: ignore[index]
        self.assertFalse(self.invocation_file.exists())
        self.assertTrue((self.root / "artifacts" / "version.stderr.log").is_file())

    def test_invalid_input_is_rejected_before_launch(self) -> None:
        self.prompt_file.unlink()
        result = self.run_runner()

        self.assertEqual(result.returncode, 2)
        self.assertIn("prompt file", result.stderr.lower())
        self.assertFalse(self.invocation_file.exists())
        self.assertFalse((self.root / "artifacts").exists())

    def test_oversized_input_is_rejected_before_launch(self) -> None:
        self.source_file.write_text("x" * 100000, encoding="utf-8")
        result = self.run_runner()

        self.assertEqual(result.returncode, 2)
        self.assertIn("96 KiB", result.stderr)
        self.assertFalse(self.invocation_file.exists())

    def test_existing_output_dir_and_invalid_model_are_rejected(self) -> None:
        output_dir = self.root / "artifacts"
        output_dir.mkdir()
        result = self.run_runner()
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not already exist", result.stderr.lower())
        import shutil

        shutil.rmtree(output_dir)
        result = self.run_runner("--model", "has whitespace")
        self.assertEqual(result.returncode, 2)
        self.assertIn("model", result.stderr.lower())
        self.assertFalse(self.invocation_file.exists())


if __name__ == "__main__":
    unittest.main()
