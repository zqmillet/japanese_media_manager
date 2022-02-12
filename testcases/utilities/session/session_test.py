import http
import os
import signal
import multiprocessing
import contextlib
import tornado.web
import tornado.ioloop
import requests
import pytest

from japanese_media_manager.utilities.session import Session

def start_tornado(api_path, port, method, responses, queue):
    class RequestHandler(tornado.web.RequestHandler): # pylint: disable = abstract-method
        response_index = 0

    def _method(self, *args, **kwargs): # pylint: disable = unused-argument
        response = responses[RequestHandler.response_index % len(responses)]
        RequestHandler.response_index += 1
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
def mock_server_manager(api_path, responses, port=8001, method='get'):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_tornado, args=(api_path, port, method, responses, queue), daemon=True)
    process.start()
    queue.get()
    yield
    os.kill(process.pid, signal.SIGINT)
    process.join()

def test_session():
    api_path = r'/book'
    url = f'http://localhost:{8001}{api_path}'

    responses = [
        {'response': 'test_session', 'status_code': http.HTTPStatus.OK},
    ]
    with mock_server_manager(api_path=api_path, responses=responses):
        session = Session()
        response = session.get(url)
        assert response.status_code == http.HTTPStatus.OK

def test_session_with_retry():
    api_path = r'/book'
    url = f'http://localhost:{8001}{api_path}'

    responses = [
        {'response': 'test_session_with_retry', 'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR},
        {'response': 'test_session_with_retry', 'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR},
        {'response': 'test_session_with_retry', 'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR},
        {'response': 'test_session_with_retry', 'status_code': http.HTTPStatus.INTERNAL_SERVER_ERROR},
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
