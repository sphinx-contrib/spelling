# -*- coding: utf-8 -*-

import sys, os

extensions = ['sphinx.ext.intersphinx',
              'sphinxcontrib.programoutput']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-programoutput'
copyright = u'2010, Sebastian Wiesner'
version = '0.4'
release = '0.4'

exclude_patterns = ['_build']

html_theme = 'default'
html_static_path = []

intersphinx_mapping = {
    'http://packages.python.org/sphinxcontrib-ansi': None}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
