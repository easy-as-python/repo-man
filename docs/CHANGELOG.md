# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

- Move from `setup.cfg` to `pyproject.toml` for package configuration
- Move from `black` to `ruff` for formatting
- Move from `isort` to `ruff` for import sorting
- Sort repos of a given type alphabetically when adding a repo to that type

## [0.0.11] - 2024-10-09

### Added

- Add support for Python 3.10, 3.11, and 3.13

## [0.0.10] - 2024-05-10

### Changed

- Use Typer for command-line parsing

## [0.0.9] - 2024-04-17

### Fixed

- Fix incorrect help string for the `list` command

### Changed

- Update `flavors` command and terminology to `types`

## [0.0.8] - 2024-02-12

### Added

- `remove` command to remove a repository from one or more types

### Changed

- Use `strict` for mypy type checking on source and tests
- Add isort to order imports consistently

## [0.0.7] - 2024-01-21

### Added

- `list` can now accept multiple `--type` parameters to list multiple repository types

## [0.0.6] - 2023-12-10

### Added

- `init` command to create a new config file
- `edit` command to edit a config file manually
- `implode` command to remove configuration
- `sniff` command to inspect configuration and issues
- More confirmations for exceptional cases
- Unit tests

### Changed

- Move root options to new `sniff` command
- Move subcommands and utilities to individual modules
- Updated error and confirmation messaging
- Exit with status code 1 in more cases
- Open long repo lists in pager

## [0.0.5] - 2023-12-09

### Changed

- Use Click for command-line parsing

### Added

- `repo-man add` can now take multiple `--type` values to add a repo to many flavors at once

## [0.0.4] - 2023-11-14

### Changed

- Use `repo-man` stylization consistently (and `repo_man` where needed for Python). This changes the executable command name, most notably.

### Fixed

- Fix `KeyError` when config doesn't contain an `ignore` section

## [0.0.3] - 2023-11-07

### Changed

- Listing repositories of a given flavor is now the `list` subcommand

### Added

- List flavors of a given repository using the `flavors` subcommand
- Configure a repository for a flavor using the `add` subcommand

## [0.0.2] - 2023-11-07

### Fixed

- Update help text to reflect repo-man program name
- Remove useless help text epilog

## [0.0.1] - 2023-11-07

### Added

- List repositories configured with a given flavor
- List repositories configured with more than one flavor
- List repositories with no configured flavor
- List configured flavors
