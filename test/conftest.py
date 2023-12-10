import configparser

import pytest
from click.testing import CliRunner

from repo_man.consts import REPO_TYPES_CFG


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def get_config():
    def func():
        config = configparser.ConfigParser()
        config.read(REPO_TYPES_CFG)
        return config

    return func
