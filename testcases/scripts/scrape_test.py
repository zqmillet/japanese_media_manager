import os
import shutil
import yaml
import pytest

from jmm.scripts.scrape import scrape
from jmm.scripts.constants import custom_configuration_path

@pytest.fixture(name='destination_directory', scope='function')
def _output_directory():
    destination_directory = './test'
    os.makedirs(destination_directory, exist_ok=True)
    yield destination_directory
    shutil.rmtree(destination_directory)

@pytest.fixture(name='configuration', scope='function')
def _configuration(proxies, directory, destination_directory, app_id, app_key):
    return {
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
            {
                'name': 'airav',
                'class': 'jmm.crawlers.AirAvCrawler',
                'with': {'proxies': proxies.dict()}
            },

        ],
        'routing_rules': [
            {
                'pattern': '.+',
                'crawler_names': ['javbooks', 'javbus', 'airav']
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
            'file_path_pattern': destination_directory + '/{star}/{number}/{number}{subtitle}{suffix}',
            'mode': 'link'
        },
        'translator': {
            'app_id': app_id,
            'app_key': app_key
        }
    }

@pytest.fixture(name='configuration_without_translator', scope='function')
def _configuration_without_translator(configuration):
    return {**configuration, 'translator': {'app_id': None, 'app_key': None}}

@pytest.fixture(name='write_configuration', scope='function')
def _write_configuration(configuration):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration))

@pytest.fixture(name='write_configuration_without_translator', scope='function')
def _write_configuration_without_translator(configuration_without_translator):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration_without_translator))

@pytest.mark.usefixtures('write_configuration')
@pytest.mark.usefixtures('file_paths')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape():
    scrape()

@pytest.mark.usefixtures('write_configuration_without_translator')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape_without_translator(file_paths):
    for index, file_path in enumerate(file_paths):
        if index > 2:
            os.remove(file_path)

    scrape()
