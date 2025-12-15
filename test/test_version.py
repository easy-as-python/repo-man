from unittest.mock import patch

from typer import testing

from repo_man.cli import cli


@patch("repo_man.cli.RELEASE_VERSION", "0.0.0")
def test_version(runner: testing.CliRunner) -> None:
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == "0.0.0"
