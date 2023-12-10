# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- `init` command to create a new config file
- `edit` command to edit a config file manually
- `implode` command to remove configuration
- `sniff` command to inspect configuration and issues
- More confirmations for exceptional cases
- A start to unit tests

### Changed

- Move root options to new `sniff` command
- Move subcommands and utilities to individual modules
- Updated error and confirmation messaging
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
