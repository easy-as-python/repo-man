from pathlib import Path

from repo_man.commands.add import add


def test_add_clean_confirm(runner, get_config):
    with runner.isolated_filesystem():
        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type"], input="Y\nY\n", obj=config)
        assert result.exit_code == 0
        assert (
            result.output
            == """No repo-man.cfg file found. Do you want to continue? [y/N]: Y
The following types are unknown and will be added:

	some-type

Continue? [y/N]: Y
"""
        )

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[some-type]
known = 
	some-repo

"""
            )


def test_add_clean_no_confirm_new_file(runner, get_config):
    with runner.isolated_filesystem():
        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type"], input="\n", obj=config)
        assert result.exit_code == 1
        assert (
            result.output
            == """No repo-man.cfg file found. Do you want to continue? [y/N]: 
Aborted!
"""
        )


def test_add_with_existing_file(runner, get_config):
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known =
    bar
"""
            )

        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type"], input="Y\n", obj=config)
        assert result.exit_code == 0
        assert (
            result.output
            == """The following types are unknown and will be added:

	some-type

Continue? [y/N]: Y
"""
        )

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[foo]
known = 
	bar

[some-type]
known = 
	some-repo

"""
            )


def test_add_with_existing_file_and_type(runner, get_config):
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[some-type]
known =
    bar
"""
            )

        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[some-type]
known = 
	bar
	some-repo

"""
            )


def test_add_multiple_types(runner, get_config):
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[some-type]
known =
    bar
"""
            )

        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type", "-t", "some-other-type"], input="Y\n", obj=config)
        assert result.exit_code == 0
        assert (
            result.output
            == """The following types are unknown and will be added:

	some-other-type

Continue? [y/N]: Y
"""
        )

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[some-type]
known = 
	bar
	some-repo

[some-other-type]
known = 
	some-repo

"""
            )


def test_add_no_action_needed(runner, get_config):
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[some-type]
known =
    some-repo
"""
            )

        (Path(".") / "some-repo").mkdir()
        config = get_config()
        result = runner.invoke(add, ["some-repo", "-t", "some-type"], obj=config)
        assert result.exit_code == 0
        assert result.output == ""

        with open("repo-man.cfg") as config_file:
            assert (
                config_file.read()
                == """[some-type]
known = 
	some-repo

"""
            )
