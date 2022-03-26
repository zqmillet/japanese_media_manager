import os
import shutil
import yaml
import pytest

from jmm.scripts.scrape import scrape
from jmm.scripts.constants import custom_configuration_path

@pytest.fixture(name='destination_directory', scope='function')
def _output_directory():
    destination_directory = 'destination_directory'
    os.makedirs(destination_directory, exist_ok=True)
    yield destination_directory
    shutil.rmtree(destination_directory)

@pytest.fixture(name='write_configuration', scope='function')
def _write_configuration(proxies, directory, destination_directory):
    configuration = {
        'crawlers': [
            {
                'name': 'javbooks',
                'class': 'jmm.crawlers.JavBooksCrawler',
                'with': {'proxies': proxies.dict()}
            },
            {
                'name': 'javbus',
                'class': 'jmm.crawlers.JavBusCrawler',
                'with': {'proxies': proxies.dict()}
            },
        ],
        'routing_rules': [
            {
                'pattern': '.+',
                'crawler_names': ['javbooks', 'javbus']
            }
        ],
        'media_finder': {
            'extensions': ['.avi', '.mp4', '.mkv'],
            'recursive': True,
            'minimum_size': 0,
            'directories': [directory]
        },
        'logger': {
            'name': 'jmm'
        },
        'file_manager': {
            'destination_directory': destination_directory,
            'mode': 'infuse'
        }
    }

    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration))

@pytest.mark.usefixtures('write_configuration')
@pytest.mark.usefixtures('file_paths')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape():
    scrape()
