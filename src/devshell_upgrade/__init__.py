import argparse
from pathlib import Path
from typing import cast

from common.nix import build_devshell, compare_nix_store_paths
from common.shell import run_command


def get_cli_args() -> tuple[bool, Path]:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--commit", action="store_true", default=True)
    _ = parser.add_argument("--no-commit", action="store_true", default=False)
    _ = parser.add_argument("dir", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    match cast("bool", args.commit), cast("bool", args.no_commit):
        case True, False:
            do_commit = True
        case False, True:
            do_commit = False
        case _:
            raise ValueError("Invalid arguments")
    return do_commit, cast("Path", args.dir)


def main() -> int:
    do_commit, cwd = get_cli_args()

    path_a = build_devshell(cwd=cwd)

    if do_commit:
        dot_jj_dir = cwd / ".jj"
        if dot_jj_dir.exists() and dot_jj_dir.is_dir():
            print("Creating a new commit for the changes...")
            run_command("jj", "commit", *("--message", "Upgrade flake inputs"), cwd=cwd)
        else:
            print(
                "No commit was created because the repository is not a jujutsu repository."
            )
            return 1
    else:
        print("Skipping commit...")

    print("Upgrading flake...")
    run_command("nix", "flake", "update", cwd=cwd)
    path_b = build_devshell(cwd=cwd)

    print("Comparing devshells...")
    compare_nix_store_paths(path_a, path_b)
    return 0
