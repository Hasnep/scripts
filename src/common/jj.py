from pathlib import Path

from .shell import run_command


def jj_edit(revset: str, cwd: Path) -> None:
    print(f"Switching to revset `{revset}` in `{cwd}`.")
    run_command("jj", "edit", *("--revset", revset), cwd=cwd)


__all__ = ["jj_edit"]
