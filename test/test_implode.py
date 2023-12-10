from pathlib import Path

from repo_man.commands.implode import implode


def test_implode_when_config_present_confirm(runner):
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()

        result = runner.invoke(implode, ["."], input="Y\n")
        assert result.exit_code == 0
        assert result.output == "Are you sure you want to do this? [y/N]: Y\n"
        assert not Path("repo-man.cfg").exists()


def test_implode_when_config_not_present_confirm(runner):
    with runner.isolated_filesystem():
        result = runner.invoke(implode, ["."], input="Y\n")
        assert result.exit_code == 0
        assert result.output == "Are you sure you want to do this? [y/N]: Y\n"


def test_implode_when_config_present_no_confirm(runner):
    with runner.isolated_filesystem():
        Path("repo-man.cfg").touch()

        result = runner.invoke(implode, ["."], input="\n")
        assert result.exit_code == 1
        assert (
            result.output
            == """Are you sure you want to do this? [y/N]: 
Aborted!
"""
        )
        assert Path("repo-man.cfg").exists()
