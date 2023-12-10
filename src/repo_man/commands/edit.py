from pathlib import Path

import click

from repo_man.consts import REPO_TYPES_CFG


@click.command
def edit():
    """Edit the repo-man configuration manually"""

    if not Path(REPO_TYPES_CFG).exists():
        click.echo(click.style(f"No {REPO_TYPES_CFG} file found.", fg="red"))
        raise SystemExit(1)

    click.edit(filename=REPO_TYPES_CFG)
