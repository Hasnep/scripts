# Scripts

Various personal scripts.

## `devshell-compare`

Compares the Nix devshell of two different jj revisions.

## `devshell-upgrade`

Upgrades the Nix devshell and displays the diff, committing the changes if the directory is a jj repository.

## `direnv-init`

Initializes the direnv environment for the current directory by adding the `.envrc` file to the repository's `.git/info/exclude` file and adding the `use flake` directive to the `.envrc` file.
