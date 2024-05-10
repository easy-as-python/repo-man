import configparser
from typing import Callable
from unittest.mock import Mock, patch

import typer

from repo_man.cli import cli


def test_list_repos_clean(runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]) -> None:
    with runner.isolated_filesystem():
        config = get_config()
        result = runner.invoke(cli, ["list", "-t", "all"], obj=config)
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


def test_list_repos_with_matches(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo
	some-other-repo

"""
            )

        config = get_config()
        result = runner.invoke(cli, ["list", "-t", "all"], obj=config)
        assert result.exit_code == 0
        assert (
            result.output
            == """some-other-repo
some-repo
"""
        )


@patch("repo_man.commands.list_repos.click.echo_via_pager")
def test_list_repos_when_long(
    mock_echo_via_pager: Mock, runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    all_repos = """some-repo-1
some-repo-2
some-repo-3
some-repo-4
some-repo-5
some-repo-6
some-repo-7
some-repo-8
some-repo-9
some-repo-10
some-repo-11
some-repo-12
some-repo-13
some-repo-14
some-repo-15
some-repo-16
some-repo-17
some-repo-18
some-repo-19
some-repo-20
some-repo-21
some-repo-22
some-repo-23
some-repo-24
some-repo-25
some-repo-26"""

    config_list = "\n	".join(all_repos.split("\n"))

    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                f"""[foo]
known = 
	{config_list}

"""
            )

        config = get_config()
        result = runner.invoke(cli, ["list", "-t", "all"], obj=config)
        assert result.exit_code == 0
        mock_echo_via_pager.assert_called_once_with("\n".join(sorted(all_repos.split("\n"))))


def test_list_repos_for_multiple_tags(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
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
        result = runner.invoke(cli, ["list", "-t", "foo", "-t", "bar"], obj=config)
        assert result.exit_code == 0
        assert (
            result.output
            == """some-other-repo
some-repo
"""
        )


def test_list_repos_when_invalid_type(
    runner: typer.testing.CliRunner, get_config: Callable[[], configparser.ConfigParser]
) -> None:
    with runner.isolated_filesystem():
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
        result = runner.invoke(cli, ["list", "-t", "baz"], obj=config)
        assert result.exit_code == 2
        print(result.output)
        assert "│ Invalid value: Invalid repository type 'baz'. Valid types are:" in result.output
        assert "│         all" in result.output
        assert "│         foo" in result.output
        assert "│         bar" in result.output
