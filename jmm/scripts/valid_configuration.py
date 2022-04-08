from typing import List

from .get_configuration import get_configuration
from .scrape import get_router
from .scrape import get_logger

def valid_configuration(numbers: List[str]) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    logger = get_logger(configuration)
    for number in numbers:
        metadata = router.get_metadata(number)
        if not metadata:
            logger.error('there is no routing rule matches this type of number %s', repr(number))
        logger.info('metadata of number %s is shown as following%s', number, repr(metadata))
