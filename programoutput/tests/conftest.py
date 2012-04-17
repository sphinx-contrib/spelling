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

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import pytest
from sphinx.application import Sphinx


#: conf.py for tests
CONF_PY = """\
extensions = ['sphinxcontrib.programoutput']

source_suffix = '.rst'

master_doc = 'index'

project = u'epydoc-test'
copyright = u'2011, foo'

version = '1'
release = '1'

exclude_patterns = []

pygments_style = 'sphinx'
html_theme = 'default'
"""


def pytest_funcarg__content(request):
    """
    Return the content for the current test, extracted from ``with_content``
    marker.
    """
    # prepend a title to the content to avoid a Sphinx warning emitted for
    # toctree-referenced documents without titles
    content = """\
Content
#######

{0}""".format(request.keywords['with_content'].args[0])
    return content


def pytest_funcarg__srcdir(request):
    """
    Generated source directory for test Sphinx application.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    srcdir = tmpdir.join('src')
    srcdir.ensure(dir=True)
    confpy = srcdir.join('conf.py')
    confpy.write(CONF_PY)
    index_document = srcdir.join('index.rst')
    index_document.write("""\
.. toctree::

   content/doc""")
    content_directory = srcdir.join('content')
    content_directory.ensure(dir=True)
    content_document = content_directory.join('doc.rst')
    content_document.write(request.getfuncargvalue('content'))
    return srcdir


def pytest_funcarg__outdir(request):
    """
    Output directory for current test.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('html')


def pytest_funcarg__doctreedir(request):
    """
    The doctree directory for the current.
    """
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('doctrees')


def pytest_funcarg__confoverrides(request):
    """
    Confoverrides for the current test as dict, extracted from the keyword
    arguments to the ``confoverrides`` marker.
    """
    confoverrides_marker = request.keywords.get('confoverrides')
    if confoverrides_marker:
        return confoverrides_marker.kwargs
    else:
        return {}


def pytest_funcarg__app(request):
    """
    Sphinx application for the current test.
    """
    srcdir = request.getfuncargvalue('srcdir')
    outdir = request.getfuncargvalue('outdir')
    doctreedir = request.getfuncargvalue('doctreedir')
    confoverrides = request.getfuncargvalue('confoverrides')
    warningiserror = 'ignore_warnings' not in request.keywords
    app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir), 'html',
                 status=None, warning=None, freshenv=None,
                 warningiserror=warningiserror, confoverrides=confoverrides)
    if 'build_app' in request.keywords:
        app.build()
    return app


def pytest_funcarg__doctree(request):
    request.applymarker(pytest.mark.build_app)
    app = request.getfuncargvalue('app')
    return app.env.get_doctree('content/doc')


def pytest_funcarg__cache(request):
    request.applymarker(pytest.mark.build_app)
    app = request.getfuncargvalue('app')
    return app.env.programoutput_cache
