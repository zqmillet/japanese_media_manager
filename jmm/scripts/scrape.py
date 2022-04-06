from typing import Optional
from typing import Dict
from typing import List
from rich.progress import track
from logging import Logger

from jmm.utilities.crawler_group import Router
from jmm.utilities.crawler_group import Rule
from jmm.utilities.crawler_group import CrawlerGroup
from jmm.utilities.file_manager import FileManager
from jmm.utilities.translator import Translator
from jmm.utilities.logger import Logger
from jmm.crawlers import Base
from jmm.utilities.configuration import Configuration
from jmm.utilities.configuration import CrawlerArguments
from jmm.utilities.functions import get_file_paths
from jmm.utilities.file_information import FileInformation

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

def get_file_informations(configuration: Configuration, input_directories: Optional[List[str]]) -> List[FileInformation]:
    arguments = configuration.media_finder.dict()
    arguments['directories'] = input_directories or arguments['directories']
    return list(map(FileInformation, get_file_paths(**arguments)))

def get_file_manager(configuration: Configuration, file_path_pattern: Optional[str], translator: Optional[Translator], logger: Logger) -> FileManager:
    file_path_pattern = file_path_pattern or configuration.file_manager.file_path_pattern
    mode = configuration.file_manager.mode
    return FileManager(mode=mode, file_path_pattern=file_path_pattern, translator=translator, logger=logger)

def get_translator(configuration: Configuration) -> Optional[Translator]:
    if configuration.translator.app_id and configuration.translator.app_key:
        return Translator(**configuration.translator.dict())
    return None

def scrape(input_directories: Optional[List[str]] = None, destination_directory: Optional[str] = None) -> None:
    configuration = get_configuration()
    router = get_router(configuration)
    logger = get_logger(configuration)
    translator = get_translator(configuration)
    file_manager = get_file_manager(configuration, destination_directory, translator, logger)
    file_informations = get_file_informations(configuration, input_directories)

    for file_information in track(file_informations):
        logger.info('processing the media %s', file_information.file_path)
        number = file_information.number

        if not number:
            logger.warning('cannot find number from file name %s', file_information.file_path)
            continue

        video = router.get_metadata(number)
        if not video:
            logger.warning('cannot find metadata of the number %s', number)
            continue

        directory = file_manager.manager(file_information, video)
        if directory:
            logger.info('media %s has been saved in %s', video.number, directory)
