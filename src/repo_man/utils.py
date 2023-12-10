import configparser

import click

from repo_man.consts import REPO_TYPES_CFG


pass_config = click.make_pass_decorator(configparser.ConfigParser)


def parse_repo_types(config: configparser.ConfigParser) -> dict[str, set[str]]:
    repo_types: dict[str, set[str]] = {"all": set()}
    for section in config.sections():
        repos = {repo for repo in config[section]["known"].split("\n") if repo}
        repo_types[section] = repos
        if section != "ignore":
            repo_types["all"].update(repos)

    return repo_types


def get_valid_repo_types():
    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)
    return sorted(set(valid_repo_types.keys()))
