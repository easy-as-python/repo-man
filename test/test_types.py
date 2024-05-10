import configparser
from pathlib import Path
from typing import Callable

import typer

from repo_man.cli import cli


def test_types_clean(runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()
        config = get_config()
        result = runner.invoke(cli, ["types", "some-repo"], obj=config)
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


def test_types_when_configured(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo

[ignore]
known = 
	some-other-repo

"""
            )

        config = get_config()
        result = runner.invoke(cli, ["types", "some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == "foo\n"


def test_types_when_not_configured(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-other-repo

"""
            )

        config = get_config()
        result = runner.invoke(cli, ["types", "some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""


def test_types_when_ignored(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[ignore]
known = 
	some-repo

"""
            )

        config = get_config()
        result = runner.invoke(cli, ["types", "some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""
