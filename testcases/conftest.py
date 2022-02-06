import pytest

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

@pytest.fixture(name='app_id', scope='session')
def _app_id(request):
    return request.config.getoption('app_id')

@pytest.fixture(name='app_key', scope='session')
def _app_key(request):
    return request.config.getoption('app_key')
