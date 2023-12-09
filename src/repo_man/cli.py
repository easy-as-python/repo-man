import configparser
import sys
from pathlib import Path
from typing import NoReturn, Union

import click


FAIL = "\033[91m"
ENDC = "\033[0m"
REPO_TYPES_CFG = "repo-man.cfg"


def check_if_allowed(path: Path) -> Union[bool, NoReturn]:
    if REPO_TYPES_CFG not in (str(item) for item in path.iterdir()):
        print(f"{FAIL}The current directory is not configured for repository management{ENDC}")
        sys.exit(1)

    return True


def parse_repo_types(config: configparser.ConfigParser) -> dict[str, set[str]]:
    repo_types: dict[str, set[str]] = {"all": set()}
    for section in config.sections():
        repos = {repo for repo in config[section]["known"].split("\n") if repo}
        repo_types[section] = repos
        if section != "ignore":
            repo_types["all"].update(repos)

    return repo_types


def check_missing_repos(path: Path, repo_types: dict[str, set[str]]) -> None:
    missing = set()
    directories = {str(directory) for directory in path.iterdir()}

    for repo in sorted(repo_types["all"]):
        if repo not in directories:
            missing.add(repo)

    if missing:
        print(f"{FAIL}The following repositories are configured but do not exist:")
        for repo in missing:
            print(f"\t{repo}")
        sys.exit(1)

    return None


def get_valid_repo_types():
    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)
    return sorted(set(valid_repo_types.keys()))


def main():
    path = Path(".")
    check_if_allowed(path)

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)
    check_missing_repos(path, valid_repo_types)

    cli()


@click.group(invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="repo-man")
@click.option("-k", "--known", is_flag=True, help="List known repository types")
@click.option("-u", "--unconfigured", is_flag=True, help="List repositories without a configured type")
@click.option("-d", "--duplicates", is_flag=True, help="List repositories with more than one configured type")
# @click.option("-v", "--verbose", "verbosity", count=True)
def cli(known: bool, unconfigured: bool, duplicates: bool):
    """Manage repositories of different types"""

    path = Path(".")
    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)

    if known:
        known_repo_types = sorted(
            [repo_type for repo_type in valid_repo_types if repo_type != "all" and repo_type != "ignore"]
        )
        for repo_type in known_repo_types:
            print(repo_type)

    if unconfigured:
        for directory in sorted(path.iterdir()):
            if (
                directory.is_dir()
                and str(directory) not in valid_repo_types["all"]
                and str(directory) not in valid_repo_types.get("ignore", [])
            ):
                print(directory)

    if duplicates:
        seen = set()
        for repo_type in valid_repo_types:
            if repo_type != "all" and repo_type != "ignore":
                for repo in valid_repo_types[repo_type]:
                    if repo in seen:
                        print(repo)
                    seen.add(repo)


@cli.command(name="list", help="The type of repository to manage")
@click.option("-t", "--type", "repo_type", type=click.Choice(get_valid_repo_types()), show_choices=False, required=True)
def list_repos(repo_type: str):
    """List matching repositories"""

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)

    for repo in valid_repo_types[repo_type]:
        print(repo)

    return None


@cli.command
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
def flavors(repo: str):
    """List the configured types for a repository"""

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)

    found = set()

    for section in config.sections():
        if section == "ignore":
            continue
        if repo in config[section]["known"].split("\n"):
            found.add(section)

    for repository in sorted(found):
        print(repository)


@cli.command
@click.option("-t", "--type", "repo_types", multiple=True, help="The type of the repository", required=True)
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
def add(repo: str, repo_types: list):
    """Add a new repository"""

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)

    for repo_type in repo_types:
        if repo_type in config:
            original_config = config[repo_type]["known"]
        else:
            original_config = ""
            config.add_section(repo_type)

        if "known" not in config[repo_type] or repo not in config[repo_type]["known"].split("\n"):
            config.set(repo_type, "known", f"{original_config}\n{repo}")

    with open(REPO_TYPES_CFG, "w") as config_file:
        config.write(config_file)
