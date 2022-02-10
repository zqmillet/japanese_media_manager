import urllib
import pytest

def pytest_addoption(parser):
    parser.addoption(
        '--app-id',
        action='store',
        type=str,
        help='specify the app id of baidu translation service',
        required=True
    )

    parser.addoption(
        '--app-key',
        action='store',
        type=str,
        help='specify the app key of baidu translation service',
        required=True
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
        '--session-test-url',
        action='store',
        type=str,
        help='specify a url for session testing',
        default='https://www.baidu.com',
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

@pytest.fixture(name='session_test_url', scope='session')
def _session_test_url(request):
    return request.config.getoption('session_test_url')

@pytest.fixture(name='session_test_threthold', scope='session')
def _session_test_threthold(request):
    return request.config.getoption('session_test_threthold')

@pytest.fixture(name='proxies', scope='session')
def _proxies(proxy_host, proxy_port, proxy_username, proxy_password):
    if not proxy_host or not proxy_port:
        return {
            'http': None,
            'https': None
        }

    if proxy_username and proxy_password:
        return {
            'http': f'http://{urllib.parse.quote(proxy_username)}:{urllib.parse.quote(proxy_password)}@{proxy_host}:{proxy_port}',
            'https': f'http://{urllib.parse.quote(proxy_username)}:{urllib.parse.quote(proxy_password)}@{proxy_host}:{proxy_port}',
        }

    return {
        'http': f'http://{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_host}:{proxy_port}',
    }
