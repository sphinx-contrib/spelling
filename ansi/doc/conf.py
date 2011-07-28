# -*- coding: utf-8 -*-
# Copyright (c) 2010, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


needs_sphinx = '1.0'

extensions = ['sphinx.ext.intersphinx', 'sphinxcontrib.issuetracker']

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinxcontrib-ansi'
copyright = u'2010, 2011 Sebastian Wiesner'
version = '0.6'
release = '0.6'

exclude_patterns = ['_build/*']

html_theme = 'default'
html_static_path = []

intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'sphinx': ('http://sphinx.pocoo.org/', None)}

issuetracker = 'bitbucket'
issuetracker_user = 'birkenfeld'
issuetracker_project = 'sphinx-contrib'


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
