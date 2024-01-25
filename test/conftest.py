import configparser
from typing import Callable

import pytest
from click.testing import CliRunner

from repo_man.consts import REPO_TYPES_CFG


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def get_config() -> Callable[[], configparser.ConfigParser]:
    def func() -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(REPO_TYPES_CFG)
        return config

    return func
