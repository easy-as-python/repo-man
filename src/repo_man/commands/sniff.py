import configparser
from pathlib import Path

import click

from repo_man.utils import parse_repo_types, pass_config


@click.command
@click.option("-k", "--known", is_flag=True, help="List known repository types")
@click.option("-u", "--unconfigured", is_flag=True, help="List repositories without a configured type")
@click.option("-d", "--duplicates", is_flag=True, help="List repositories with more than one configured type")
@pass_config
def sniff(config: configparser.ConfigParser, known: bool, unconfigured: bool, duplicates: bool):
    """Show information and potential issues with configuration"""

    path = Path(".")
    valid_repo_types = parse_repo_types(config)

    if known:
        known_repo_types = sorted(
            [repo_type for repo_type in valid_repo_types if repo_type != "all" and repo_type != "ignore"]
        )
        for repo_type in known_repo_types:
            click.echo(repo_type)

    if unconfigured:
        for directory in sorted(path.iterdir()):
            if (
                directory.is_dir()
                and str(directory) not in valid_repo_types["all"]
                and str(directory) not in valid_repo_types.get("ignore", [])
            ):
                click.echo(directory)

    if duplicates:
        seen_repos = set()
        duplicate_repos = set()
        for repo_type in valid_repo_types:
            if repo_type != "all" and repo_type != "ignore":
                for repo in valid_repo_types[repo_type]:
                    if repo in seen_repos:
                        duplicate_repos.add(repo)
                    seen_repos.add(repo)

        click.echo("\n".join(sorted(duplicate_repos)))
