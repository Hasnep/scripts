import shlex
import subprocess
from pathlib import Path


def run_command(*command: str | Path, cwd: Path | None = None) -> None:
    command_str = [
        (y.absolute().as_posix() if isinstance(y, Path) else y) for y in command
    ]
    print(f"Running command: {' '.join(shlex.quote(x) for x in command_str)}")
    _ = subprocess.run(command_str, check=True, cwd=cwd)


def run_command_capture_output(*command: str | Path, cwd: Path | None = None) -> str:
    command_str = [(str(y) if isinstance(y, Path) else y) for y in command]
    print(f"Running command: {' '.join(shlex.quote(x) for x in command_str)}")
    return subprocess.run(
        command_str, check=True, cwd=cwd, capture_output=True
    ).stdout.decode()


__all__ = ["run_command", "run_command_capture_output"]
