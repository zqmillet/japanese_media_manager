from argparse import ArgumentParser

from jmm.scripts.generate_configuration import generate_configuration
from jmm.scripts.scrape import scrape
from jmm.scripts.valid_configuration import valid_configuration
from jmm.scripts.show_version import show_version
from jmm.scripts import command as COMMAND

def main() -> None:
    argument_parser = ArgumentParser(
        prog='jmm',
        description='collect, check and complete your personal adult videos',
    )

    subparsers = argument_parser.add_subparsers(dest='command')

    generate_configuration_parser = subparsers.add_parser(
        name=COMMAND.GENERATE_CONFIG,
        help='generate custom configuration file'
    )
    test_config_parser = subparsers.add_parser(
        name=COMMAND.VALID_CONFIG,
        help='valid custom configuration'
    )
    scrape_parser = subparsers.add_parser(
        name=COMMAND.SCRAPE,
        help='scrape metadata of media and manage them'
    )
    _ = subparsers.add_parser(
        name=COMMAND.SHOW_VERSION,
        help='show jmm version'
    )

    generate_configuration_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='if specify this argument, the custom configuration file will be overwritten forcely'
    )

    scrape_parser.add_argument(
        '-i', '--input-directories',
        action='store',
        type=str,
        nargs='*',
        default=[],
        help='specify directories which contain media, if this argument is not specified, scraper will read it from config file.'
    )
    scrape_parser.add_argument(
        '-o', '--destination-directory',
        action='store',
        type=str,
        help='specify the destination directory',
        default=None
    )

    test_config_parser.add_argument(
        '-n', '--numbers',
        type=str,
        nargs='+',
        help='specify the numbers of media for testing config'
    )

    arguments = argument_parser.parse_args()

    if arguments.command == COMMAND.GENERATE_CONFIG:
        generate_configuration(force=arguments.force)  # pragma: no cover
    elif arguments.command == COMMAND.SCRAPE:
        scrape(input_directories=arguments.input_directories, destination_directory=arguments.destination_directory)  # pragma: no cover
    elif arguments.command == COMMAND.VALID_CONFIG:
        valid_configuration(numbers=arguments.numbers)  # pragma: no cover
    elif arguments.command == COMMAND.SHOW_VERSION:
        show_version()  # pragma: no cover
    else:
        argument_parser.print_usage()

if __name__ == '__main__':
    main()  # pragma: no cover
