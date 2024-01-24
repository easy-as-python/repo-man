import configparser

import click

from repo_man.consts import REPO_TYPES_CFG
from repo_man.utils import parse_repo_types, pass_config, ensure_config_file_exists


@click.command(name="remove", help="Remove a repository from one or more types")
@click.option("-t", "--type", "repo_types", multiple=True, help="The types from which to remove the repository")
@click.argument("repo", type=click.Path(exists=True, file_okay=False))
@pass_config
def remove(config: configparser.ConfigParser, repo: str, repo_types: list[str]):
    """Remove a repository from some or all types"""

    ensure_config_file_exists()

    valid_repo_types = parse_repo_types(config)

    for repo_type in repo_types:
        if repo_type not in config:
            repo_list = "\n\t".join(valid_repo_types)
            raise click.BadParameter(f"Invalid repository type '{repo_type}'. Valid types are:\n\n\t{repo_list}")

        if "known" not in config[repo_type] or repo not in config[repo_type]["known"].split("\n"):
            click.confirm(f"Repository '{repo}' is not configured for type '{repo_type}'. Continue?", abort=True)

        original_config = config[repo_type]["known"]
        config.set(
            repo_type,
            "known",
            "\n".join(original_repo for original_repo in original_config.split("\n") if original_repo != repo),
        )

    with open(REPO_TYPES_CFG, "w") as config_file:
        config.write(config_file)
