import pytest
from pydantic import ValidationError

from jmm.utilities.configuration import Configuration
from jmm.utilities.configuration import CrawlerArguments
from jmm.crawlers import Base

def test_configuration():
    data = {
        'crawlers': [
            {
                'name': 'javbus',
                'class': 'jmm.crawlers.JavBusCrawler',
            },
            {
                'name': 'javdb',
                'class': 'jmm.crawlers.JavdbCrawler',
            }
        ],
        'routing_rules': [
            {
                'pattern': r'\d+',
                'crawler_names': ['javbus', 'javdb']
            },
            {
                'pattern': r'\w+',
                'crawler_names': ['javdb', 'javbus']
            }
        ]
    }
    configuration = Configuration(**data)
    assert configuration.crawler_configurations[0].name == 'javbus'
    assert configuration.crawler_configurations[1].name == 'javdb'
    assert issubclass(configuration.crawler_configurations[0].clazz, Base)
    assert issubclass(configuration.crawler_configurations[1].clazz, Base)

@pytest.mark.parametrize(
    'data, message', [
        (
            {
                'crawlers': [{'name': 'javbus'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            'field required'
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': '233'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            "cannot get class from '233'"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'os.path.isdir'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            "class 'os.path.isdir' must be a type"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'pathlib.Path'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            "class 'Path' must be a subclass of class jmm.crawlers.base.Base"
        ),
        (
            {
                'crawlers': None,
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            "none is not an allowed value"
        ),
        (
            {
                'crawlers': [],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus', 'javdb']}]
            },
            "crawlers is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'jmm.crawlers.JavBusCrawler'}],
                'routing_rules': [],
            },
            "routing_rules is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'jmm.crawlers.JavBusCrawler'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': []}]
            },
            "crawler_names is empty"
        ),
        (
            {
                'crawlers': [{'name': 'javbus', 'class': 'jmm.crawlers.Base'}],
                'routing_rules': [{'pattern': r'\d+', 'crawler_names': ['javbus']}]
            },
            'class cannot be jmm.crawlers.base.Base'
        )
    ]
)
def test_configuration_with_error(data, message):
    with pytest.raises(ValidationError) as information:
        Configuration(**data)
    assert information.value.errors()[0]['msg'] == message

def test_crawler_arguments():
    arguments = CrawlerArguments()
    print(arguments.dict())
