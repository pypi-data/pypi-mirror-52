"""
Loads configuration.
"""

import glob
import logging
import os

import yaml

from . import utils

PROJECT_CONF_DIRS = ("conf", os.curdir)
PROJECT_CONF = "polarion_tools.*.yaml"
BASELINE_CONF = "polarion_tools.yaml"

# pylint: disable=invalid-name
logger = logging.getLogger(__name__)


def get_config_files(project_path=None, project_root=None):
    project_root = project_root or utils.find_vcs_root(project_path or os.curdir)
    if project_root is None:
        return []

    search_dirs = PROJECT_CONF_DIRS + (project_root,)
    baseline_file = None
    conf_files = []

    for conf_dir in search_dirs:
        if conf_files and baseline_file:
            break

        conf_dir = conf_dir.lstrip("./")
        if not conf_dir:
            continue
        joined_dir = (
            os.path.join(project_root, conf_dir) if conf_dir != project_root else project_root
        )
        conf_files = conf_files or glob.glob(os.path.join(joined_dir, PROJECT_CONF))
        baseline_file = baseline_file or glob.glob(os.path.join(joined_dir, BASELINE_CONF))

    if baseline_file:
        conf_files.insert(0, baseline_file[0])

    return conf_files


def get_config(project_path=None, config_values=None, config_files=None):
    """Loads configuration from project config file."""
    config_values = config_values or {}
    config_files = config_files or get_config_files(project_path)

    for conf_file in config_files:
        try:
            with open(conf_file, encoding="utf-8") as input_file:
                loaded_settings = yaml.safe_load(input_file)
        except OSError:
            logger.warning("Failed to load config from %s", conf_file)
        else:
            logger.info("Config loaded from %s", conf_file)
            config_values = utils.merge_dicts(config_values, loaded_settings)

    return config_values
