# -*- coding: utf-8 -*-

import os
import sys

doc_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(
    os.path.join(doc_directory, os.pardir)))

from sphinxcontrib import issuetracker

needs_sphinx = '1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinxcontrib.issuetracker']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-issuetracker'
copyright = u'2010, 2011, Sebastian Wiesner'
version = '.'.join(issuetracker.__version__.split('.')[:2])
release = issuetracker.__version__

exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'sphinx': ('http://sphinx.pocoo.org/', None)}

issuetracker = 'bitbucket'
issuetracker_project = 'sphinx-contrib'
issuetracker_user = 'birkenfeld'


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
