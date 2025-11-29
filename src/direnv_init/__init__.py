import argparse
from pathlib import Path
from typing import cast

from common.shell import run_command


def get_cli_args() -> Path:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("dir", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    return cast("Path", args.dir).absolute()


def main() -> int:
    cwd = get_cli_args()

    # Check if the repository is a jujutsu repository
    dot_jj_dir = cwd / ".jj"
    if not (dot_jj_dir.exists() and dot_jj_dir.is_dir()):
        print(f"The directory `{cwd}` is not a jujutsu repository.")
        return 1

    # Git ignore file
    git_info_exclude_file = cwd / ".git" / "info" / "exclude"
    if not (git_info_exclude_file.exists() and git_info_exclude_file.is_file()):
        print(f"Creating git exclude file `{git_info_exclude_file}`.")
        _ = git_info_exclude_file.write_text("")

    git_info_exclude_file_lines = git_info_exclude_file.read_text().splitlines()
    if ".envrc" not in git_info_exclude_file_lines:
        git_info_exclude_file_lines = [*git_info_exclude_file_lines, ".envrc"]
        print(f"Adding .envrc to `{git_info_exclude_file}`.")
        _ = git_info_exclude_file.write_text("\n".join(git_info_exclude_file_lines))
    else:
        print(f".envrc is already in `{git_info_exclude_file}`.")

    # .envrc file
    dot_env_rc_file = cwd / ".envrc"
    if not (dot_env_rc_file.exists() and dot_env_rc_file.is_file()):
        print(f"Creating .envrc file `{dot_env_rc_file}`.")
        _ = dot_env_rc_file.write_text("use flake\n")
        run_command("direnv", "allow", cwd=cwd)
    else:
        print(f".envrc file `{dot_env_rc_file}` already exists.")

    return 0
