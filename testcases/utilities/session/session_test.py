import time
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session(interval):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get('https://www.baidu.com')
    assert timer.time < 0.1

    for _ in range(4):
        with Timer() as timer:
            session.get('https://www.baidu.com')
        assert timer.time - interval < 0.1

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session_with_sleep(interval):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get('https://www.baidu.com')
    assert timer.time < 0.1

    time.sleep(interval)

    with Timer() as timer:
        session.get('https://www.baidu.com')
    assert timer.time < 0.1
