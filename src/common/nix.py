from pathlib import Path

from .shell import run_command, run_command_capture_output


def build_devshell(cwd: Path) -> Path:
    print(f"Building devshell in `{cwd.absolute().as_posix()}`.")
    nix_store_path = run_command_capture_output(
        "nix",
        "build",
        "--no-link",
        "--print-out-paths",
        f"{cwd.absolute().as_posix()}#devShells.aarch64-darwin.default",
    )
    return Path(nix_store_path.strip())


def compare_nix_store_paths(path_a: Path, path_b: Path) -> None:
    print(f"Comparing Nix store paths in `{path_a}` and `{path_b}`.")
    run_command("nvd", "diff", path_a, path_b)


__all__ = ["build_devshell", "compare_nix_store_paths"]
