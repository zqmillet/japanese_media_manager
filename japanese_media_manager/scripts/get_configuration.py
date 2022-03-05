import os
import mergedeep
import yaml

from .constants import custom_configuration_path
from .constants import default_configuration_path

def get_configuration() -> dict:
    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    if not os.path.isfile(custom_configuration_path):
        return default_configuration

    with open(custom_configuration_path, 'r', encoding='utf8') as file:
        custom_configuration = yaml.safe_load(file.read())

    return mergedeep.merge(default_configuration, custom_configuration)
