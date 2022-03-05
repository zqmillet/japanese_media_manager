import os
import pathlib

default_configuration_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.config.yaml')
custom_configuration_path = os.path.join(pathlib.Path.home(), '.jmm.cfg')
