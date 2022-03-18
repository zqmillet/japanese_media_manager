import argparse

from jmm.scripts.generate_configuration import generate_configuration
from jmm.scripts.scrape import scrape
from jmm.scripts.valid_configuration import valid_configuration
from jmm.scripts.show_version import show_version
import jmm.scripts.command as COMMAND

def main() -> None:
    argument_parser = argparse.ArgumentParser(
        prog='jmm',
        description='collect, check and complete your personal adult videos'
    )

    subparsers = argument_parser.add_subparsers(dest='command')
    subparsers.add_parser(COMMAND.GENERATE_CONFIG)
    subparsers.add_parser(COMMAND.SCRAPE)
    subparsers.add_parser(COMMAND.SHOW_VERSION)
    test_config_parser = subparsers.add_parser(COMMAND.VALID_CONFIG)
    test_config_parser.add_argument(
        '-n', '--numbers',
        type=str,
        nargs='+',
        help='specify the numbers of media for testing config'
    )

    arguments = argument_parser.parse_args()

    if arguments.command == COMMAND.GENERATE_CONFIG:
        generate_configuration()  # pragma: no cover
    elif arguments.command == COMMAND.SCRAPE:
        scrape()  # pragma: no cover
    elif arguments.command == COMMAND.VALID_CONFIG:
        valid_configuration(numbers=arguments.numbers)
    elif arguments.command == COMMAND.SHOW_VERSION:
        show_version()
    else:
        argument_parser.print_usage()

if __name__ == '__main__':
    main()
