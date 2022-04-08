from typing import List
from pydantic import BaseModel
from pydantic import validator
from pydantic import Field

from .crawler_configuration import CrawlerConfiguration
from .routing_rule_configuration import RoutingRuleConfiguration
from .media_finder_arguments import MediaFinderArguments
from .logger_arguments import LoggerArguments
from .file_manager_arguments import FileManagerArguments
from .translator_arguments import TranslatorArguments
from .proxies import Proxies

class Configuration(BaseModel):
    """
    jmm 的配置信息.
    """

    crawlers: List[CrawlerConfiguration] = Field(alias='crawlers')
    routing_rules: List[RoutingRuleConfiguration]
    media_finder: MediaFinderArguments
    logger: LoggerArguments
    file_manager: FileManagerArguments
    translator: TranslatorArguments
    global_proxies: Proxies

    @validator('crawlers')
    def _crawlers(cls, value: List[CrawlerConfiguration]) -> List[CrawlerConfiguration]:
        if not value:
            raise ValueError('crawlers is empty')
        return value

    @validator('routing_rules')
    def _routing_rules(cls, value: List[RoutingRuleConfiguration]) -> List[RoutingRuleConfiguration]:
        if not value:
            raise ValueError('routing_rules is empty')
        return value
