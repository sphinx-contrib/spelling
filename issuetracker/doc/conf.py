# -*- coding: utf-8 -*-

needs_sphinx = '1.0'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinxcontrib.issuetracker']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-issuetracker'
copyright = u'2010, Sebastian Wiesner'
version = '0.5'
release = '0.5.2'

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
