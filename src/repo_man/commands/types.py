from pathlib import Path
from typing import Annotated

import typer

from repo_man.utils import ensure_config_file_exists


def types(ctx: typer.Context, repo: Annotated[Path, typer.Argument(exists=True, file_okay=False)]) -> None:
    """List the configured types for a repository"""

    config = ctx.obj

    ensure_config_file_exists()

    found = set()

    for section in config.sections():
        if section == "ignore":
            continue
        if str(repo) in config[section]["known"].split("\n"):
            found.add(section)

    for repository in sorted(found):
        typer.echo(repository)
