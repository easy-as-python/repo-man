import configparser
from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import get_valid_repo_types, parse_repo_types, pass_config


@click.command(name="list", help="The type of repository to manage")
@click.option("-t", "--type", "repo_type", type=click.Choice(get_valid_repo_types()), show_choices=False, required=True)
@pass_config
def list_repos(config: configparser.ConfigParser, repo_type: str):
    """List matching repositories"""

    if not Path(REPO_TYPES_CFG).exists():
        click.echo(click.style(f"No {REPO_TYPES_CFG} file found.", fg="red"))
        raise SystemExit(1)

    valid_repo_types = parse_repo_types(config)

    repos = sorted(valid_repo_types[repo_type])

    if len(repos) > 25:
        click.echo_via_pager("\n".join(repos))
    else:
        click.echo("\n".join(repos))
