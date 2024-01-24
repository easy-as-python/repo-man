import configparser

import click

from repo_man.utils import pass_config, ensure_config_file_exists


@click.command
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
@pass_config
def flavors(config: configparser.ConfigParser, repo: str):
    """List the configured types for a repository"""

    ensure_config_file_exists()

    found = set()

    for section in config.sections():
        if section == "ignore":
            continue
        if repo in config[section]["known"].split("\n"):
            found.add(section)

    for repository in sorted(found):
        click.echo(repository)
