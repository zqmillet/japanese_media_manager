from logging import CRITICAL

from .logger import Logger

dumb = Logger(name='dumb', level=CRITICAL + 10)
