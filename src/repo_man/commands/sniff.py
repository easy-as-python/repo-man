from pathlib import Path
from typing import Annotated, Optional

import typer

from repo_man.utils import parse_repo_types


def sniff(
    ctx: typer.Context,
    known: Annotated[Optional[bool], typer.Option("-k", "--known", help="List known repository types")] = False,
    unconfigured: Annotated[
        Optional[bool], typer.Option("-u", "--unconfigured", help="List repositories without a configured type")
    ] = False,
    duplicates: Annotated[
        Optional[bool], typer.Option("-d", "--duplicates", help="List repositories with more than one configured type")
    ] = False,
) -> None:
    """Show information and potential issues with configuration"""

    config = ctx.obj

    path = Path(".")
    valid_repo_types = parse_repo_types(config)

    if known:
        known_repo_types = sorted(
            [repo_type for repo_type in valid_repo_types if repo_type != "all" and repo_type != "ignore"]
        )
        for repo_type in known_repo_types:
            typer.echo(repo_type)

    if unconfigured:
        for directory in sorted(path.iterdir()):
            if (
                directory.is_dir()
                and str(directory) not in valid_repo_types["all"]
                and str(directory) not in valid_repo_types.get("ignore", [])
            ):
                typer.echo(directory)

    if duplicates:
        seen_repos = set()
        duplicate_repos = set()
        for repo_type in valid_repo_types:
            if repo_type != "all" and repo_type != "ignore":
                for repo in valid_repo_types[repo_type]:
                    if repo in seen_repos:
                        duplicate_repos.add(repo)
                    seen_repos.add(repo)

        typer.echo("\n".join(sorted(duplicate_repos)))
