from pathlib import Path

from repo_man.commands.flavors import flavors


def test_flavors_clean(runner, get_config):
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()
        config = get_config()
        result = runner.invoke(flavors, ["some-repo"], obj=config)
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


def test_flavors_when_configured(runner, get_config):
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo

[ignore]
known = 
	some-other-repo

"""
            )

        config = get_config()
        result = runner.invoke(flavors, ["some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == "foo\n"


def test_flavors_when_not_configured(runner, get_config):
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-other-repo

"""
            )

        config = get_config()
        result = runner.invoke(flavors, ["some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""


def test_flavors_when_ignored(runner, get_config):
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()

        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[ignore]
known = 
	some-repo

"""
            )

        config = get_config()
        result = runner.invoke(flavors, ["some-repo"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""
