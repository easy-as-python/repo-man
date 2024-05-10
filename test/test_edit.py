from pathlib import Path
from unittest.mock import Mock, patch

import typer

from repo_man.cli import cli


def test_edit_clean(runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["edit"])
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


@patch("repo_man.commands.edit.typer.edit")
def test_edit_when_config_present(mock_edit: Mock, runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()
        result = runner.invoke(cli, ["edit"])
        assert result.exit_code == 0
        assert result.output == ""
        mock_edit.assert_called_once_with(filename="repo-man.cfg")
