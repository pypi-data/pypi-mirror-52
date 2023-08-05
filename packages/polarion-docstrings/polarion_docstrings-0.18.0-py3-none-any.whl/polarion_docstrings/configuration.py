"""
Loads configuration.
"""

import glob
import os

import yaml

from polarion_docstrings import utils

PROJECT_CONF_DIRS = ("conf", os.curdir)
PROJECT_CONF = "polarion_tools*.yaml"


def get_config(project_path=None):
    """Loads configuration from project config file."""
    config_settings = {}

    project_root = utils.find_vcs_root(project_path or os.curdir)
    if project_root is None:
        return config_settings

    for conf_dir in PROJECT_CONF_DIRS:
        conf_dir = conf_dir.lstrip("./")
        joined_dir = os.path.join(project_root, conf_dir) if conf_dir else project_root
        joined_glob = os.path.join(joined_dir, PROJECT_CONF)
        conf_files = glob.glob(joined_glob)
        if conf_files:
            break
    else:
        conf_files = []

    for conf_file in conf_files:
        try:
            with open(conf_file, encoding="utf-8") as input_file:
                loaded_settings = yaml.safe_load(input_file)
        except OSError:
            pass
        else:
            config_settings.update(loaded_settings)

    return config_settings
