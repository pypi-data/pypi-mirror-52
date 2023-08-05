# pylint: disable=missing-docstring

import os
from polarion_tools_common import configuration, utils

EXPECTED_CONFIG = {
    "blacklisted_tests": ["\\[.*rhev", "cfme/tests/containers/", "test_.*blacklisted"],
    "whitelisted_tests": [
        "cfme/tests/infrastructure/test_quota_tagging.py::test_.*\\[.*rhe?v",
        "cfme/tests/v2v",
        "test_.*whitelisted",
        "test_tenant_quota.py",
    ],
    "docstrings": {"required_fields": ["assignee", "initialEstimate", "status"]},
}


def test_get_config(data_dir):
    config_files = configuration.get_config_files(project_root=data_dir)
    config = configuration.get_config(config_files=config_files)
    assert config == EXPECTED_CONFIG


def test_find_vcs_root(root_dir):
    abs_root_dir = os.path.abspath(root_dir)
    vcs_root = utils.find_vcs_root("./")
    assert abs_root_dir == vcs_root
