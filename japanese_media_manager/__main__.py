import argparse

from japanese_media_manager.scripts.generate_configuration import generate_configuration
from japanese_media_manager.scripts.scrape import scrape

class COMMAND:
    GENERATE_CONFIG = 'generate-config'
    SCRAPE = 'scrape'

argument_parser = argparse.ArgumentParser(
    prog='jmm',
    description='collect, check and complete your personal adult videos'
)

subparsers = argument_parser.add_subparsers(dest='command')
generate_config_parser = subparsers.add_parser(COMMAND.GENERATE_CONFIG)
scrape_parser = subparsers.add_parser(COMMAND.SCRAPE)

arguments = argument_parser.parse_args()

if arguments.command == COMMAND.GENERATE_CONFIG:
    generate_configuration()
elif arguments.command == COMMAND.SCRAPE:
    scrape(arguments)
else:
    argument_parser.print_usage()
