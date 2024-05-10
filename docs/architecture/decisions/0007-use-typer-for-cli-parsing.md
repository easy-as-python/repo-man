# 7. Use Typer for CLI parsing

Date: 2024-05-10

## Status

Accepted

Supersedes [5. Use Click for CLI parsing](0005-use-click-for-cli-parsing.md)

## Context

Type safety is important to maintainability and correctness of code, especially in systems that accept arbitrary user input.
Command-line arguments and options in most CLI frameworks can be annotated with type hints, but many frameworks require specifying information about the CLI arguments and the handler function arguments in a redundant way.
Typer is a library that uses Python type hints to generate a CLI parser, reducing the amount of boilerplate code needed to create a CLI.

## Decision

Use Typer for CLI parsing in the project.

## Consequences

- Developers can use type hints to specify the types of CLI arguments and options.
- repo-man can be composed into other Typer-based applications.
