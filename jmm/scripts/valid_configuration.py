from typing import List

from .get_configuration import get_configuration

def valid_configuration(numbers: List[str]) -> None:
    configuration = get_configuration()
    for number in numbers:
        metadata = configuration.router.get_metadata(number)
        if not metadata:
            raise Exception(f'there is no routing rule matches this type of number {repr(number)}')
        print(metadata)
