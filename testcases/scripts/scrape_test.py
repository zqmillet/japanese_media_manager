import os
import shutil
import pathlib
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

@pytest.fixture(name='configuration_in_link_mode', scope='function')
def _configuration_in_link_mode(proxies, directory, destination_directory, app_id, app_key):
    return {
        'crawlers': [
            {
                'name': 'javbooks',
                'class': 'jmm.crawlers.JavBooksCrawler',
            },
            {
                'name': 'javbus',
                'class': 'jmm.crawlers.JavBusCrawler',
            },
            {
                'name': 'airav',
                'class': 'jmm.crawlers.AirAvCrawler',
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
        },
        'global_proxies': proxies.dict()
    }

@pytest.fixture(name='configuration_without_translator', scope='function')
def _configuration_without_translator(configuration_in_link_mode):
    return {**configuration_in_link_mode, 'translator': {'app_id': None, 'app_key': None}}

@pytest.fixture(name='configuration_in_copy_mode', scope='function')
def _configuration_in_copy_mode(configuration_in_link_mode, destination_directory):
    return {
        **configuration_in_link_mode,
        'file_manager': {
            'file_path_pattern': destination_directory + '/{star}/{number}/{number}{subtitle}{suffix}',
            'mode': 'copy'
        },
    }

@pytest.fixture(name='configuration_in_move_mode', scope='function')
def _configuration_in_move_mode(configuration_in_link_mode, destination_directory):
    return {
        **configuration_in_link_mode,
        'file_manager': {
            'file_path_pattern': destination_directory + '/{star}/{number}/{number}{subtitle}{suffix}',
            'mode': 'move'
        },
    }

@pytest.fixture(name='write_configuration_in_link_mode', scope='function')
def _write_configuration(configuration_in_link_mode):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration_in_link_mode))

@pytest.fixture(name='write_configuration_without_translator', scope='function')
def _write_configuration_without_translator(configuration_without_translator):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration_without_translator))

@pytest.fixture(name='write_configuration_in_copy_mode', scope='function')
def _write_configuration_in_copy_mode(configuration_in_copy_mode):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration_in_copy_mode))

@pytest.fixture(name='write_configuration_in_move_mode', scope='function')
def _write_configuration_in_move_mode(configuration_in_move_mode):
    with open(custom_configuration_path, 'w', encoding='utf8') as file:
        file.write(yaml.safe_dump(configuration_in_move_mode))

@pytest.mark.usefixtures('write_configuration_in_link_mode')
@pytest.mark.usefixtures('file_paths')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape_in_link_mode(directory):
    assert pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

    scrape()

    assert pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-fanart.jpg').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-poster.jpg').is_symlink()
    assert pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

@pytest.mark.usefixtures('write_configuration_in_copy_mode')
@pytest.mark.usefixtures('file_paths')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape_in_copy_mode(directory):
    assert pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

    scrape()

    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_symlink()
    assert pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_file()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-fanart.jpg').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-poster.jpg').is_symlink()
    assert pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

@pytest.mark.usefixtures('write_configuration_in_move_mode')
@pytest.mark.usefixtures('file_paths')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape_in_move_mode(directory):
    assert pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

    scrape()

    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_symlink()
    assert pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_file()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-fanart.jpg').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-poster.jpg').is_symlink()
    assert not pathlib.Path(os.path.join(directory, 'IPX-486_C.mp4')).is_file()

@pytest.mark.usefixtures('write_configuration_without_translator')
@pytest.mark.usefixtures('protect_custom_config_file')
def test_scrape_without_translator(file_paths):
    for index, file_path in enumerate(file_paths):
        if index > 2:
            os.remove(file_path)

    scrape()

    assert pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C.mp4').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-fanart.jpg').is_symlink()
    assert not pathlib.Path('test/桃乃木かな/IPX-486/IPX-486-C-poster.jpg').is_symlink()
