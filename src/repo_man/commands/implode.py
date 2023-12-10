from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG


@click.command
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def implode(path: Path):
    """Remove repo-man configuration for the specified directory"""

    click.confirm(click.style("Are you sure you want to do this?", fg="yellow"), abort=True)
    (path / REPO_TYPES_CFG).unlink(missing_ok=True)
