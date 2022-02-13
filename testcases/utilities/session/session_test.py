import http
import os
import time
import signal
import multiprocessing
import contextlib
import logging
import tornado.web
import tornado.ioloop
import requests
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

def start_tornado(api_path, port, method, responses, wait, queue):
    logging.getLogger('tornado.access').disabled = True

    class RequestHandler(tornado.web.RequestHandler): # pylint: disable = abstract-method
        response_index = 0

    def _method(self, *args, **kwargs): # pylint: disable = unused-argument
        response = responses[RequestHandler.response_index % len(responses)]
        RequestHandler.response_index += 1
        time.sleep(wait)
        self.set_status(response.get('status_code', http.HTTPStatus.OK))
        self.finish(response['response'])

    setattr(RequestHandler, method, _method)
    RequestHandler.response_index = 0

    application = tornado.web.Application([(api_path, RequestHandler)])
    application.listen(port)

    try:
        queue.put(None)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()

@contextlib.contextmanager
def mock_server_manager(api_path, responses, port=8001, method='get', wait=0):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_tornado, args=(api_path, port, method, responses, wait, queue), daemon=True)
    process.start()
    queue.get()
    yield
    os.kill(process.pid, signal.SIGINT)
    process.join()

def test_session():
    api_path = r'/book'
    port = 8001
    url = f'http://localhost:{port}{api_path}'

    responses = [
        {'response': 'test_session', 'status_code': http.HTTPStatus.OK},
    ]
    with mock_server_manager(api_path=api_path, responses=responses):
        session = Session()
        response = session.get(url)
        assert response.status_code == http.HTTPStatus.OK

@pytest.mark.parametrize(
    'status_code', [http.HTTPStatus.INTERNAL_SERVER_ERROR, http.HTTPStatus.BAD_REQUEST, http.HTTPStatus.BAD_GATEWAY]
)
def test_session_with_retry(status_code):
    api_path = r'/book'
    port = 8001
    url = f'http://localhost:{port}{api_path}'

    responses = [
        {'response': 'test_session_with_retry', 'status_code': status_code},
        {'response': 'test_session_with_retry', 'status_code': status_code},
        {'response': 'test_session_with_retry', 'status_code': status_code},
        {'response': 'test_session_with_retry', 'status_code': status_code},
        {'response': 'test_session_with_retry', 'status_code': http.HTTPStatus.OK},
    ]
    with mock_server_manager(api_path=api_path, responses=responses):
        with pytest.raises(requests.exceptions.RetryError):
            Session().get(url)

    with mock_server_manager(api_path=api_path, responses=responses):
        Session(retries=4).get(url)

    with mock_server_manager(api_path=api_path, responses=responses):
        Session(retries=5).get(url)

    with mock_server_manager(api_path=api_path, responses=responses):
        with pytest.raises(requests.exceptions.RetryError):
            Session(retries=1).get(url)

def test_session_with_timeout():
    api_path = r'/book'
    port = 8001
    url = f'http://localhost:{port}{api_path}'

    responses = [
        {'response': 'test_session_with_timeout', 'status_code': http.HTTPStatus.OK},
    ]

    with mock_server_manager(api_path=api_path, responses=responses):
        session = Session()
        with Timer() as timer:
            session.get(url)
        assert timer.time < 0.1

    with mock_server_manager(api_path=api_path, responses=responses, wait=1):
        session = Session()
        with Timer() as timer:
            session.get(url)
        assert 1.0 < timer.time < 1.1

    with mock_server_manager(api_path=api_path, responses=responses, wait=1):
        session = Session(timeout=0.5)

        with pytest.raises(requests.exceptions.RequestException) as information:
            session.get(url)
        assert 'timeout' in str(information.value)

        session.get(url, timeout=2)

    with mock_server_manager(api_path=api_path, responses=responses, wait=1):
        session = Session(timeout=2)

        session.get(url)
        with pytest.raises(requests.exceptions.RequestException) as information:
            session.get(url, timeout=0.5)
        assert 'timeout' in str(information.value)

def test_session_with_interval():
    api_path = r'/book'
    port = 8001
    url = f'http://localhost:{port}{api_path}'

    responses = [{'response': 'test_session_with_timeout', 'status_code': http.HTTPStatus.OK}]

    with mock_server_manager(api_path=api_path, responses=responses):
        session = Session(interval=1)

        with Timer() as timer:
            session.get(url)
            session.get(url)
        assert 1 < timer.time < 1.1

    responses = [{'response': 'test_session_with_timeout', 'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR}]
    with mock_server_manager(api_path=api_path, responses=responses):
        session = Session(interval=1, retries=3)

        with Timer() as timer:
            with pytest.raises(requests.exceptions.RequestException):
                session.get(url)

        assert 3 < timer.time < 3.1

def test_session_with_proxies(proxies):
    session = Session(proxies=proxies)
    response = session.get('https://www.google.com')
    assert response.status_code == http.HTTPStatus.OK
