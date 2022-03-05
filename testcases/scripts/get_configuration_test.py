import yaml
import pytest

from japanese_media_manager.scripts.get_configuration import get_configuration
from japanese_media_manager.scripts.constants import custom_configuration_path
from japanese_media_manager.scripts.constants import default_configuration_path

@pytest.mark.usefixtures('protect_custom_config_file')
def test_get_default_configurations():
    with open(default_configuration_path, 'r', encoding='utf8') as file:
        assert yaml.safe_load(file.read()) == get_configuration()

@pytest.mark.usefixtures('protect_custom_config_file')
def test_get_custom_configurations():
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump({'test': 'test'}))

    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    assert default_configuration != get_configuration()
    assert get_configuration()['test'] == 'test'

    default_configuration['test'] = 'test'
    assert default_configuration == get_configuration()
