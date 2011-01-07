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

from sphinxcontrib.issuetracker import make_issue_reference_resolver


def assert_cache_ignored(app):
    cache = app.env.issuetracker_cache
    assert not cache.get.called
    assert not cache.__setitem__.called


def assert_cache_visited(app, issue_id, issue_info):
    cache = app.env.issuetracker_cache
    cache.get.assert_called_with(issue_id)
    cache.__setitem__.assert_called_with(issue_id, issue_info)


def pytest_funcarg__issue_id(request):
    return '10'


def pytest_funcarg__issue_uri(request):
    id = request.getfuncargvalue('issue_id')
    return 'http://example.com/issues/{0}'.format(id)


def pytest_funcarg__issue_info(request):
    uri = request.getfuncargvalue('issue_uri')
    return dict(uri=uri, closed=False)


def pytest_funcarg__contnode(request):
    issue_id = request.getfuncargvalue('issue_id')
    return nodes.Text('#{0}'.format(issue_id))


def pytest_funcarg__node(request):
    issue_id = request.getfuncargvalue('issue_id')
    node = pending_xref()
    node['reftype'] = 'issue'
    node['reftarget'] = issue_id
    node.append(request.getfuncargvalue('contnode'))
    return node


def pytest_funcarg__resolver(request):
    return make_issue_reference_resolver(
        request.getfuncargvalue('get_issue_information'))


def pytest_funcarg__resolve(request):
    resolver = request.getfuncargvalue('resolver')
    app = request.getfuncargvalue('app')
    node = request.getfuncargvalue('node')
    return partial(resolver, app, app.env, node, node[0])


def test_make_isssue_reference_resolver_unknown_reftype(app, issue_id,
                                                        resolve, node):
    node['reftype'] = 'spam'
    assert resolve() is None
    assert_cache_ignored(app)


def test_make_issue_reference_resolver_no_issue(resolve, app, issue_id,
                                                get_issue_information):
    get_issue_information.mock.return_value = None
    assert resolve() is None
    assert_cache_visited(app, issue_id, None)


def test_make_issue_reference_resolver_no_uri(resolve, app, issue_id,
                                              issue_info):
    del issue_info['uri']
    assert resolve() is None
    assert_cache_visited(app, issue_id, issue_info)


def test_make_issue_reference_resolver_open_issue(app, resolve, contnode,
                                                  issue_id, issue_info):
    node = resolve()
    assert isinstance(node, nodes.reference)
    assert node[0] is contnode
    assert node['refuri'] == issue_info['uri']
    assert 'reference-issue' in node['classes']
    assert 'issue-closed' not in node['classes']
    assert_cache_visited(app, issue_id, issue_info)


def test_make_issue_reference_resolver_closed_issue(app, resolve, contnode,
                                                    issue_id, issue_info):
    issue_info['closed'] = True
    node = resolve()
    assert isinstance(node, nodes.reference)
    assert node[0] is contnode
    assert node['refuri'] == issue_info['uri']
    assert 'reference-issue' in node['classes']
    assert 'issue-closed' in node['classes']
    assert_cache_visited(app, issue_id, issue_info)


def test_get_issue_information_called(app, resolve, get_issue_information):
    resolve()
    get_issue_information.mock.assert_called_with(
        'issuetracker', 'foobar', '10', app)
    app.config.issuetracker_project = 'spam with eggs'
    resolve()
    get_issue_information.mock.assert_called_with(
        'spam with eggs', 'foobar', '10', app)
