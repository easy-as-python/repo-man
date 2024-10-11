# Contributing to repo-man

Thank you for your interest in improving repo-man!
Please read these guidelines to see how best to contribute to the project's success.

## Source code issues

If you've discovered an issue with the code in this repository, please [open an issue](https://github.com/easy-as-python/repo-man/issues/new/choose).
Or, if you have time, please consider forking this repository and opening a pull request with the fix!

## Questions

If you just have a question or would like to discuss ideas, [start a discussion](https://github.com/easy-as-python/repo-man/discussions/new).

## Code of conduct

Please read the [code of conduct](../CODE_OF_CONDUCT.md) before contributing to this repository.

## Local development

This section covers how to work with the project when developing changes locally.

### Running

To run repo-man as a command-line interface (CLI) locally, you need to install the package.
You can install the package in a Python virtual environment using your preferred method, or use [pipx](https://pipx.pypa.io/stable/).
You can use the `-e` flag in either pip or pipx to install repo-man from the project directory as an editable package so that any changes you make will be reflected the next time you use the CLI.
If using a virtual environment, be sure the environment is activated before trying to use the CLI so that the `repo-man` command will be on your `$PATH`.

### Testing

The test suite runs using [tox](https://tox.wiki).
You can install tox into the same virtual environment you use to install the project, or you can install tox using pipx as well.
Once you've installed tox, you can run the `tox` command in the root of the project to run unit tests with coverage.

### Linting, type checking, and formatting

Several other project development activities such as linting, type checking, and formatting are also available as tox environments.
You can see all available tasks in `pyproject.toml`.
These will be run when you open a pull request, and the checks will fail if you haven't fixed any issues locally.
If this happens, run the tasks locally to find and fix any issues, then push your changes.
