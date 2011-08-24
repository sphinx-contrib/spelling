# -*- coding: utf-8 -*-
# Copyright (c) 2011, Sebastian Wiesner <lunaryorn@googlemail.com>
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


import os
import sys
import re

from sphinx import addnodes

doc_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(
    os.path.join(doc_directory, os.pardir, 'sphinxcontrib')))

import issuetracker

needs_sphinx = '1.0'

extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.autodoc',
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
issuetracker_project = 'birkenfeld/sphinx-contrib'

event_sig_re = re.compile(r'([a-zA-Z-]+)\s*\((.*)\)')

def parse_event(env, sig, signode):
    m = event_sig_re.match(sig)
    if not m:
        signode += addnodes.desc_name(sig, sig)
        return sig
    name, args = m.groups()
    signode += addnodes.desc_name(name, name)
    plist = addnodes.desc_parameterlist()
    for arg in args.split(','):
        arg = arg.strip()
        plist += addnodes.desc_parameter(arg, arg)
    signode += plist
    return name


def setup(app):
    app.add_description_unit('confval', 'confval',
                             'pair: %s; configuration value')
    app.add_description_unit('event', 'event', 'pair: %s; event', parse_event)
