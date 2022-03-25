from typing import List
from pydantic import BaseModel
from pydantic import validator
from pydantic import Field

from jmm.utilities.crawler_group import Router
from jmm.utilities.crawler_group import Rule
from jmm.utilities.crawler_group import CrawlerGroup

from .crawler_configuration import CrawlerConfiguration
from .routing_rule_configuration import RoutingRuleConfiguration
from .media_finder_arguments import MediaFinderArguments
from .logger_arguments import LoggerArguments

class Configuration(BaseModel):
    """
    jmm 的配置信息.
    """

    crawlers: List[CrawlerConfiguration] = Field(alias='crawlers')
    routing_rules: List[RoutingRuleConfiguration]
    media_finder: MediaFinderArguments
    logger: LoggerArguments

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

    @property
    def router(self) -> Router:
        crawler_map = {}
        for crawler_configuration in self.crawlers:
            crawler_map[crawler_configuration.name] = crawler_configuration.clazz(**crawler_configuration.arguments.dict())

        rules = []
        for routing_rule in self.routing_rules:
            rules.append(
                Rule(
                    pattern=routing_rule.pattern,
                    crawler_group=CrawlerGroup(
                        crawlers=[crawler_map[crawler_name] for crawler_name in routing_rule.crawler_names]
                    )
                )
            )
        return Router(rules)
