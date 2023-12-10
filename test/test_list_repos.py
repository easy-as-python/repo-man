import configparser

from repo_man.commands.list_repos import list_repos


def test_list_repos_clean(runner, get_config):
    with runner.isolated_filesystem():
        config = get_config()
        result = runner.invoke(list_repos, ["-t", "all"], obj=config)
        assert result.exit_code == 1
        assert result.output == "No repo-man.cfg file found.\n"


def test_list_repos_with_matches(runner, get_config):
    with runner.isolated_filesystem():
        with open("repo-man.cfg", "w") as config_file:
            config_file.write("""[foo]
known = 
	some-repo
	some-other-repo

""")

        config = get_config()
        result = runner.invoke(list_repos, ["-t", "all"], obj=config)
        assert result.exit_code == 0
        assert result.output == """some-other-repo
some-repo
"""
