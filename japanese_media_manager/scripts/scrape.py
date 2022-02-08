from .get_configuration import get_configuration

def scrape(arguments):
    configuration = get_configuration()
    print(arguments, configuration)
