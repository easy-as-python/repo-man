import configparser
from pathlib import Path
from typing import Callable

import typer

from repo_man.cli import cli


def test_known(runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo

[bar]
known = 
	some-other-repo

[ignore]
known = 
	yet-another-repo

"""
            )

        config = get_config()
        config.read("repo-man.cfg")

        result = runner.invoke(cli, ["sniff", "--known"], obj=config)
        assert result.exit_code == 0
        assert result.output == "bar\nfoo\n"


def test_unconfigured(runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()
        Path("some-other-repo").mkdir()
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo

"""
            )

        config = get_config()
        config.read("repo-man.cfg")

        result = runner.invoke(cli, ["sniff", "--unconfigured"], obj=config)
        assert result.exit_code == 0
        assert result.output == "some-other-repo\n"


def test_duplicates(runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo
	some-other-repo

[bar]
known = 
	some-repo
	some-other-repo
	yet-another-repo

"""
            )

        config = get_config()
        config.read("repo-man.cfg")

        result = runner.invoke(cli, ["sniff", "--duplicates"], obj=config)
        assert result.exit_code == 0
        assert result.output == "some-other-repo\nsome-repo\n"
