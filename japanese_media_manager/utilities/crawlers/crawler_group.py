from logging import Logger
from typing import List, Optional, Dict

from japanese_media_manager.utilities.logger import dumb
from .base import Base

class CrawlerGroup:
    def __init__(self, crawlers: List[Base], required_fields: List[str], logger: Optional[Logger] = dumb):
        self.crawlers = crawlers
        self.required_fields = required_fields
        self.logger = logger

    def get_metadata(self, number: str) -> Optional[Dict]:
        pass
