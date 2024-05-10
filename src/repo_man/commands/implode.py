from pathlib import Path
from typing import Annotated

import typer

from repo_man.consts import REPO_TYPES_CFG


def implode(path: Annotated[Path, typer.Argument(exists=True, file_okay=False, dir_okay=True)]) -> None:
    """Remove repo-man configuration for the specified directory"""

    typer.confirm(typer.style("Are you sure you want to do this?", fg="yellow"), abort=True)
    (path / REPO_TYPES_CFG).unlink(missing_ok=True)
