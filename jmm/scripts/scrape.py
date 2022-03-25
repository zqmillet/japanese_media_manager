from typing import Optional
from typing import Dict
from typing import List

from jmm.utilities.crawler_group import Router
from jmm.utilities.crawler_group import Rule
from jmm.utilities.crawler_group import CrawlerGroup
from jmm.utilities.media_finder import MediaFinder
from jmm.utilities.logger import Logger
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
                crawler_group=CrawlerGroup(
                    [crawlers[name] for name in rule_configuration.crawler_names]
                )
            )
        )
    return Router(rules)

def get_logger(configuration: Configuration) -> Logger:
    return Logger(**configuration.logger.dict())

def get_media_finder(configuration: Configuration, input_directories: Optional[List[str]]) -> MediaFinder:
    media_finder = MediaFinder(**configuration.media_finder.dict())
    media_finder.directories = input_directories or media_finder.directories
    return media_finder

def scrape(input_directories: Optional[List[str]] = None, output_directory: Optional[str] = None) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    logger = get_logger(configuration)
    media_finder = get_media_finder(configuration, input_directories)

    for file_information in media_finder:
        number = file_information.number
        if not number:
            logger.warning('cannot find number from file name %s', file_information.file_path)
            continue
        print(router.get_metadata(number))
        print(output_directory)
