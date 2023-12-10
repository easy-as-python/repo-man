from pathlib import Path
from unittest.mock import patch

from repo_man.commands import edit


def test_edit_clean(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(edit.edit)
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


@patch("repo_man.commands.edit.click.edit")
def test_edit_when_config_present(mock_edit, runner):
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()
        result = runner.invoke(edit.edit)
        assert result.exit_code == 0
        assert result.output == ""
        mock_edit.assert_called_once_with(filename="repo-man.cfg")
