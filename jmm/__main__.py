import argparse

from jmm.scripts.generate_configuration import generate_configuration
from jmm.scripts.scrape import scrape
import jmm.scripts.command as COMMAND

def main() -> None:
    argument_parser = argparse.ArgumentParser(
        prog='jmm',
        description='collect, check and complete your personal adult videos'
    )

    subparsers = argument_parser.add_subparsers(dest='command')
    subparsers.add_parser(COMMAND.GENERATE_CONFIG)
    subparsers.add_parser(COMMAND.SCRAPE)

    arguments = argument_parser.parse_args()

    if arguments.command == COMMAND.GENERATE_CONFIG:
        generate_configuration()  # pragma: no cover
    elif arguments.command == COMMAND.SCRAPE:
        scrape()  # pragma: no cover
    else:
        argument_parser.print_usage()

if __name__ == '__main__':
    main()
