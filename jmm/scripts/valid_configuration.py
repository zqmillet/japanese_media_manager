from typing import List
from rich.progress import track

from .get_configuration import get_configuration

def valid_configuration(numbers: List[str]) -> None:
    configuration = get_configuration()
    for number in track(numbers, description='crawling...'):
        metadata = configuration.router.get_metadata(number)
        if metadata is None:
            raise Exception
        print(metadata)
