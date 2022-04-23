import urllib
import os
import pathlib
import shutil
import pytest

from jmm.utilities.session import Proxies

def pytest_addoption(parser):
    parser.addoption(
        '--app-id',
        action='store',
        type=str,
        help='specify the app id of baidu translation service',
        default=None
    )

    parser.addoption(
        '--app-key',
        action='store',
        type=str,
        help='specify the app key of baidu translation service',
        default=None
    )

    parser.addoption(
        '--proxy-host',
        action='store',
        type=str,
        help='specify the host of proxy',
        default=None,
    )

    parser.addoption(
        '--proxy-port',
        action='store',
        type=str,
        help='specify the port of proxy',
        default=None,
    )

    parser.addoption(
        '--proxy-username',
        action='store',
        type=str,
        help='specify the username of proxy',
        default=None,
    )

    parser.addoption(
        '--proxy-password',
        action='store',
        type=str,
        help='specify the password of proxy',
        default=None,
    )

    parser.addoption(
        '--session-test-threthold',
        action='store',
        type=float,
        help='specify a threthold for session testing',
        default=0.1,
    )

@pytest.fixture(name='app_id', scope='session')
def _app_id(request):
    return request.config.getoption('app_id')

@pytest.fixture(name='app_key', scope='session')
def _app_key(request):
    return request.config.getoption('app_key')

@pytest.fixture(name='proxy_host', scope='session')
def _proxy_host(request):
    return request.config.getoption('proxy_host')

@pytest.fixture(name='proxy_port', scope='session')
def _proxy_port(request):
    return request.config.getoption('proxy_port')

@pytest.fixture(name='proxy_username', scope='session')
def _proxy_username(request):
    return request.config.getoption('proxy_username')

@pytest.fixture(name='proxy_password', scope='session')
def _proxy_password(request):
    return request.config.getoption('proxy_password')

@pytest.fixture(name='session_test_threthold', scope='session')
def _session_test_threthold(request):
    return request.config.getoption('session_test_threthold')

@pytest.fixture(name='proxies', scope='session')
def _proxies(proxy_host, proxy_port, proxy_username, proxy_password):
    if not proxy_host or not proxy_port:
        return Proxies()

    if proxy_username and proxy_password:
        return Proxies(
            http=f'http://{urllib.parse.quote(proxy_username)}:{urllib.parse.quote(proxy_password)}@{proxy_host}:{proxy_port}',
            https=f'http://{urllib.parse.quote(proxy_username)}:{urllib.parse.quote(proxy_password)}@{proxy_host}:{proxy_port}',
        )

    return Proxies(
        http=f'http://{proxy_host}:{proxy_port}',
        https=f'http://{proxy_host}:{proxy_port}',
    )

@pytest.fixture(name='custom_config_file_path', scope='session')
def _custom_config_file_path():
    return os.path.join(pathlib.Path.home(), '.jmm.cfg')

@pytest.fixture(name='protect_custom_config_file', scope='function')
def _protect_custom_config_file(custom_config_file_path):
    if not os.path.isfile(custom_config_file_path):
        yield
        if os.path.isfile(custom_config_file_path):
            os.remove(custom_config_file_path)
    else:
        with open(custom_config_file_path, 'rb') as file:
            content = file.read()

        os.remove(custom_config_file_path)
        yield
        with open(custom_config_file_path, 'wb') as file:
            file.write(content)

@pytest.fixture(name='directory', scope='function')
def _directory():
    directory = 'for_test'

    if os.path.isdir(directory):
        shutil.rmtree(directory)

    yield directory

    if os.path.isdir(directory):
        shutil.rmtree(directory)

@pytest.fixture(name='file_paths', scope='function')
def _file_paths(directory):
    file_paths = [
        os.path.join(directory, 'star-325.mp4'),
        os.path.join(directory, '松本菜奈実', 'SSNI-306', 'ssni-306.mkv'),
        os.path.join(directory, '松本菜奈実', 'SSNI-306', 'ssni-306.jpg'),
        os.path.join(directory, '松本菜奈実', 'SSNI-306', 'ssni-306.nfo'),
        os.path.join(directory, '松本菜奈実', 'SSNI-306', 'ssni-306.srt'),
        os.path.join(directory, 'xxx', 'star-326-cd1.mp4'),
        os.path.join(directory, 'xxx', 'star-326-cd2.mp4'),
        os.path.join(directory, 'xxx', 'star-326-cd3.mp4'),
        os.path.join(directory, '松本菜奈実', 'dsb-250', 'dsb-250-cd1-c.srt'),
        os.path.join(directory, '松本菜奈実', 'dsb-250', 'dsb-250-cd1-c.mp4'),
        os.path.join(directory, '松本菜奈実', 'dsb-250', 'dsb-250-cd2-c.srt'),
        os.path.join(directory, '松本菜奈実', 'dsb-250', 'dsb-250-cd2-c.mp4'),
        os.path.join(directory, '松本菜奈実', 'dsb-250-c.mp4'),
    ]

    for file_path in file_paths:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pathlib.Path(file_path).touch()

    yield file_paths
