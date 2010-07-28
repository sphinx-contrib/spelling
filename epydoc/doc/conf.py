# -*- coding: utf-8 -*-

import sys, os

needs_sphinx = '1.0'

extensions = ['sphinx.ext.intersphinx']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-epydoc'
copyright = u'2010, Sebastian Wiesner'
version = '0.4'
release = '0.4'

exclude_patterns = ['_build']

html_theme = 'default'
html_static_path = []

intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'sphinx': ('http://sphinx.pocoo.org/', None)}


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')

