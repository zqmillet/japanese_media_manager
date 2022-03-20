import os
import sys
import subprocess

working_directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(working_directory)

author = 'kinopico'
project = 'the manual of jMM'
html_favicon = './statics/logo.png'
extensions = [
    'sphinx.ext.autodoc',
    'manual.extensions.bash',
    'sphinxcontrib.tikz',
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

autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False

tikz_latex_preamble = r'''
\usepackage{{ctex}}
\setmainfont[Path={current_directory}/manual/fonts/pingfang/, UprightFont=*_regular, BoldFont=*_bold]{{pingfang}}
\setCJKmainfont[Path={current_directory}/manual/fonts/pingfang/, UprightFont=*_regular, BoldFont=*_bold]{{pingfang}}
\setmonofont[Path={current_directory}/manual/fonts/sfmono/, UprightFont=*_regular, BoldFont=*_bold]{{sfmono}}
'''.format(current_directory=working_directory)

tikz_latex_preamble += r'''
\definecolor{crawler}{rgb}{0.5, 0.5, 0.5}
\definecolor{block}{rgb}{0.8, 0.8, 0.8}

\tikzset{
    reference/.style = {fill=reference, rectangle, line width=1pt, minimum width=0.9cm, minimum height=0.9cm, font=\tt\footnotesize},
    object/.style = {fill=object, rectangle, line width=1pt, minimum width=0.9cm, minimum height=0.9cm, font=\tt\footnotesize},
    code/.style = {font=\tt\footnotesize, anchor=west},
    plaintext/.style = {font=\footnotesize\bf, anchor=base},
    ref/.style = {line width=1pt, ->}
}
'''

tikz_tikzlibraries='positioning'

latex_engine = 'xelatex'

def setup(app):
    os.chdir(os.path.dirname(os.path.dirname(__file__)))
