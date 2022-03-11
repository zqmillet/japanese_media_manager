import os
import logging
import pytest

from jmm.utilities.logger import Logger

def test_logger(capsys):
    logger = Logger()
    logger.debug('debug')
    logger.info('info')
    logger.warning('warn')
    logger.error('error')
    logger.critical('critical')

    output = ''.join(capsys.readouterr())

    assert 'debug' in output
    assert 'info' in output
    assert 'warn' in output
    assert 'error' in output
    assert 'critical' in output

def test_logger_with_level(capsys):
    logger = Logger(level=logging.WARNING)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warn')
    logger.error('error')
    logger.critical('critical')

    output = ''.join(capsys.readouterr())

    assert 'debug' not in output
    assert 'info' not in output
    assert 'warn' in output
    assert 'error' in output
    assert 'critical' in output

def test_dumb_logger(capsys):
    logger = Logger(level=logging.CRITICAL + 10)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warn')
    logger.error('error')
    logger.critical('critical')

    output = ''.join(capsys.readouterr())

    assert 'debug' not in output
    assert 'info' not in output
    assert 'warn' not in output
    assert 'error' not in output
    assert 'critical' not in output

@pytest.fixture(name='file_path')
def _file_path():
    file_path = 'test.log'
    if os.path.isfile(file_path):
        os.remove(file_path)

    assert not os.path.isfile(file_path)
    yield file_path

    if os.path.isfile(file_path):
        os.remove(file_path)

def test_logger_file_handler(capsys, file_path):
    logger = Logger(level=logging.WARNING, file_path=file_path)

    logger.debug('debug')
    logger.info('info')
    logger.warning('warn')
    logger.error('error')
    logger.critical('critical')

    output = ''.join(capsys.readouterr())

    assert 'debug' not in output
    assert 'info' not in output
    assert 'warn' in output
    assert 'error' in output
    assert 'critical' in output

    assert os.path.isfile(file_path)
    with open(file_path, 'r', encoding='utf8') as file:
        content = file.read()

    assert 'debug' not in content
    assert 'info' not in content
    assert 'warn' in content
    assert 'error' in content
    assert 'critical' in content
