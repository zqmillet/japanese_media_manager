import pytest
from pydantic import ValidationError

from japanese_media_manager.utilities.configuration import Configuration
from japanese_media_manager.crawlers import Base

def test_configuration():
    data = {
        'crawlers': [
            {
                'name': 'javbus',
                'class': 'japanese_media_manager.crawlers.JavBusCrawler',
            },
            {
                'name': 'javdb',
                'class': 'japanese_media_manager.crawlers.JavdbCrawler',
            }
        ],
        'routing_rules': [
            {
                'pattern': r'\d+',
                'crawlers': ['javbus', 'javdb']
            },
            {
                'pattern': r'\w+',
                'crawlers': ['javdb', 'javbus']
            }
        ]
    }
    configuration = Configuration(**data)
    assert configuration.crawlers[0].name == 'javbus'
    assert configuration.crawlers[1].name == 'javdb'
    assert issubclass(configuration.crawlers[0].clazz, Base)
    assert issubclass(configuration.crawlers[1].clazz, Base)

@pytest.mark.parametrize(
    'data, message', [
        (
            {
                'crawlers': [{'name': 'javbus'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            'field required'
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': '233'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            "cannot get class from '233'"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'os.path.isdir'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            "class 'os.path.isdir' must be a type"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'pathlib.Path'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            "class 'Path' must be a subclass of class japanese_media_manager.crawlers.base.Base"
        ),
        (
            {
                'crawlers': None,
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            "none is not an allowed value"
        ),
        (
            {
                'crawlers': [],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus', 'javdb']}]
            },
            "crawlers is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'japanese_media_manager.crawlers.JavBusCrawler'}],
                'routing_rules': [],
            },
            "routing_rules is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'japanese_media_manager.crawlers.JavBusCrawler'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': []}]
            },
            "crawlers is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'japanese_media_manager.crawlers.Base'}],
                'routing_rules': [{'pattern': r'\d+', 'crawlers': ['javbus']}]
            },
            'class cannot be japanese_media_manager.crawlers.base.Base'
        )
    ]
)
def test_configuration_with_error(data, message):
    with pytest.raises(ValidationError) as information:
        Configuration(**data)
    assert information.value.errors()[0]['msg'] == message
