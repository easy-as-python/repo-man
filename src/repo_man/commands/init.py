from pathlib import Path
from typing import Annotated

import typer

from repo_man.consts import REPO_TYPES_CFG


def init(path: Annotated[Path, typer.Argument(exists=True, file_okay=False, dir_okay=True)]) -> None:
    """Initialize repo-man to track repositories located at the specified path"""

    if (path / REPO_TYPES_CFG).exists():
        typer.confirm(
            typer.style(f"{REPO_TYPES_CFG} file already exists. Overwrite with empty configuration?", fg="yellow"),
            abort=True,
        )

    with open(path / REPO_TYPES_CFG, "w"):
        pass
