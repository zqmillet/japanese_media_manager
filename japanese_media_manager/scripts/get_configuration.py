import os
import pathlib
import mergedeep
import yaml

def get_configuration() -> dict:
    default_configuration_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.config.yaml')
    custom_configuration_path = os.path.join(pathlib.Path.home(), '.jmm.cfg')

    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    if not os.path.isfile(custom_configuration_path):
        return default_configuration

    with open(custom_configuration_path, 'r', encoding='utf8') as file:
        custom_configuration = yaml.safe_load(file.read())

    return mergedeep.merge(default_configuration, custom_configuration)
