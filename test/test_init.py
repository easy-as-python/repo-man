from pathlib import Path

from click.testing import CliRunner

from repo_man.cli import init


def test_init_clean():
    runner = CliRunner()

    with runner.isolated_filesystem():
        assert not Path("repo-man.cfg").exists()

        result = runner.invoke(init, ["."])
        assert result.exit_code == 0
        assert result.output == ""
        assert Path("repo-man.cfg").exists()


def test_init_with_existing_confirm():
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known =
    bar
"""
            )

        result = runner.invoke(init, ["."], input="Y")
        assert result.exit_code == 0
        assert result.output == "repo-man.cfg file already exists. Overwrite with empty configuration? [y/N]: Y\n"

        with open("repo-man.cfg") as config_file:
            assert config_file.read() == ""


def test_init_with_existing_no_confirm():
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known =
    bar
"""
            )

        result = runner.invoke(init, ["."], input="\n")
        assert result.exit_code == 1
        assert (
            result.output == "repo-man.cfg file already exists. Overwrite with empty configuration? [y/N]: \nAborted!\n"
        )

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[foo]
known =
    bar
"""
            )
