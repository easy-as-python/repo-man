# 4. Use consistent repo-man stylization

Date: 2023-11-14

## Status

Accepted

## Context

It is often nice to use a single word for shell command names and Python package names.
If the name is short enough to work as a single word it is probably usable and memorable.
The `repoman` name was already taken on the Python Package Index, but `repo-man` was available.

As the maintainer I have already tripped on the fact that there exist both `repo-man` and `repoman` instances in this project.
Using a consistent name stylization relieves this friction.

## Decision

Use `repo-man` and its Python-compatible equivalent `repo_man` consistently for everything.

## Consequences

- The shell command name most notably changes from `repoman` to `repo-man`
- The Python package import name changes from `repoman` to `repo_man`
- The config file can be renamed to better associate it with the command that uses it
- Confusion will be minimized about stylization; it's always two-worded
- Those using tab completion in their shell should be minimally impacted
- Those using the command in scripts will need to update it
- There is little utility to using the Python package directly at present, so little impact is expected
