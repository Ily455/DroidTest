from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from droidtest.core import CommandResult, load_commands, run_adb_commands, split_results


class LoadCommandsTests(unittest.TestCase):
    def test_load_commands_skips_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commands.txt"
            path.write_text("\n# comment\nshell getprop\n\n shell dumpsys battery \n", encoding="utf-8")
            self.assertEqual(load_commands(path), ["shell getprop", "shell dumpsys battery"])

    def test_load_commands_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_commands("/nonexistent/path/commands.txt")


class RunnerTests(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_adb_commands_includes_device(self, mocked_run):
        mocked_run.return_value.returncode = 0
        mocked_run.return_value.stdout = "ok"
        mocked_run.return_value.stderr = ""

        # FIX: run_adb_commands is now a generator — wrap in list() to evaluate it
        results = list(run_adb_commands(["shell getprop"], device_serial="emulator-5554"))

        mocked_run.assert_called_once()
        call_args = mocked_run.call_args[0][0]
        self.assertEqual(call_args[:3], ["adb", "-s", "emulator-5554"])
        self.assertEqual(results[0].stdout, "ok")
        self.assertTrue(results[0].ok)

    @patch("subprocess.run")
    def test_stop_on_failure_halts_execution(self, mocked_run):
        """--stop-on-failure must stop executing commands, not just stop reporting."""
        mocked_run.return_value.returncode = 1
        mocked_run.return_value.stdout = ""
        mocked_run.return_value.stderr = "error"

        gen = run_adb_commands(["shell cmd1", "shell cmd2", "shell cmd3"])
        first = next(gen)  # consume one result

        self.assertFalse(first.ok)
        # generator should not have executed cmd2/cmd3 yet
        self.assertEqual(mocked_run.call_count, 1)

    @patch("subprocess.run")
    def test_timeout_returns_returncode_124(self, mocked_run):
        import subprocess
        exc = subprocess.TimeoutExpired(cmd=["adb", "shell", "getprop"], timeout=5)
        exc.stdout = "partial"
        exc.stderr = None
        mocked_run.side_effect = exc

        results = list(run_adb_commands(["shell getprop"], timeout=5))

        self.assertEqual(results[0].returncode, 124)
        self.assertEqual(results[0].stdout, "partial")
        self.assertIn("Timed out", results[0].stderr)

    def test_split_results(self):
        items = [
            CommandResult("shell ok", 0, "ok", ""),
            CommandResult("shell bad", 1, "", "error"),
        ]
        success, failed = split_results(items)
        self.assertEqual(len(success), 1)
        self.assertEqual(len(failed), 1)


if __name__ == "__main__":
    unittest.main()
