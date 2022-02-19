author = 'kinopico'
project = 'the manual of jMM'
extensions = ['sphinx.ext.autodoc']

html_theme = 'sphinx_rtd_theme'
source_suffix = ['.rst']

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': True,
    'exclude-members': 'request, __weakref__'
}
