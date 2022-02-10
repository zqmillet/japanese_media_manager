import time
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session(interval, session_test_url, session_test_threthold):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < session_test_threthold

    for _ in range(4):
        with Timer() as timer:
            session.get(session_test_url)
        assert timer.time - interval < session_test_threthold

@pytest.mark.parametrize('interval', [1, 1.5, 0.5, 0])
def test_session_with_sleep(interval, session_test_url, session_test_threthold):
    session = Session(interval=interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < session_test_threthold

    time.sleep(interval)

    with Timer() as timer:
        session.get(session_test_url)
    assert timer.time < session_test_threthold
