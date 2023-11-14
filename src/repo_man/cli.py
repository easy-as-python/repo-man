import argparse
import configparser
import sys
from pathlib import Path
from typing import NoReturn, Union


FAIL = "\033[91m"
ENDC = "\033[0m"
REPO_TYPES_CFG = "repo-man.cfg"


def check_if_allowed(path: Path) -> Union[bool, NoReturn]:
    if REPO_TYPES_CFG not in (str(item) for item in path.iterdir()):
        print(f"{FAIL}The current directory is not configured for repository management{ENDC}")
        sys.exit(1)

    return True


def configure_arguments(parser: argparse.ArgumentParser, repo_types: dict[str, set[str]]) -> None:
    subparsers = parser.add_subparsers(description="Subcommands for managing repositories", dest="subcommand")

    # List repos
    list_parser = subparsers.add_parser("list", help="List matching repositories")

    list_parser.add_argument(
        "-t",
        "--type",
        required=True,
        choices=sorted(set(repo_types.keys()) - {"ignore", "all"}),
        metavar="TYPE",
        help="The type of repository to manage",
    )

    # Add a new repo
    add_parser = subparsers.add_parser("add", help="Add a new repository")

    add_parser.add_argument(
        "repository",
        choices=[str(directory) for directory in Path(".").iterdir() if directory.is_dir()],
        metavar="REPOSITORY",
        help="The name of the repository",
    )

    add_parser.add_argument(
        "-t",
        "--type",
        required=True,
        help="The type of the repository",
    )

    # Check a repo
    flavor_parser = subparsers.add_parser("flavors", help="List the configured types for a repository")

    flavor_parser.add_argument(
        "repository",
        choices=[str(directory) for directory in Path(".").iterdir() if directory.is_dir()],
        metavar="REPOSITORY",
        help="The name of the repository",
    )

    # Inspect repos
    parser.add_argument(
        "-k",
        "--known",
        action="store_true",
        help="List known repository types",
    )

    parser.add_argument(
        "-d",
        "--duplicates",
        action="store_true",
        help="List repositories without a configured type",
    )

    parser.add_argument(
        "-u",
        "--unconfigured",
        action="store_true",
        help="List repositories without a configured type",
    )

    parser.add_argument(
        "-m",
        "--missing",
        action="store_true",
        help="List configured repositories that aren't cloned",
    )


def parse_repo_types(config: configparser.ConfigParser) -> dict[str, set[str]]:
    config.read(REPO_TYPES_CFG)

    repo_types: dict[str, set[str]] = {"all": set()}
    for section in config.sections():
        repos = {repo for repo in config[section]["known"].split("\n") if repo}
        repo_types[section] = repos
        if section != "ignore":
            repo_types["all"].update(repos)

    return repo_types


def check_missing_repos(path: Path, repo_types: dict[str, set[str]]) -> None:
    missing = set()
    directories = {str(directory) for directory in path.iterdir()}

    for repo in sorted(repo_types["all"]):
        if repo not in directories:
            missing.add(repo)

    if missing:
        print(f"{FAIL}The following repositories are configured but do not exist:")
        for repo in missing:
            print(f"\t{repo}")
        sys.exit(1)

    return None


def handle_list(
    path: Path, config: configparser.ConfigParser, args, repo_types: dict[str, set[str]]
) -> Union[None, NoReturn]:
    if args.type not in repo_types:
        print(f"\n{FAIL}Unknown type {args.type}. Valid types are:{ENDC}")
        for repo_type in repo_types:
            if repo_type != "all" and repo_type != "ignore":
                print(f"\t{repo_type}")
        sys.exit(1)

    for repo in repo_types[args.type]:
        print(repo)

    return None


def handle_add(path: Path, config: configparser.ConfigParser, args, repo_types: dict[str, set[str]]) -> None:
    if args.type in config:
        original_config = config[args.type]["known"]
    else:
        original_config = ""
        config.add_section(args.type)

    if "known" not in config[args.type] or args.repository not in config[args.type]["known"].split("\n"):
        config.set(args.type, "known", f"{original_config}\n{args.repository}")

    with open(REPO_TYPES_CFG, "w") as config_file:
        config.write(config_file)

    return None


def handle_flavors(path: Path, config: configparser.ConfigParser, args, repo_types: dict[str, set[str]]) -> None:
    found = set()
    for section in config.sections():
        if section == "ignore":
            continue
        if args.repository in config[section]["known"].split("\n"):
            found.add(section)
    for repository in sorted(found):
        print(repository)

    return None


def handle_meta(path: Path, config: configparser.ConfigParser, args, repo_types: dict[str, set[str]]) -> None:
    if args.known:
        known_repo_types = sorted(
            [repo_type for repo_type in repo_types if repo_type != "all" and repo_type != "ignore"]
        )
        for repo_type in known_repo_types:
            print(repo_type)

    if args.unconfigured:
        for directory in sorted(path.iterdir()):
            if (
                directory.is_dir()
                and str(directory) not in repo_types["all"]
                and str(directory) not in repo_types.get("ignore", [])
            ):
                print(directory)

    if args.duplicates:
        seen = set()
        for repo_type in repo_types:
            if repo_type != "all" and repo_type != "ignore":
                for repo in repo_types[repo_type]:
                    if repo in seen:
                        print(repo)
                    seen.add(repo)


def main():
    path = Path(".")

    check_if_allowed(path)

    parser = argparse.ArgumentParser(
        prog="repo-man",
        description="Manage repositories of different types",
    )

    config = configparser.ConfigParser()
    repo_types = parse_repo_types(config)
    configure_arguments(parser, repo_types)
    args = parser.parse_args()
    check_missing_repos(path, repo_types)

    if args.subcommand == "list":
        handle_list(path, config, args, repo_types)
    elif args.subcommand == "add":
        handle_add(path, config, args, repo_types)
    elif args.subcommand == "flavors":
        handle_flavors(path, config, args, repo_types)
    else:
        handle_meta(path, config, args, repo_types)
