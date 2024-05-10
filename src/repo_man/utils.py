import configparser
from pathlib import Path

import typer

from repo_man.consts import REPO_TYPES_CFG


def parse_repo_types(config: configparser.ConfigParser) -> dict[str, set[str]]:
    repo_types: dict[str, set[str]] = {"all": set()}
    for section in config.sections():
        repos = {repo for repo in config[section]["known"].split("\n") if repo}
        repo_types[section] = repos
        if section != "ignore":
            repo_types["all"].update(repos)

    return repo_types


def get_valid_repo_types() -> list[str]:
    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    valid_repo_types = parse_repo_types(config)
    return sorted(set(valid_repo_types.keys()))


def ensure_config_file_exists(confirm: bool = False) -> None:
    if not Path(REPO_TYPES_CFG).exists():
        if confirm:
            typer.confirm(
                typer.style(f"No {REPO_TYPES_CFG} file found. Do you want to continue?", fg="yellow"), abort=True
            )
        else:
            typer.secho(f"No {REPO_TYPES_CFG} file found.", fg="red")
            raise SystemExit(1)
