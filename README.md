# DroidTest

DroidTest is a small command-line runner for Android `adb` diagnostics. It reads commands from a file, executes them in sequence, and produces a clean pass/fail summary.

## What was improved

- Refactored into a package structure (`droidtest/`) instead of one large script.
- Safer command parsing with `shlex.split`.
- Better command file parsing (ignores comments and blank lines).
- Optional per-command timeout.
- Optional `adb -s <serial>` device targeting.
- Optional stop-on-first-failure mode.
- JSON report export.
- Consistent process exit codes (`0` success, `2` when any command fails).

## Project structure

- `DroidTest.py` — backward-compatible launcher.
- `droidtest/core.py` — command loading and execution logic.
- `droidtest/cli.py` — argument parsing and output behavior.
- `list.txt` — default command list.
- `tests/` — unit tests.

## Usage

```bash
python DroidTest.py [options]
```

### Key options

- `-c, --commands-file` Path to commands list file (default: `list.txt`)
- `-d, --device` ADB device serial (`adb -s ...`)
- `-t, --timeout` Per-command timeout in seconds
- `-v, --verbose` Print command output inline
- `-S, --success-only` Print only successful commands
- `-F, --fail-only` Print only failed commands
- `--stop-on-failure` Stop after first failed command
- `--json FILE` Save full execution report as JSON
- `--success-file FILE` Append pass details to file
- `--fail-file FILE` Append failure details to file

### Example

```bash
python DroidTest.py -v --timeout 8 --json report.json --fail-file failed.log
```

## Commands file format

The default command file is `list.txt`. Each non-empty, non-comment line should be an `adb` subcommand:

```text
# comments are allowed
shell getprop ro.product.model
shell dumpsys battery
```

DroidTest prefixes each line with `adb` automatically.

## Running tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```
