import time
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

THRETHOLD = 0.1

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session(interval, session_test_url):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < THRETHOLD

    for _ in range(4):
        with Timer() as timer:
            session.get(session_test_url)
        assert timer.time - interval < THRETHOLD

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session_with_sleep(interval, session_test_url):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < THRETHOLD

    time.sleep(interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < THRETHOLD
