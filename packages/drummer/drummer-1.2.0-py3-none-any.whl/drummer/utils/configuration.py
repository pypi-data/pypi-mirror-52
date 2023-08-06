# -*- coding: utf-8 -*-
from os import path
from drummer.utils.fio import read_yaml

class ConfigurationException(Exception):
    pass

def load_config(BASE_DIR):
    """Loads configuration and task list from yaml files."""

    config_filename = path.join(BASE_DIR, 'config/drummer-config.yml')
    tasks_filename = path.join(BASE_DIR, 'config/drummer-tasks.yml')

    try:
        config = read_yaml(config_filename)
    except:
        raise ConfigurationException('Configuration file not found')

    try:
        tasks = read_yaml(tasks_filename)
        config['tasks'] = tasks
    except:
        raise ConfigurationException('Task file not found')

    config['base_dir'] = BASE_DIR

    return config
