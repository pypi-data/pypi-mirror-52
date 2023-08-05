# pylint: disable=missing-docstring

import os

import pytest

TESTS_DIR = os.path.dirname(os.path.relpath(__file__))
TESTS_DATA_DIR = os.path.join(TESTS_DIR, "data")
ROOT_DIR = os.path.join(TESTS_DIR, os.pardir)


@pytest.fixture(scope="session")
def root_dir():
    return ROOT_DIR


@pytest.fixture(scope="session")
def tests_dir():
    return TESTS_DIR


@pytest.fixture(scope="session")
def data_dir():
    return TESTS_DATA_DIR
