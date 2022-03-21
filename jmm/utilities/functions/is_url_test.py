import pytest

from jmm.utilities.functions import is_url

@pytest.mark.parametrize(
    'url, expected_output', [
        ('http://www.baidu.com', True),
        ('sock://www.baidu.com', True),
        ('https://www.baidu.com', True),
        ('https:/www.baidu.com', False),
        ('https//www.baidu.com', False),
        ('www.baidu.com', False),
        ('/www.baidu.com', False),
        ('/api/path', False),
    ]
)
def test_is_url(url, expected_output):
    assert is_url(url) == expected_output
