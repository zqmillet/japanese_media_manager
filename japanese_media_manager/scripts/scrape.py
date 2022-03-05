import argparse

from .get_configuration import get_configuration

def scrape(arguments: argparse.Namespace) -> None:
    configuration = get_configuration()
    print(configuration)
    print(arguments)
