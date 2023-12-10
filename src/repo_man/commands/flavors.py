import configparser
from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import pass_config


@click.command
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
@pass_config
def flavors(config: configparser.ConfigParser, repo: str):
    """List the configured types for a repository"""

    if not Path(REPO_TYPES_CFG).exists():
        click.echo(click.style(f"No {REPO_TYPES_CFG} file found.", fg="red"))
        raise SystemExit(1)

    found = set()

    for section in config.sections():
        if section == "ignore":
            continue
        if repo in config[section]["known"].split("\n"):
            found.add(section)

    for repository in sorted(found):
        click.echo(repository)
