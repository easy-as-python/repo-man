import configparser

import click

from repo_man.commands.add import add
from repo_man.commands.edit import edit
from repo_man.commands.flavors import flavors
from repo_man.commands.implode import implode
from repo_man.commands.init import init
from repo_man.commands.list_repos import list_repos
from repo_man.commands.sniff import sniff
from repo_man.consts import REPO_TYPES_CFG


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_name="repo-man")
@click.pass_context
def cli(context):  # pragma: no cover
    """Manage repositories of different types"""

    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)
    context.obj = config


def main():  # pragma: no cover
    cli.add_command(add)
    cli.add_command(edit)
    cli.add_command(flavors)
    cli.add_command(implode)
    cli.add_command(init)
    cli.add_command(list_repos)
    cli.add_command(sniff)
    cli()
