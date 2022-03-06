from argparse import Namespace
from typing import List
from typing import Dict
from pydoc import locate

from japanese_media_manager.utilities.crawler_group import Router
from japanese_media_manager.utilities.crawler_group import Rule
from japanese_media_manager.utilities.crawler_group import CrawlerGroup
from japanese_media_manager.crawlers import Base
from .get_configuration import get_configuration

def get_crawlers(configuration: List[Dict]) -> Dict[str, Base]:
    crawlers = {}
    for crawler_configuration in configuration:
        arguments = crawler_configuration.get('with', {})
        clazz = locate(crawler_configuration['class'])
        if not isinstance(clazz, type):
            continue
        name = crawler_configuration['name']
        crawlers[name] = clazz(**arguments)
    return crawlers

def get_router(configuration: dict) -> Router:
    crawlers = get_crawlers(configuration['crawlers'])
    rules = []
    for rule_configuration in configuration['routing_rules']:
        rules.append(Rule(rule_configuration['pattern'], CrawlerGroup([crawlers[name] for name in rule_configuration['crawlers']])))
    return Router(rules)

def scrape(arguments: Namespace) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    print(arguments)
    print(router.get_metadata('star-325'))
