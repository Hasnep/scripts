{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];
      perSystem =
        {
          self',
          pkgs,
          inputs',
          ...
        }:
        {
          packages = {
            default = pkgs.python3.pkgs.buildPythonApplication {
              pname = "scripts";
              version = "0.0.0";
              format = "pyproject";

              src = ./.;
              propagatedBuildInputs = [
                pkgs.python3.pkgs.setuptools
                pkgs.python3.pkgs.setuptools-scm
              ];
            };
          };
          apps = {
            devshell-compare = {
              type = "app";
              program = pkgs.lib.getExe' self'.packages.default "devshell-compare";
            };
            devshell-upgrade = {
              type = "app";
              program = pkgs.lib.getExe' self'.packages.default "devshell-upgrade";
            };
            direnv-init = {
              type = "app";
              program = pkgs.lib.getExe' self'.packages.default "direnv-init";
            };
          };
          devShells.default = pkgs.mkShell {
            packages = [
              # keep-sorted start
              pkgs.actionlint
              pkgs.basedpyright
              pkgs.keep-sorted
              pkgs.nixfmt
              pkgs.nodePackages.prettier
              pkgs.prek
              pkgs.python3Packages.pre-commit-hooks
              pkgs.ratchet
              pkgs.ruff
              pkgs.toml-sort
              # keep-sorted end
            ];
            shellHook = "prek install --overwrite";
          };
          formatter = pkgs.nixfmt-tree;
        };
    };
}
