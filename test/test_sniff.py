import configparser
import os
from collections.abc import Callable
from pathlib import Path

from typer import testing

from repo_man.cli import cli


def test_known(runner: testing.CliRunner, get_config: Callable[[], configparser.ConfigParser], tmp_path: Path) -> None:
    repo = tmp_path / "some-repo"
    repo.mkdir()
    os.chdir(tmp_path)

    with open("repo-man.cfg", "w") as config_file:
        config_file.write(
            """[foo]
known =
	some-repo

[bar]
known =
	some-other-repo

[ignore]
known =
	yet-another-repo

"""
        )

    config = get_config()
    config.read("repo-man.cfg")

    result = runner.invoke(cli, ["sniff", "--known"], obj=config)
    assert result.exit_code == 0
    assert result.output == "bar\nfoo\n"


def test_unconfigured(
    runner: testing.CliRunner, get_config: Callable[[], configparser.ConfigParser], tmp_path: Path
) -> None:
    repo = tmp_path / "some-repo"
    repo.mkdir()
    other_repo = tmp_path / "some-other-repo"
    other_repo.mkdir()
    os.chdir(tmp_path)

    with open("repo-man.cfg", "w") as config_file:
        config_file.write(
            """[foo]
known =
	some-repo

"""
        )

    config = get_config()
    config.read("repo-man.cfg")

    result = runner.invoke(cli, ["sniff", "--unconfigured"], obj=config)
    assert result.exit_code == 0
    assert result.output == "some-other-repo\n"


def test_duplicates(
    runner: testing.CliRunner, get_config: Callable[[], configparser.ConfigParser], tmp_path: Path
) -> None:
    repo = tmp_path / "some-repo"
    repo.mkdir()
    other_repo = tmp_path / "some-other-repo"
    other_repo.mkdir()
    os.chdir(tmp_path)

    with open("repo-man.cfg", "w") as config_file:
        config_file.write(
            """[foo]
known =
	some-repo
	some-other-repo

[bar]
known =
	some-repo
	some-other-repo
	yet-another-repo

"""
        )

    config = get_config()
    config.read("repo-man.cfg")

    result = runner.invoke(cli, ["sniff", "--duplicates"], obj=config)
    assert result.exit_code == 0
    assert result.output == "some-other-repo\nsome-repo\n"
