from pathlib import Path
from typing import Annotated

import typer

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import ensure_config_file_exists


def add(
    ctx: typer.Context,
    repo: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    repo_types: Annotated[list[str], typer.Option("-t", "--types", help="The type of the repository")],
) -> None:
    """Add a new repository"""

    config = ctx.obj
    ensure_config_file_exists(confirm=True)

    new_types = [repo_type for repo_type in repo_types if repo_type not in config]
    if new_types:
        message = "\n\t".join(new_types)
        typer.confirm(f"The following types are unknown and will be added:\n\n\t{message}\n\nContinue?", abort=True)

    for repo_type in repo_types:
        if repo_type in config:
            original_config = config[repo_type]["known"]
        else:
            original_config = ""
            config.add_section(repo_type)

        if "known" not in config[repo_type] or str(repo) not in config[repo_type]["known"].split("\n"):
            config.set(repo_type, "known", f"{original_config}\n{repo}")

    with open(REPO_TYPES_CFG, "w") as config_file:
        config.write(config_file)
