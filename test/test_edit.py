import os
from pathlib import Path
from unittest.mock import Mock, patch

from typer import testing

from repo_man.cli import cli


def test_edit_clean(runner: testing.CliRunner, tmp_path: Path) -> None:
    os.chdir(tmp_path)

    result = runner.invoke(cli, ["edit"])
    assert result.exit_code == 1
    assert result.output == "No repo-man.cfg file found.\n"


@patch("repo_man.commands.edit.click.edit")
def test_edit_when_config_present(mock_edit: Mock, runner: testing.CliRunner, tmp_path: Path) -> None:
    os.chdir(tmp_path)

    Path("repo-man.cfg").touch()
    result = runner.invoke(cli, ["edit"])
    assert result.exit_code == 0
    assert result.output == ""
    mock_edit.assert_called_once_with(filename="repo-man.cfg")
