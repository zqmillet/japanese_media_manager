import pytest

from jmm.utilities.configuration import LoggerArguments

@pytest.mark.parametrize(
    'data', [
        {},
        {'name': 'gouliguojiashengsiyi'},
        {'fmt': 'qiyinhuofubiquzhi'},
        {'level': 0, 'file_path': '/tiny_work.log'},
    ]
)
def test_logger_arguments(data):
    arguments = LoggerArguments(**data)
    assert arguments.dict() == data

@pytest.mark.parametrize(
    'data, errors', [
        (
            {'name': 233},
            [{'loc': ('name',), 'msg': 'str type expected', 'type': 'type_error.str'}]
        ),
        (
            {'level': 'gouliguojiashengsiyi'},
            [{'loc': ('level',), 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}]
        )
    ]
)
def test_logger_arguments_with_exception(data, errors):
    with pytest.raises(Exception) as information:
        LoggerArguments(**data)

    assert information.value.errors() == errors
