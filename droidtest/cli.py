from __future__ import annotations

import argparse
import json
from pathlib import Path

from droidtest.core import load_commands, run_adb_commands, split_results


BANNER = r"""
  _____            _     _ _______        _
 |  __ \          (_)   | |__   __|      | |
 | |  | |_ __ ___  _  __| |  | | ___  ___| |_ ___ _ __
 | |  | | '__/ _ \| |/ _` |  | |/ _ \/ __| __/ _ \ '__|
 | |__| | | | (_) | | (_| |  | |  __/\__ \ ||  __/ |
 |_____/|_|  \___/|_|\__,_|  |_|\___||___/\__\___|_|
""".strip("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run and report Android adb diagnostic commands."
    )
    parser.add_argument("-c", "--commands-file", default="list.txt", help="Path to command file.")
    parser.add_argument("-d", "--device", help="ADB device serial to target (adb -s).")
    parser.add_argument("-t", "--timeout", type=float, default=None, help="Per-command timeout in seconds.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print stdout/stderr per command.")
    parser.add_argument("-S", "--success-only", action="store_true", help="Show only successful commands.")
    parser.add_argument("-F", "--fail-only", action="store_true", help="Show only failed commands.")
    parser.add_argument("--stop-on-failure", action="store_true", help="Stop execution after first failed command.")
    parser.add_argument("--json", dest="json_file", help="Write full results as JSON file.")
    parser.add_argument("--success-file", help="Append successful command details to a file.")
    parser.add_argument("--fail-file", help="Append failed command details to a file.")
    return parser


def _append_result(path: str, prefix: str, command: str, output: str) -> None:
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(f"{prefix}: {command}\n")
        if output:
            handle.write(output + "\n")
        handle.write("\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print(BANNER)

    commands = load_commands(args.commands_file)
    if not commands:
        print("No commands found in input file.")
        return 1

    results = []
    for result in run_adb_commands(commands, device_serial=args.device, timeout=args.timeout):
        results.append(result)

        if result.ok:
            if args.success_file:
                _append_result(args.success_file, "PASS", result.command, result.stdout)
        else:
            if args.fail_file:
                _append_result(args.fail_file, "FAIL", result.command, result.stderr)
            if args.stop_on_failure:
                break

        show = (not args.success_only and not args.fail_only) or (args.success_only and result.ok) or (
            args.fail_only and not result.ok
        )
        if show:
            status = "PASS" if result.ok else "FAIL"
            print(f"{status}: {result.command}")
            if args.verbose:
                body = result.stdout if result.ok else result.stderr
                if body:
                    print(body)

    success, failed = split_results(results)
    print(f"\nSummary: {len(success)} passed, {len(failed)} failed, {len(results)} total")

    if args.json_file:
        payload = {
            "summary": {"passed": len(success), "failed": len(failed), "total": len(results)},
            "results": [item.to_dict() for item in results],
        }
        Path(args.json_file).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
