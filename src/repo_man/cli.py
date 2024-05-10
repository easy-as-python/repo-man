import configparser
from typing import Annotated, Optional

import typer

from repo_man.commands.add import add
from repo_man.commands.edit import edit
from repo_man.commands.implode import implode
from repo_man.commands.init import init
from repo_man.commands.list_repos import list_repos
from repo_man.commands.remove import remove
from repo_man.commands.sniff import sniff
from repo_man.commands.types import types
from repo_man.consts import RELEASE_VERSION, REPO_TYPES_CFG


def version_callback(value: bool) -> None:
    if value:
        print(RELEASE_VERSION)
        raise typer.Exit()


cli = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@cli.callback(invoke_without_command=True)
def default(
    context: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True, help="Print the version of this tool."),
    ] = None,
) -> None:
    """Manage repositories of different types"""

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    context.obj = config


cli.command()(add)
cli.command()(edit)
cli.command()(types)
cli.command()(implode)
cli.command()(init)
cli.command(name="list")(list_repos)
cli.command()(remove)
cli.command()(sniff)


def main() -> None:  # pragma: no cover
    cli()
