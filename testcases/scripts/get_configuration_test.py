import pydoc
import yaml
import pytest

from jmm.scripts.get_configuration import get_configuration
from jmm.scripts.constants import custom_configuration_path
from jmm.scripts.constants import default_configuration_path

@pytest.mark.usefixtures('protect_custom_config_file')
def test_get_default_configurations():
    with open(default_configuration_path, 'r', encoding='utf8') as file:
        data = yaml.safe_load(file.read())

    configuation = get_configuration()

    for index, crawler_configuration in enumerate(configuation.crawler_configurations):
        assert crawler_configuration.name == data['crawlers'][index]['name']
        assert crawler_configuration.clazz is pydoc.locate(data['crawlers'][index]['class'])

    for index, routing_rule in enumerate(configuation.routing_rules):
        assert routing_rule.crawler_names == data['routing_rules'][index]['crawler_names']
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
                            'crawler_names': ['javbus']
                        }
                    ]
                }
            )
        )

    with open(default_configuration_path, 'r', encoding='utf8') as file:
        default_configuration = yaml.safe_load(file.read())

    configuation = get_configuration()
    for index, crawler_configuration in enumerate(configuation.crawler_configurations):
        assert crawler_configuration.name == default_configuration['crawlers'][index]['name']
        assert crawler_configuration.clazz is pydoc.locate(default_configuration['crawlers'][index]['class'])

    assert configuation.routing_rules[0].pattern == r'\d+'
    assert configuation.routing_rules[0].crawler_names == ['javbus']
