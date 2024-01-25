import configparser
from pathlib import Path
from typing import Callable

import click

from repo_man.commands.remove import remove


def test_remove_clean(runner: click.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
    some-repo
"""
            )

        config = get_config()
        result = runner.invoke(remove, ["-t", "foo", "some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""

        with open("repo-man.cfg") as config_file:
            assert config_file.read() == "[foo]\nknown = \n\n"


def test_remove_when_invalid_type(
    runner: click.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
    some-repo
"""
            )

        config = get_config()
        result = runner.invoke(remove, ["-t", "bar", "some-repo"], obj=config)
        assert result.exit_code == 2
        assert result.output.endswith(
            """Error: Invalid value: Invalid repository type 'bar'. Valid types are:

\tall
\tfoo
"""
        )

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[foo]
known = 
    some-repo
"""
            )


def test_remove_when_unused_type(
    runner: click.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
    some-repo

[bar]
known = 
    some-other-repo
"""
            )

        config = get_config()
        result = runner.invoke(remove, ["-t", "bar", "some-repo"], obj=config)
        assert result.exit_code == 1
        assert (
            result.output
            == """Repository 'some-repo' is not configured for type 'bar'. Continue? [y/N]: 
Aborted!
"""
        )
