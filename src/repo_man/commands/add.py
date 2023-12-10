import configparser
from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import pass_config


@click.command
@click.option("-t", "--type", "repo_types", multiple=True, help="The type of the repository", required=True)
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
@pass_config
def add(config: configparser.ConfigParser, repo: str, repo_types: list[str]):
    """Add a new repository"""

    if not Path(REPO_TYPES_CFG).exists():
        click.confirm(click.style(f"No {REPO_TYPES_CFG} file found. Do you want to continue?", fg="yellow"), abort=True)

    new_types = [repo_type for repo_type in repo_types if repo_type not in config]
    if new_types:
        message = "\n\t".join(new_types)
        click.confirm(f"The following types are unknown and will be added:\n\n\t{message}\n\nContinue?", abort=True)

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
