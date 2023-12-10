from pathlib import Path

from repo_man.commands.sniff import sniff


def test_known(runner, get_config):
    with runner.isolated_filesystem():
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

        result = runner.invoke(sniff, ["--known"], obj=config)
        assert result.exit_code == 0
        assert result.output == "bar\nfoo\n"


def test_unconfigured(runner, get_config):
    with runner.isolated_filesystem():
        Path("some-repo").mkdir()
        Path("some-other-repo").mkdir()
        with open("repo-man.cfg", "w") as config_file:
            config_file.write(
                """[foo]
known = 
	some-repo

"""
            )

        config = get_config()
        config.read("repo-man.cfg")

        result = runner.invoke(sniff, ["--unconfigured"], obj=config)
        assert result.exit_code == 0
        assert result.output == "some-other-repo\n"


def test_duplicates(runner, get_config):
    with runner.isolated_filesystem():
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

        result = runner.invoke(sniff, ["--duplicates"], obj=config)
        assert result.exit_code == 0
        assert result.output == "some-other-repo\nsome-repo\n"
