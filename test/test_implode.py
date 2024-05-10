from pathlib import Path

import typer

from repo_man.cli import cli


def test_implode_when_config_present_confirm(runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()

        result = runner.invoke(cli, ["implode", "."], input="Y\n")
        assert result.exit_code == 0
        assert result.output == "Are you sure you want to do this? [y/N]: Y\n"
        assert not Path("repo-man.cfg").exists()


def test_implode_when_config_not_present_confirm(runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["implode", "."], input="Y\n")
        assert result.exit_code == 0
        assert result.output == "Are you sure you want to do this? [y/N]: Y\n"


def test_implode_when_config_present_no_confirm(runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()

        result = runner.invoke(cli, ["implode", "."], input="\n")
        assert result.exit_code == 1
        assert (
            result.output
            == """Are you sure you want to do this? [y/N]: 
Aborted.
"""
        )
        assert Path("repo-man.cfg").exists()
