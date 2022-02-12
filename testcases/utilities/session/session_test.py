import http
import requests
import pytest

from japanese_media_manager.utilities.session import Session
from japanese_media_manager.utilities.timer import Timer

from japanese_media_manager.utilities.mock_server import mock_server_manager

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
