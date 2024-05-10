from pathlib import Path
from typing import Annotated

import typer

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import ensure_config_file_exists, parse_repo_types


def remove(
    ctx: typer.Context,
    repo: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    repo_types: Annotated[
        list[str], typer.Option("-t", "--type", help="The types from which to remove the repository")
    ],
) -> None:
    """Remove a repository from some or all types"""

    config = ctx.obj

    ensure_config_file_exists()

    valid_repo_types = parse_repo_types(config)

    for repo_type in repo_types:
        if repo_type not in config:
            repo_list = "\n\t".join(valid_repo_types)
            raise typer.BadParameter(f"Invalid repository type '{repo_type}'. Valid types are:\n\n\t{repo_list}")

        if "known" not in config[repo_type] or str(repo) not in config[repo_type]["known"].split("\n"):
            typer.confirm(f"Repository '{repo}' is not configured for type '{repo_type}'. Continue?", abort=True)

        original_config = config[repo_type]["known"]
        config.set(
            repo_type,
            "known",
            "\n".join(original_repo for original_repo in original_config.split("\n") if original_repo != str(repo)),
        )

    with open(REPO_TYPES_CFG, "w") as config_file:
        config.write(config_file)
