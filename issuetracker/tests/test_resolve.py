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

from functools import partial

from docutils import nodes
from sphinx.addnodes import pending_xref

from sphinxcontrib.issuetracker import resolve_issue_references


def assert_cache_ignored(app):
    cache = app.env.issuetracker_cache
    assert not cache.get.called
    assert not cache.__setitem__.called


def assert_cache_visited(app, issue_id, issue_info):
    cache = app.env.issuetracker_cache
    cache.get.assert_called_with(issue_id)
    cache.__setitem__.assert_called_with(issue_id, issue_info)


def assert_issue_reference(node, uri, is_closed):
    assert isinstance(node, nodes.reference)
    assert node['refuri'] == uri
    assert 'reference-issue' in node['classes']
    if is_closed:
        assert 'issue-closed' in node['classes']
    else:
        assert 'issue-closed' not in node['classes']


def pytest_funcarg__issue_id(request):
    return '10'


def pytest_funcarg__contnode(request):
    return nodes.Text('#{0}'.format(request.getfuncargvalue('issue_id')))


def pytest_funcarg__refnode(request):
    refnode = pending_xref()
    refnode['reftype'] = 'issue'
    refnode['reftarget'] = request.getfuncargvalue('issue_id')
    refnode.append(request.getfuncargvalue('contnode'))
    return refnode


def pytest_funcarg__doc(request):
    doc = nodes.paragraph()
    doc.append(request.getfuncargvalue('refnode'))
    return doc


def pytest_funcarg__resolve(request):
    app = request.getfuncargvalue('app')
    doc = request.getfuncargvalue('doc')
    return partial(resolve_issue_references, app, doc)


def test_resolve_unknown_reftype(app, resolve, refnode, doc):
    refnode['reftype'] = 'spam'
    resolve()
    assert isinstance(doc[0], pending_xref)
    assert_cache_ignored(app)


def test_resolve_no_issue(app, resolve, doc, contnode, issue_id):
    app.emit_firstresult.return_value = None
    resolve()
    assert doc[0] is contnode
    assert_cache_visited(app, issue_id, None)


def test_resolve_no_uri(app, resolve, doc, contnode, issue_id):
    app.emit_firstresult.return_value = {'closed': True}
    resolve()
    assert doc[0] is contnode
    assert_cache_visited(app, issue_id, {'closed': True})


def test_resolve_open_issue(app, resolve, doc, contnode, issue_id):
    app.emit_firstresult.return_value = {'uri': 'spam'}
    resolve()
    assert_issue_reference(doc[0], 'spam', False)
    assert_cache_visited(app, issue_id, {'uri': 'spam'})


def test_resolve_open_issue_with_key(app, resolve, doc, contnode, issue_id):
    app.emit_firstresult.return_value = {'uri': 'spam', 'closed': False}
    resolve()
    assert_issue_reference(doc[0], 'spam', False)
    assert_cache_visited(app, issue_id, {'uri': 'spam', 'closed': False})


def test_resolve_closed_issue(app, resolve, doc, contnode, issue_id):
    app.emit_firstresult.return_value = {'uri': 'spam', 'closed': True}
    resolve()
    assert_issue_reference(doc[0], 'spam', True)
    assert_cache_visited(app, issue_id, {'uri': 'spam', 'closed': True})


def test_event_emitted(app, resolve):
    app.emit_firstresult.return_value = {}
    resolve()
    app.emit_firstresult.assert_called_with(
        'issuetracker-resolve-issue', 'issuetracker', 'foobar', '10')

def test_event_emitted_other_project(app, resolve):
    app.emit_firstresult.return_value = {}
    app.config.issuetracker_project = 'spam with eggs'
    resolve()
    app.emit_firstresult.assert_called_with(
        'issuetracker-resolve-issue', 'spam with eggs', 'foobar', '10')
