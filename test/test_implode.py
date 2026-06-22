import os
from pathlib import Path

from typer import testing

from repo_man.cli import cli


def test_implode_when_config_present_confirm(runner: testing.CliRunner, tmp_path: Path) -> None:
    os.chdir(tmp_path)

    Path("repo-man.cfg").touch()

    result = runner.invoke(cli, ["implode", "."], input="Y\n")
    assert result.exit_code == 0
    assert result.output == "Are you sure you want to do this? [y/N]: Y\n"
    assert not Path("repo-man.cfg").exists()


def test_implode_when_config_not_present_confirm(runner: testing.CliRunner, tmp_path: Path) -> None:
    os.chdir(tmp_path)

    result = runner.invoke(cli, ["implode", "."], input="Y\n")
    assert result.exit_code == 0
    assert result.output == "Are you sure you want to do this? [y/N]: Y\n"


def test_implode_when_config_present_no_confirm(runner: testing.CliRunner, tmp_path: Path) -> None:
    os.chdir(tmp_path)

    Path("repo-man.cfg").touch()

    result = runner.invoke(cli, ["implode", "."], input="\n")
    assert result.exit_code == 1
    assert result.output == """Are you sure you want to do this? [y/N]: \nAborted.\n"""
    assert Path("repo-man.cfg").exists()
