import typer

from repo_man.utils import get_valid_repo_types


def test_get_valid_repo_types(runner: typer.testing.CliRunner) -> None:
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
    some-repo
"""
            )

        assert get_valid_repo_types() == ["all", "foo"]
