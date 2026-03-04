from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from droidtest.core import CommandResult, load_commands, run_adb_commands, split_results


class LoadCommandsTests(unittest.TestCase):
    def test_load_commands_skips_comments_and_blanks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "commands.txt"
            path.write_text("\n# comment\nshell getprop\n\n shell dumpsys battery \n", encoding="utf-8")
            self.assertEqual(load_commands(path), ["shell getprop", "shell dumpsys battery"])


class RunnerTests(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_adb_commands_includes_device(self, mocked_run):
        mocked_run.return_value.returncode = 0
        mocked_run.return_value.stdout = "ok"
        mocked_run.return_value.stderr = ""

        results = run_adb_commands(["shell getprop"], device_serial="emulator-5554")

        mocked_run.assert_called_once()
        call_args = mocked_run.call_args[0][0]
        self.assertEqual(call_args[:3], ["adb", "-s", "emulator-5554"])
        self.assertEqual(results[0].stdout, "ok")
        self.assertTrue(results[0].ok)

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
