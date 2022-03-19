import pytest

from jmm.utilities.configuration import CrawlerArguments
from jmm.utilities.configuration import Proxies

@pytest.mark.parametrize(
    'data, expected_dict', [
        ({}, {'interval': 0, 'timeout': 1, 'retries': 3, 'verify': False}),
        ({'timeout': 1}, {'interval': 0, 'timeout': 1, 'retries': 3, 'verify': False}),
        ({'base_url': '2333'}, {'interval': 0, 'timeout': 1, 'retries': 3, 'verify': False, 'base_url': '2333'}),
        ({'retries': 0.1}, {'interval': 0, 'timeout': 1, 'retries': 0, 'verify': False}),
        ({'proxies': {}}, {'interval': 0, 'timeout': 1, 'retries': 3, 'verify': False, 'proxies': Proxies()}),
        ({'proxies': None}, {'interval': 0, 'timeout': 1, 'retries': 3, 'verify': False}),
    ]
)
def test_crawler_arguments(data, expected_dict):
    crawler_arguments = CrawlerArguments(**data)
    assert crawler_arguments.dict() == expected_dict

@pytest.mark.parametrize(
    'data, errors', [
        (
            {'base_url': 0},
            [{'loc': ('base_url',), 'msg': 'str type expected', 'type': 'type_error.str'}]
        ),
        (
            {'retries': -1},
            [{'loc': ('retries',), 'msg': 'ensure this value is greater than or equal to 0', 'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]
        ),
        (
            {'verify': -1},
            [{'loc': ('verify',), 'msg': 'value could not be parsed to a boolean', 'type': 'type_error.bool'}]
        ),
        (
            {'proxies': {'socket': 'http://localhost'}},
            [{'loc': ('proxies', 'socket'), 'msg': 'extra fields not permitted', 'type': 'value_error.extra'}]
        ),
        (
            {'proxy': {'socket': 'http://localhost'}},
            [{'loc': ('proxy',), 'msg': 'extra fields not permitted', 'type': 'value_error.extra'}]
        ),
        (
            {'interval': -0.3},
            [{'loc': ('interval',), 'msg': 'ensure this value is greater than or equal to 0', 'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]
        ),
    ]
)
def test_crawler_arguments_with_exception(data, errors):
    with pytest.raises(Exception) as information:
        CrawlerArguments(**data)

    assert information.value.errors() == errors
