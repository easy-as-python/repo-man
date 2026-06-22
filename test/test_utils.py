import os
from pathlib import Path

from typer import testing

from repo_man.utils import get_valid_repo_types


def test_get_valid_repo_types(runner: testing.CliRunner, tmp_path: Path) -> None:
    repo = tmp_path / "some-repo"
    repo.mkdir()
    os.chdir(tmp_path)

    with open("repo-man.cfg", "w") as config_file:
        config_file.write(
            """[foo]
known =
    some-repo
"""
        )

    assert get_valid_repo_types() == ["all", "foo"]
