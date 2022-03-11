from argparse import Namespace
from typing import Dict

from jmm.utilities.crawler_group import Router
from jmm.utilities.crawler_group import Rule
from jmm.utilities.crawler_group import CrawlerGroup
from jmm.crawlers import Base
from jmm.utilities.configuration import Configuration

from .get_configuration import get_configuration

def get_crawlers(configuration: Configuration) -> Dict[str, Base]:
    crawlers = {}
    for crawler_configuration in configuration.crawlers:
        arguments = crawler_configuration.arguments or {}
        name = crawler_configuration.name
        crawlers[name] = crawler_configuration.clazz(**arguments)
    return crawlers

def get_router(configuration: Configuration) -> Router:
    crawlers = get_crawlers(configuration)
    rules = []
    for rule_configuration in configuration.routing_rules:
        rules.append(Rule(pattern=rule_configuration.pattern, crawler_group=CrawlerGroup([crawlers[name] for name in rule_configuration.crawlers])))
    return Router(rules)

def scrape(arguments: Namespace) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    print(arguments)
    print(router.get_metadata('star-325'))
