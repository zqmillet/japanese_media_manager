from typing import Optional
from typing import Dict
from typing import List

from jmm.utilities.crawler_group import Router
from jmm.utilities.crawler_group import Rule
from jmm.utilities.crawler_group import CrawlerGroup
from jmm.utilities.media_finder import MediaFinder
from jmm.crawlers import Base
from jmm.utilities.configuration import Configuration
from jmm.utilities.configuration import CrawlerArguments

from .get_configuration import get_configuration

def get_crawlers(configuration: Configuration) -> Dict[str, Base]:
    crawlers = {}
    for crawler_configuration in configuration.crawlers:
        arguments: CrawlerArguments = crawler_configuration.arguments
        name = crawler_configuration.name
        crawlers[name] = crawler_configuration.clazz(**arguments.dict())
    return crawlers

def get_router(configuration: Configuration) -> Router:
    crawlers = get_crawlers(configuration)
    rules = []
    for rule_configuration in configuration.routing_rules:
        rules.append(
            Rule(
                pattern=rule_configuration.pattern,
                crawler_group=CrawlerGroup([crawlers[name] for name in rule_configuration.crawler_names])
            )
        )
    return Router(rules)

def scrape(input_directories: Optional[List[str]] = None, output_directory: Optional[str] = None) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    media_finder = MediaFinder(**configuration.media_finder.dict())
    media_finder.directories = input_directories or media_finder.directories
    for file_information in media_finder:
        number = file_information.number
        if not number:
            continue
        print(router.get_metadata(number))
