from re import match
from typing import List

from jmm.utilities.crawler_group import CrawlerGroup
from jmm.utilities.crawler_group import Router

from .get_configuration import get_configuration

def valid_configuration(numbers: List[str]) -> None:
    configuration = get_configuration()
    for number in numbers:
        metadata = configuration.router.get_metadata(number)
        print(metadata)
