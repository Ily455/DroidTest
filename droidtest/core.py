from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shlex
import subprocess
from typing import Iterable, Iterator


@dataclass
class CommandResult:
    command: str
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0

    def to_dict(self) -> dict:
        data = asdict(self)
        data["ok"] = self.ok
        return data


def load_commands(file_path: str | Path) -> list[str]:
    """Load commands from a file, skipping comments and blank lines."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Command file not found: {path}")

    commands: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        commands.append(line)
    return commands


def run_adb_commands(
    commands: Iterable[str],
    *,
    device_serial: str | None = None,
    timeout: float | None = None,
) -> Iterator[CommandResult]:
    """Yield a CommandResult for each adb command.

    FIX: changed from returning list[CommandResult] to Iterator[CommandResult].
    The previous implementation executed all commands upfront and returned a
    fully-evaluated list, which meant --stop-on-failure in the CLI had no effect
    on actual execution — it only stopped processing already-completed results.
    Yielding one result at a time lets the caller break early and truly halt
    further command execution.
    """
    for command in commands:
        adb_command = ["adb"]
        if device_serial:
            adb_command += ["-s", device_serial]
        adb_command += shlex.split(command)

        try:
            completed = subprocess.run(
                adb_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            result = CommandResult(
                command=command,
                returncode=completed.returncode,
                stdout=completed.stdout.strip(),
                stderr=completed.stderr.strip(),
            )
        except subprocess.TimeoutExpired as exc:
            # FIX: removed unnecessary isinstance(exc.stdout, str) check.
            # subprocess.run is called with text=True, so exc.stdout is always
            # str | None — the bytes branch was unreachable.
            result = CommandResult(
                command=command,
                returncode=124,
                stdout=(exc.stdout or "").strip(),
                stderr=f"Timed out after {timeout}s",
            )

        yield result


def split_results(
    results: Iterable[CommandResult],
) -> tuple[list[CommandResult], list[CommandResult]]:
    success: list[CommandResult] = []
    failed: list[CommandResult] = []
    for result in results:
        (success if result.ok else failed).append(result)
    return success, failed
