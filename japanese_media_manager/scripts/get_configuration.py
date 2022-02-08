import os
import pathlib
import mergedeep
import yaml

from japanese_media_manager.utilities.dataclass import DataClass
from japanese_media_manager.utilities.dataclass import List
from japanese_media_manager.utilities.dataclass import Field

class RouteItem(DataClass):
    pattern = Field(type=str)
    metadatas = Field(type=list)

class Configuration(DataClass):
    route = List(RouteItem)
    proxies = Field(type=dict)
    suffixes = Field(type=list)

def get_configuration():
    default_configuration_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.config.yaml')
    custom_configuration_path = os.path.join(pathlib.Path.home(), '.jmm.cfg')

    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    if not os.path.isfile(custom_configuration_path):
        return Configuration(default_configuration)

    with open(custom_configuration_path, 'r', encoding='utf8') as file:
        custom_configuration = yaml.safe_load(file.read())

    return Configuration(mergedeep.merge(default_configuration, custom_configuration))
