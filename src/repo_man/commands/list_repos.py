from typing import Annotated

import click
import typer

from repo_man.utils import ensure_config_file_exists, parse_repo_types


def list_repos(ctx: typer.Context, repo_types: Annotated[list[str], typer.Option("-t", "--type")]) -> None:
    """List matching repositories"""

    config = ctx.obj

    ensure_config_file_exists()

    valid_repo_types = parse_repo_types(config)
    found_repos = set()

    for repo_type in repo_types:
        if repo_type not in valid_repo_types:
            repo_list = "\n\t".join(valid_repo_types)
            raise typer.BadParameter(f"Invalid repository type '{repo_type}'. Valid types are:\n\n\t{repo_list}")
        found_repos.update(valid_repo_types[repo_type])

    repos = sorted(found_repos)

    if len(repos) > 25:
        click.echo_via_pager("\n".join(repos))
    else:
        typer.echo("\n".join(repos))
