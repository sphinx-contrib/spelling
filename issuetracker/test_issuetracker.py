#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import py.test
from mock import Mock
from docutils import nodes
from sphinx.addnodes import pending_xref

from sphinxcontrib import issuetracker


def pytest_funcarg__issue_info(request):
    return dict(uri='http://example.com/issues/10', closed=False)


def pytest_funcarg__get_issue_information(request):
    get_issue_information = Mock()
    info = request.getfuncargvalue('issue_info')
    get_issue_information.return_value = info
    return get_issue_information


def pytest_funcarg__resolver(request):
    return issuetracker.make_issue_reference_resolver(
        request.getfuncargvalue('get_issue_information'))


def pytest_funcarg__config(request):
    config = Mock()
    config.project = 'issuetracker'
    config.issuetracker = 'spamtracker'
    config.issuetracker_user = 'foobar'
    config.issuetracker_project = None
    config.issuetracker_issue_pattern = re.compile(r'#(\d+)')
    return config

def pytest_funcarg__app(request):
    app = Mock()
    app.config = request.getfuncargvalue('config')
    return app


def pytest_funcarg__env(request):
    env = Mock()
    env.config = request.getfuncargvalue('config')
    return env


def pytest_funcarg__node(request):
    node = pending_xref()
    node['reftype'] = 'issue'
    node['reftarget'] = '10'
    node.append(nodes.Text('#10'))
    return node


def pytest_funcarg__doc(request):
    doc = nodes.paragraph()
    doc.append(nodes.Text('foo #1 bar'))
    em = nodes.emphasis()
    em.append(nodes.Text('see #2 if you are #abc brave'))
    doc.append(em)
    doc.settings = Mock()
    doc.settings.language_code = ''
    doc.settings.env = request.getfuncargvalue('env')
    return doc


def test_get_github_issue_information(env):
    info = issuetracker.get_github_issue_information(
        'pyudev', 'lunaryorn', '2', env)
    assert info == {'closed': True,
                    'uri': 'https://github.com/lunaryorn/pyudev/issues/2'}


def test_get_bitbucket_issue_information_resolved(env):
    info = issuetracker.get_bitbucket_issue_information(
        'synaptiks', 'lunar', '22', env)
    assert info == {'closed': True,
                    'uri': 'http://bitbucket.org/lunar/synaptiks/issue/22/'}


def test_get_bitbucket_issue_information_invalid(env):
    info = issuetracker.get_bitbucket_issue_information(
        'synaptiks', 'lunar', '36', env)
    assert info == {'closed': True,
                    'uri': 'http://bitbucket.org/lunar/synaptiks/issue/36/'}


def test_get_bitbucket_issue_information_duplicate(env):
    info = issuetracker.get_bitbucket_issue_information(
        'synaptiks', 'lunar', '42', env)
    assert info == {'closed': True,
                    'uri': 'http://bitbucket.org/lunar/synaptiks/issue/42/'}


def test_get_google_code_issue_information_fixed(env):
    info = issuetracker.get_google_code_issue_information(
        'pytox', None, '2', env)
    assert info == {
        'closed': True,
        'uri': 'http://code.google.com/p/pytox/issues/detail?id=2'}


def test_get_google_code_issue_information_invalid(env):
    info = issuetracker.get_google_code_issue_information(
        'pytox', None, '5', env)
    assert info == {
        'closed': True,
        'uri': 'http://code.google.com/p/pytox/issues/detail?id=5'}


def test_get_google_code_issue_information_wontfix(env):
    info = issuetracker.get_google_code_issue_information(
        'pytox', None, '6', env)
    assert info == {
        'closed': True,
        'uri': 'http://code.google.com/p/pytox/issues/detail?id=6'}

def test_get_debian_issue_information_fixed(env):
    info = issuetracker.get_debian_issue_information(
        'ldb-tools', None, '584227', env)
    assert info == {
        'closed': True,
        'uri': 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=584227'}

def test_get_debian_issue_information_open(env):
    info = issuetracker.get_debian_issue_information(
        'xul-ext-sync', None, '600890', env)
    assert info == {
        'closed': False,
        'uri': 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=600890'}

def test_get_debian_issue_information_invalid(env):
    info = issuetracker.get_debian_issue_information(
        'release.debian.org', None, '1', env)
    assert info == None

def test_make_isssue_reference_resolver_invalid_reftype(
    app, env, resolver, node):
    node['reftype'] = 'spam'
    assert resolver(app, env, node, node[0]) is None


def test_make_issue_reference_resolver_no_issue(
    app, env, resolver, node, get_issue_information):
    get_issue_information.return_value = None
    assert resolver(app, env, node, node[0]) is None


def test_make_issue_reference_resolver_no_uri(
    app, env, resolver, node, issue_info):
    del issue_info['uri']
    assert resolver(app, env, node, node[0]) is None


def test_make_issue_reference_resolver_open_issue(
    app, env, resolver, node, issue_info):
    contnode = node[0]
    node = resolver(app, env, node, node[0])
    assert isinstance(node, nodes.reference)
    assert node[0] is contnode
    assert node['refuri'] == issue_info['uri']
    assert 'reference-issue' in node['classes']
    assert 'issue-closed' not in node['classes']


def test_make_issue_reference_resolver_closed_issue(
    app, env, resolver, node, issue_info):
    issue_info['closed'] = True
    contnode = node[0]
    node = resolver(app, env, node, node[0])
    assert isinstance(node, nodes.reference)
    assert node[0] is contnode
    assert node['refuri'] == issue_info['uri']
    assert 'reference-issue' in node['classes']
    assert 'issue-closed' in node['classes']


def test_get_issue_information_called(
    app, env, resolver, node, get_issue_information):
    resolver(app, env, node, node[0])
    get_issue_information.assert_called_with(
        'issuetracker', 'foobar', '10', app)
    app.config.issuetracker_project = 'spam with eggs'
    resolver(app, env, node, node[0])
    get_issue_information.assert_called_with(
        'spam with eggs', 'foobar', '10', app)


def test_builtin_issue_trackers():
    for tracker in ('github', 'bitbucket',
                    'launchpad', 'google code', 'debian'):
        assert tracker in issuetracker.BUILTIN_ISSUE_TRACKERS


def _assert_text(node, text):
    assert isinstance(node, nodes.Text)
    assert node.astext() == text


def _assert_xref(node, target):
    assert isinstance(node, pending_xref)
    _assert_text(node[0], '#%s' % target)
    assert node['reftype'] == 'issue'
    assert node['reftarget'] == target


def test_issues_references(doc):
    transformer = issuetracker.IssuesReferences(doc)
    transformer.apply()
    assert isinstance(doc, nodes.paragraph)
    assert doc.astext() == 'foo #1 barsee #2 if you are #abc brave'
    _assert_text(doc[0], 'foo ')
    _assert_xref(doc[1], '1')
    _assert_text(doc[2], ' bar')
    em = doc[3]
    assert isinstance(em, nodes.emphasis)
    _assert_text(em[0], 'see ')
    _assert_xref(em[1], '2')
    _assert_text(em[2], ' if you are #abc brave')


def test_issues_references_too_many_groups(doc, config):
    config.issuetracker_issue_pattern = r'(#)(\d+)'
    transformer = issuetracker.IssuesReferences(doc)
    with py.test.raises(ValueError) as exc_info:
        transformer.apply()
    error = exc_info.value
    assert str(error) == ('issuetracker_issue_pattern must have '
                          'exactly one group: %r' % ((u'#', u'1'),))


def test_auto_connect_builtin_issue_resolvers_known_tracker(app):
    app.config.issuetracker = 'bitbucket'
    issuetracker.auto_connect_builtin_issue_resolvers(app)
    assert app.connect.called


def test_auto_connect_builtin_issue_resolvers_unknown_tracker(app):
    app.config.issuetracker = 'spamtracker'
    with py.test.raises(KeyError):
        issuetracker.auto_connect_builtin_issue_resolvers(app)


def test_auto_connect_builtin_issue_resolvers_no_tracker(app):
    app.config.issuetracker = None
    issuetracker.auto_connect_builtin_issue_resolvers(app)
    assert not app.connect.called


def test_add_stylesheet(app):
    issuetracker.add_stylesheet(app)
    app.add_stylesheet.assert_called_with('issuetracker.css')


def test_setup(app):
    issuetracker.setup(app)
    app.require_sphinx.assert_called_with('1.0')
    app.add_transform.assert_called_with(issuetracker.IssuesReferences)
    app.connect.call_args_list = [
        (('builder-inited',
          issuetracker.auto_connect_builtin_issue_resolvers), {}),
        (('builder-inited', issuetracker.add_stylesheet), {}),
        (('build-finished', issuetracker.copy_stylesheet), {})]
    app.add_config_value.call_args_list = [
        (('issuetracker_issue_pattern', re.compile(r'#(\d+)'), 'env'), {}),
        (('issuetracker_user', None, 'env'), {}),
        (('issuetracker_project', None, 'env'), {}),
        (('issuetracker', None, 'env'), {})]


def main():
    import py
    py.cmdline.pytest()


if __name__ == '__main__':
    main()
