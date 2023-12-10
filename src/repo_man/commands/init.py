from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG


@click.command
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
def init(path: Path):
    """Initialize repo-man to track repositories located at the specified path"""

    if (path / REPO_TYPES_CFG).exists():
        click.confirm(
            click.style(f"{REPO_TYPES_CFG} file already exists. Overwrite with empty configuration?", fg="yellow"),
            abort=True,
        )

    with open(path / REPO_TYPES_CFG, "w"):
        pass
