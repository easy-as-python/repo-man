import configparser

import click

from repo_man.utils import ensure_config_file_exists, parse_repo_types, pass_config


@click.command(name="list")
@click.option("-t", "--type", "repo_types", multiple=True, show_choices=False, required=True)
@pass_config
def list_repos(config: configparser.ConfigParser, repo_types: list[str]) -> None:
    """List matching repositories"""

    ensure_config_file_exists()

    valid_repo_types = parse_repo_types(config)
    found_repos = set()

    for repo_type in repo_types:
        if repo_type not in valid_repo_types:
            repo_list = "\n\t".join(valid_repo_types)
            raise click.BadParameter(f"Invalid repository type '{repo_type}'. Valid types are:\n\n\t{repo_list}")
        found_repos.update(valid_repo_types[repo_type])

    repos = sorted(found_repos)

    if len(repos) > 25:
        click.echo_via_pager("\n".join(repos))
    else:
        click.echo("\n".join(repos))
