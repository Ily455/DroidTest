# DroidTest

DroidTest is a small command-line runner for Android `adb` diagnostics. It reads commands from a file, executes them in sequence, and produces a clean pass/fail summary.

## What it does

- Runs a list of `adb` subcommands from a file
- Reports each command as PASS or FAIL
- Optionally filters output, stops on first failure, exports JSON reports
- Supports per-command timeouts and multi-device targeting

## Project structure

- `DroidTest.py` — entry point (backwards-compatible launcher)
- `droidtest/core.py` — command loading and execution logic
- `droidtest/cli.py` — argument parsing and output behavior
- `list.txt` — default command list
- `tests/` — unit tests
- `backup.py` — original single-file version, kept for reference

## Connect your Android device

1. Enable **Developer options**: Settings → About phone → tap **Build number** 7 times
2. Enable **USB debugging**: Settings → Developer options → USB debugging ON
3. Connect via USB and accept the RSA authorization prompt on the phone
4. Verify ADB sees your device:

```bash
adb devices
```

You should see your device serial with `device` status. If multiple devices are connected, use `--device <serial>`.

### Troubleshooting

- Device shows `unauthorized` → revoke USB debugging authorizations on the phone and reconnect
- No device appears → check USB cable, ensure `adb` is in PATH
- Restart ADB: `adb kill-server && adb start-server`

## Usage

```bash
python DroidTest.py [options]
```

| Flag | Description |
|------|-------------|
| `-c, --commands-file` | Path to commands file (default: `list.txt`) |
| `-d, --device` | ADB device serial (`adb -s`) |
| `-t, --timeout` | Per-command timeout in seconds |
| `-v, --verbose` | Print command output inline |
| `-S, --success-only` | Show only successful commands |
| `-F, --fail-only` | Show only failed commands (mutually exclusive with `-S`) |
| `--stop-on-failure` | Stop executing after the first failed command |
| `--json FILE` | Save full report as JSON |
| `--success-file FILE` | Append pass details to file |
| `--fail-file FILE` | Append fail details to file |

### Example

```bash
python DroidTest.py -v --timeout 8 --json report.json --fail-file failed.log
```

## Commands file format

Each non-empty, non-comment line is an `adb` subcommand. DroidTest prefixes `adb` automatically:

```text
# comments are allowed
shell getprop ro.product.model
shell dumpsys battery
shell df -h
```

## Running tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | All commands passed |
| `1` | No commands found in input file |
| `2` | One or more commands failed |

## Requirements

- Python 3.10+
- `adb` installed and available in PATH
- No third-party Python dependencies
