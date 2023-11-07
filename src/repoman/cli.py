#!/usr/bin/env python

import argparse
import configparser
import sys
from pathlib import Path
from typing import NoReturn, Union


FAIL = "\033[91m"
ENDC = "\033[0m"
REPO_TYPES_CFG = "repo-types.cfg"


def check_if_allowed(path: Path) -> Union[bool, NoReturn]:
    if REPO_TYPES_CFG not in (str(item) for item in path.iterdir()):
        print(f"{FAIL}The current directory is not configured for repository management{ENDC}")
        sys.exit(1)

    return True


def configure_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List repositories of the specified type",
    )

    parser.add_argument(
        "-t",
        "--type",
        help="The type of repository to manage",
    )

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


def parse_repo_types() -> dict[str, set[str]]:
    config = configparser.ConfigParser()
    config.read(REPO_TYPES_CFG)

    repo_types: dict[str, set[str]] = {"all": set()}
    for section in config.sections():
        repos = {repo for repo in config[section]["known"].split("\n") if repo}
        repo_types[section] = repos
        if section != "ignore":
            repo_types["all"].update(repos)

    return repo_types


def check_missing_repos(path: Path, repo_types: dict[str, set[str]]) -> Union[None, NoReturn]:
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


def main():
    path = Path(".")

    check_if_allowed(path)

    parser = argparse.ArgumentParser(
        prog="./thing",
        description="Manage repositories of different types",
        epilog="Cool, man.",
    )

    configure_arguments(parser)
    args = parser.parse_args()
    repo_types = parse_repo_types()
    check_missing_repos(path, repo_types)

    if args.known:
        known_repo_types = sorted(
            [repo_type for repo_type in repo_types if repo_type != "all" and repo_type != "ignore"]
        )
        for repo_type in known_repo_types:
            print(repo_type)

    if args.type and args.type not in repo_types:
        print(f"\n{FAIL}Unknown type {args.type}. Valid types are:{ENDC}")
        for repo_type in repo_types:
            if repo_type != "all":
                print(f"\t{repo_type}")
        sys.exit(1)

    if args.unconfigured:
        for directory in sorted(path.iterdir()):
            if (
                directory.is_dir()
                and str(directory) not in repo_types["all"]
                and str(directory) not in repo_types["ignore"]
            ):
                print(directory)

    if args.list:
        for repo in repo_types[args.type]:
            print(repo)

    if args.duplicates:
        seen = set()
        for repo_type in repo_types:
            if repo_type != "all" and repo_type != "ignore":
                for repo in repo_types[repo_type]:
                    if repo in seen:
                        print(repo)
                    seen.add(repo)
