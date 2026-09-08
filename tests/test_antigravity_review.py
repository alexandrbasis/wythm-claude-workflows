#!/usr/bin/env python3
"""Behavioral tests for the bounded agy review adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / ".claude/skills/antigravity-cli/scripts/review.py"
HOOK = ROOT / ".claude/scripts/review-plan-gemini.sh"


FAKE_AGY = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json
    import os
    from pathlib import Path
    import sys
    import time

    if sys.argv[1:] == ["--version"]:
        print("1.1.test")
        sys.exit(int(os.environ.get("FAKE_AGY_VERSION_EXIT", "0")))

    invocation_file = os.environ.get("FAKE_AGY_INVOCATION")
    if invocation_file:
        Path(invocation_file).write_text(json.dumps(sys.argv[1:]), encoding="utf-8")

    sys.stderr.write(os.environ.get("FAKE_AGY_STDERR", ""))
    if os.environ.get("FAKE_AGY_SLEEP"):
        time.sleep(float(os.environ["FAKE_AGY_SLEEP"]))
    sys.stdout.write(os.environ.get("FAKE_AGY_STDOUT", ""))
    sys.exit(int(os.environ.get("FAKE_AGY_EXIT", "0")))
    """
)


class AntigravityReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.fake_agy = self.fake_bin / "agy"
        self.fake_agy.write_text(FAKE_AGY, encoding="utf-8")
        self.fake_agy.chmod(self.fake_agy.stat().st_mode | stat.S_IXUSR)
        legacy = self.fake_bin / "gemini"
        legacy.write_text("#!/bin/sh\nexit 55\n")
        legacy.chmod(0o700)

        self.prompt_file = self.root / "prompt.md"
        self.prompt_file.write_text("Review the change.", encoding="utf-8")
        self.source_file = self.root / "source.py"
        self.source_file.write_text("print('source')\n", encoding="utf-8")

        self.env = os.environ.copy()
        self.env["PATH"] = f"{self.fake_bin}{os.pathsep}{self.env['PATH']}"
        self.invocation_file = self.root / "invocation.json"
        self.env["FAKE_AGY_INVOCATION"] = str(self.invocation_file)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_runner(
        self,
        *extra_args: str,
        stdout: str = '{"status":"SUCCESS","response":"Looks good."}',
        stderr: str = "diagnostic warning\n",
        exit_code: int = 0,
        timeout: str = "3",
        sleep: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        output_dir = self.root / "artifacts"
        self.env["FAKE_AGY_STDOUT"] = stdout
        self.env["FAKE_AGY_STDERR"] = stderr
        self.env["FAKE_AGY_EXIT"] = str(exit_code)
        if sleep is None:
            self.env.pop("FAKE_AGY_SLEEP", None)
        else:
            self.env["FAKE_AGY_SLEEP"] = sleep
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
        )

    def read_invocation(self) -> list[str]:
        return json.loads(self.invocation_file.read_text(encoding="utf-8"))

    def test_valid_response_is_printed_and_sources_are_inlined(self) -> None:
        result = self.run_runner("--model", "gemini-3.8-flash-high", "--effort", "high")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Looks good.")
        invocation = self.read_invocation()
        self.assertEqual(
            invocation[2:],
            [
                "--model",
                "gemini-3.8-flash-high",
                "--effort",
                "high",
                "--output-format",
                "json",
                "--print-timeout",
                "3s",
            ],
        )
        self.assertEqual(invocation[0], "-p")
        self.assertIn("Review the change.", invocation[1])
        self.assertIn(f"[BEGIN SOURCE: {self.source_file}]", invocation[1])
        self.assertIn("print('source')", invocation[1])
        self.assertNotIn("@", invocation[1])

        artifacts = self.root / "artifacts"
        self.assertEqual(
            json.loads((artifacts / "stdout.json").read_text(encoding="utf-8")),
            {"status": "SUCCESS", "response": "Looks good."},
        )
        self.assertEqual((artifacts / "stderr.log").read_text(encoding="utf-8"), "diagnostic warning\n")
        receipt = json.loads((artifacts / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["provider"], "agy")
        self.assertEqual(receipt["version"], "1.1.test")
        self.assertEqual(receipt["model"], "gemini-3.8-flash-high")
        self.assertEqual(receipt["status"], "SUCCESS")
        self.assertEqual(receipt["scope"]["files"], [str(self.source_file.resolve())])
        self.assertEqual(receipt["prompt_purpose"], "Review the change.")
        self.assertEqual(receipt["output_dir"], str(artifacts.resolve()))

    def test_provider_default_omits_model_and_marks_receipt_unverified(self) -> None:
        result = self.run_runner()

        self.assertEqual(result.returncode, 0, result.stderr)
        invocation = self.read_invocation()
        self.assertEqual(invocation[0], "-p")
        self.assertNotIn("--model", invocation)
        self.assertNotIn("--effort", invocation)
        receipt = json.loads((self.root / "artifacts" / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["model"], "provider default (unverified)")

    def test_soft_denial_with_nonempty_response_fails_closed(self) -> None:
        result = self.run_runner(
            stdout=json.dumps(
                {
                    "status": "SUCCESS",
                    "response": "I was able to answer, but one action was denied.",
                    "denied_actions": ["read_file"],
                }
            )
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("artifacts", result.stderr)
        self.assertEqual((self.root / "artifacts" / "stderr.log").read_text(encoding="utf-8"), "diagnostic warning\n")
        receipt = json.loads((self.root / "artifacts" / "receipt.json").read_text())
        self.assertEqual(receipt["status"], "FAILURE")
        self.assertEqual(receipt["failure"], "denied actions")

    def test_timeout_kills_process_and_preserves_artifacts(self) -> None:
        result = self.run_runner(sleep="20", timeout="3", stderr="timed out\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("timeout", result.stderr.lower())
        self.assertEqual((self.root / "artifacts" / "stderr.log").read_text(encoding="utf-8"), "timed out\n")
        receipt = json.loads((self.root / "artifacts" / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["status"], "FAILURE")
        self.assertEqual(receipt["failure"], "timeout")

    def test_nonzero_exit_is_failure_even_with_valid_json(self) -> None:
        result = self.run_runner(exit_code=7)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        receipt = json.loads((self.root / "artifacts" / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["status"], "FAILURE")
        self.assertEqual(receipt["failure"], "exit code 7")

    def test_nonfinite_timeout_rejected_before_launch(self):
        result = self.run_runner(timeout="nan")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse(self.invocation_file.exists())

    def test_oversized_input_is_rejected_before_launch(self):
        self.source_file.write_text("x" * 100000)
        result = self.run_runner()
        self.assertEqual(result.returncode, 2)
        self.assertIn("96 KiB", result.stderr)
        self.assertFalse(self.invocation_file.exists())

    def run_hook(self, payload):
        workflow = self.root / ".claude"
        script_dir = workflow / "scripts"
        runner_dir = workflow / "skills" / "antigravity-cli" / "scripts"
        script_dir.mkdir(parents=True)
        runner_dir.mkdir(parents=True)
        shutil.copy2(RUNNER, runner_dir / "review.py")
        hook = script_dir / "review-plan-gemini.sh"
        shutil.copy2(HOOK, hook)
        plan = self.root / "plan.md"
        plan.write_text("Original plan.\n")
        self.env["FAKE_AGY_STDOUT"] = json.dumps(payload)
        event = {"tool_name": "ExitPlanMode", "tool_response": {"plan": "Original plan.", "filePath": str(plan)}}
        result = subprocess.run(["bash", str(hook)], input=json.dumps(event), env=self.env, cwd=self.root, capture_output=True, text=True, timeout=10)
        return result, plan

    def test_hook_preserves_plan_on_soft_denial(self):
        result, plan = self.run_hook({"status": "SUCCESS", "response": "Partial review", "denied_actions": ["read_file"]})
        self.assertEqual(plan.read_text(), "Original plan.\n")
        self.assertIn("incomplete", json.loads(result.stdout)["systemMessage"])

    def test_hook_appends_complete_review(self):
        result, plan = self.run_hook({"status": "SUCCESS", "response": "Known defect."})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Known defect.", plan.read_text())
        self.assertIn("Antigravity", json.loads(result.stdout)["additionalContext"])

    def test_version_failure_retains_complete_receipt(self):
        self.env["FAKE_AGY_VERSION_EXIT"] = "3"
        result = self.run_runner("--model", "gemini-test")
        self.assertEqual(result.returncode, 1)
        receipt = json.loads((self.root / "artifacts/receipt.json").read_text())
        self.assertEqual(receipt["model"], "gemini-test")
        self.assertEqual(receipt["version"], "unverified")
        self.assertEqual(receipt["scope"]["files"], [str(self.source_file.resolve())])
        self.assertEqual(receipt["prompt_purpose"], "Review the change.")
        self.assertFalse(self.invocation_file.exists())

    def test_malformed_json_is_failure(self) -> None:
        result = self.run_runner(stdout="not json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("malformed", result.stderr.lower())
        receipt = json.loads((self.root / "artifacts" / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["failure"], "malformed JSON")

    def test_empty_response_is_failure(self) -> None:
        result = self.run_runner(stdout='{"status":"SUCCESS","response":"   "}')

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty response", result.stderr.lower())

    def test_nonempty_error_is_failure(self) -> None:
        result = self.run_runner(stdout='{"status":"SUCCESS","response":"answer","error":"quota"}')

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())

    def test_missing_input_file_is_rejected_without_invoking_agy(self) -> None:
        self.prompt_file.unlink()
        result = self.run_runner()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prompt file", result.stderr.lower())
        self.assertFalse(self.invocation_file.exists())
        self.assertFalse((self.root / "artifacts").exists())

    def test_existing_output_dir_is_rejected(self) -> None:
        output_dir = self.root / "artifacts"
        output_dir.mkdir()
        result = subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--prompt-file",
                str(self.prompt_file),
                "--output-dir",
                str(output_dir),
                "--timeout",
                "3",
            ],
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not already exist", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
