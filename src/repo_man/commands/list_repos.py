import configparser
from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import parse_repo_types, pass_config


@click.command(name="list", help="The type of repository to manage")
@click.option("-t", "--type", "repo_types", multiple=True, show_choices=False, required=True)
@pass_config
def list_repos(config: configparser.ConfigParser, repo_types: list[str]):
    """List matching repositories"""

    if not Path(REPO_TYPES_CFG).exists():
        click.echo(click.style(f"No {REPO_TYPES_CFG} file found.", fg="red"))
        raise SystemExit(1)

    valid_repo_types = parse_repo_types(config)
    repos = set()
    for repo_type in repo_types:
        if repo_type not in valid_repo_types:
            repo_list = "\n\t".join(valid_repo_types)
            raise click.BadParameter(f"Invalid repository type '{repo_type}'. Valid types are:\n\n\t{repo_list}")
        repos.update(valid_repo_types[repo_type])

    repos = sorted(repos)

    if len(repos) > 25:
        click.echo_via_pager("\n".join(repos))
    else:
        click.echo("\n".join(repos))
