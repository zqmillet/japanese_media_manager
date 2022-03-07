import pydoc
import yaml
import pytest

from japanese_media_manager.scripts.get_configuration import get_configuration
from japanese_media_manager.scripts.constants import custom_configuration_path
from japanese_media_manager.scripts.constants import default_configuration_path

@pytest.mark.usefixtures('protect_custom_config_file')
def test_get_default_configurations():
    with open(default_configuration_path, 'r', encoding='utf8') as file:
        data = yaml.safe_load(file.read())

    configuation = get_configuration()

    for index, crawler in enumerate(configuation.crawlers):
        assert crawler.name == data['crawlers'][index]['name']
        assert crawler.clazz is pydoc.locate(data['crawlers'][index]['class'])

    for index, routing_rule in enumerate(configuation.routing_rules):
        assert routing_rule.crawlers == data['routing_rules'][index]['crawlers']
        assert routing_rule.pattern == data['routing_rules'][index]['pattern']

@pytest.mark.usefixtures('protect_custom_config_file')
def test_get_custom_configurations():
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(
            yaml.safe_dump(
                {
                    'routing_rules': [
                        {
                            'pattern': r'\d+',
                            'crawlers': ['javbus']
                        }
                    ]
                }
            )
        )

    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    configuation = get_configuration()
    for index, crawler in enumerate(configuation.crawlers):
        assert crawler.name == default_configuration['crawlers'][index]['name']
        assert crawler.clazz is pydoc.locate(default_configuration['crawlers'][index]['class'])

    assert configuation.routing_rules[0].pattern == r'\d+'
    assert configuation.routing_rules[0].crawlers == ['javbus']
