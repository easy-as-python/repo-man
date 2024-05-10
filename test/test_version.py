from repo_man import cli


def test_version(runner, monkeypatch):
    monkeypatch.setattr(cli, "RELEASE_VERSION", "0.0.0")
    result = runner.invoke(cli.cli, ["--version"])
    assert result.exit_code == 0
    assert result.output.strip() == f"0.0.0"
