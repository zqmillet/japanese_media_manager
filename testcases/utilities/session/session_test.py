import time
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

url = 'https://www.baidu.com'
threthold = 0.5

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session(interval):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(url)
    assert timer.time < threthold

    for _ in range(4):
        with Timer() as timer:
            session.get(url)
        assert timer.time - interval < threthold

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session_with_sleep(interval):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(url)
    assert timer.time < threthold

    time.sleep(interval)

    with Timer() as timer:
        session.get(url)
    assert timer.time < threthold
