import argparse
from pathlib import Path
from typing import cast

from common.jj import jj_edit
from common.nix import build_devshell, compare_nix_store_paths


def get_cli_args() -> tuple[str, str, Path]:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("revset_a", type=str)
    _ = parser.add_argument("revset_b", type=str)
    _ = parser.add_argument("dir", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    return (
        cast("str", args.revset_a),
        cast("str", args.revset_b),
        cast("Path", args.dir),
    )


def main() -> int:
    revset_a, revset_b, cwd = get_cli_args()

    jj_edit(revset_a, cwd=cwd)
    path_a = build_devshell(cwd=cwd)

    jj_edit(revset_b, cwd=cwd)
    path_b = build_devshell(cwd=cwd)

    print("Comparing devshells...")
    compare_nix_store_paths(path_a, path_b)
    return 0
