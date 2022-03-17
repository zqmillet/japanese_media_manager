import os
import sys
import subprocess

working_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(working_directory)

author = 'kinopico'
project = 'the manual of jMM'
extensions = [
    'sphinx.ext.autodoc',
    'manual.extensions.bash'
]

html_theme = 'sphinx_rtd_theme'
source_suffix = ['.rst']

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': True,
    'exclude-members': 'request, __weakref__',
}
autodoc_typehints = 'both'
autodoc_class_signature = 'separated'
