# 5. Use Click for CLI parsing

Date: 2023-12-09

## Status

Accepted

Superseded by [7. Use Typer for CLI parsing](0007-use-typer-for-cli-parsing.md)

## Context

Parsing command-line arguments is a challenging problem.
A tool of sufficient complexity may need to expose its behavior through arguments, options, and subcommands.
It may also need to perform common validations such as the existence of files and a controlled vocabulary of option values.
Doing this with `argparse` works up to a point, but becomes very difficult to reason about very quickly.

An ideal outcome is that each command can be reasoned about on its own, written in a compact form that just about fits on a screen.
A contributor should be able to see the name of the command, whether it's a subcommand, what options and arguments it takes, without losing the context.
Common validations are abstracted such that they can be supplied in short forms with minimal duplication.

A solution will provide a testable way of building a CLI so that the behavior of the tool can be verified.

## Decision

Use the Click package for command-line parsing.

## Consequences

- Cognitive load drops significantly to increase confidence in adding new features
- Subcommands can be generated quickly using `@click.group`
- Validations can be generated quickly using `click.Choice`, `required=True`, and so on
- Arguments and options can be generated quickly using `@click.argument` and `@click.option`
- `CliRunner` can be used for testing
