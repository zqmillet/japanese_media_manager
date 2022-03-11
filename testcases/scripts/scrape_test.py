import yaml
import pytest

from jmm.scripts.scrape import scrape
from jmm.scripts.constants import custom_configuration_path

@pytest.fixture(name='write_configuration', scope='function')
def _write_configuration(proxies):
    configuration = {
        'crawlers': [
            {
                'name': 'javbus',
                'class': 'jmm.crawlers.JavBusCrawler',
                'with': {'proxies': proxies}
            },
            {
                'name': 'javbooks',
                'class': 'jmm.crawlers.JavBooksCrawler',
                'with': {'proxies': proxies}
            }
        ],
        'routing_rules': [
            {
                'pattern': '.+',
                'crawlers': ['javbooks', 'javbus']
            }
        ]
    }

    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration))

@pytest.mark.usefixtures('write_configuration')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape():
    assert scrape(None) is None
