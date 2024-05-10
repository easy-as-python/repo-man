import typer

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import ensure_config_file_exists


def edit() -> None:
    """Edit the repo-man configuration manually"""

    ensure_config_file_exists()

    typer.edit(filename=REPO_TYPES_CFG)
