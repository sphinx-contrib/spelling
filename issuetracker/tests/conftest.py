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

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import os

import pytest
import py.path
from mock import Mock
from lxml import etree
from pyquery import PyQuery
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import SphinxStandaloneReader

from sphinxcontrib.issuetracker import Issue, IssuesReferences


TEST_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def assert_issue_reference(doctree, issue, title=False):
    __tracebackhide__ = True
    reference = doctree.find('reference')
    assert len(reference) == 1
    assert reference.attr.refuri == issue.url
    classes = reference.attr.classes.split(' ')
    is_closed = 'issue-closed' in classes
    assert 'reference-issue' in classes
    assert issue.closed == is_closed
    if title:
        assert reference.text() == issue.title
    else:
        assert reference.text() == '#{0}'.format(issue.id)
    return reference


def get_doctree_as_xml(app, docname):
    return etree.fromstring(str(app.env.get_doctree(docname)))


def get_doctree_as_pyquery(app, docname):
    tree = get_doctree_as_xml(app, docname)
    return PyQuery(tree)


def update_confoverrides(request, **confoverrides):
    overrides_mark = request.keywords.setdefault(
        'confoverrides', pytest.mark.confoverrides())
    confoverrides.update(overrides_mark.kwargs)
    overrides_mark.kwargs = confoverrides


def pytest_namespace():
    return dict((f.__name__, f) for f in
                (get_doctree_as_xml, get_doctree_as_pyquery,
                 assert_issue_reference, update_confoverrides))


def pytest_configure(config):
    config.confpy = py.path.local(TEST_DIRECTORY).join('conf.py')


def pytest_funcarg__content(request):
    content_mark = request.keywords.get('with_content')
    if not content_mark:
        raise ValueError('no content provided')
    return content_mark.args[0]


def pytest_funcarg__srcdir(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    srcdir = tmpdir.join('src')
    srcdir.ensure(dir=True)
    confpy = request.getfuncargvalue('pytestconfig').confpy
    confpy.copy(srcdir)
    content = request.getfuncargvalue('content')
    srcdir.join('index.rst').write(content)
    return srcdir


def pytest_funcarg__outdir(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('html')


def pytest_funcarg__doctreedir(request):
    tmpdir = request.getfuncargvalue('tmpdir')
    return tmpdir.join('doctrees')


def reset_global_state():
    """
    Remove global state setup by Sphinx.

    Makes sure that we got a fresh test application for each test.
    """
    SphinxStandaloneReader.transforms.remove(IssuesReferences)
    StandaloneHTMLBuilder.css_files.remove('_static/issuetracker.css')


def pytest_funcarg__app(request):
    srcdir = request.getfuncargvalue('srcdir')
    outdir = request.getfuncargvalue('outdir')
    doctreedir = request.getfuncargvalue('doctreedir')
    confoverrides = request.keywords.get('confoverrides')
    if confoverrides:
        confoverrides = confoverrides.kwargs
    app = Sphinx(str(srcdir), str(srcdir), str(outdir), str(doctreedir),
                 'html',confoverrides=confoverrides, status=None, warning=None,
                 freshenv=True)
    request.addfinalizer(reset_global_state)
    return app


def pytest_funcarg__issue(request):
    issue_marker = request.keywords.get('with_issue')
    if issue_marker:
        return Issue(*issue_marker.args, **issue_marker.kwargs)
    return None


def pytest_funcarg__mock_resolver(request):
    issue = request.getfuncargvalue('issue')
    lookup_mock_issue = Mock(name='lookup_mock_issue', return_value=issue)
    app = request.getfuncargvalue('app')
    app.connect(b'issuetracker-resolve-issue', lookup_mock_issue)
    return lookup_mock_issue
