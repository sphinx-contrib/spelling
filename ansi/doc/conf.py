# -*- coding: utf-8 -*-

import sys, os

needs_sphinx = '1.0'

extensions = ['sphinx.ext.intersphinx', 'sphinxcontrib.issuetracker']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-ansi'
copyright = u'2010, Sebastian Wiesner'
version = '0.5'
release = '0.5.1'

exclude_patterns = ['_build']

html_theme = 'default'
html_static_path = []

intersphinx_mapping = {'python': ('http://docs.python.org/', None)}
                       # broken in Sphinx 1.0
                       # 'sphinx': ('http://sphinx.pocoo.org/', None)}

issuetracker = 'bitbucket'
issuetracker_user = 'birkenfeld'
issuetracker_project = 'sphinx-contrib'


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
