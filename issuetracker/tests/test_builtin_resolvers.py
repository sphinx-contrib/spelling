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

import pytest

from sphinxcontrib.issuetracker import (Issue, BUILTIN_ISSUE_TRACKERS,
                                        TrackerConfig)


TRACKER_DEPENDENCIES = {
    'debian': ['debianbts'],
    'launchpad': ['launchpadlib'],
}


SPHINX = TrackerConfig('birkenfeld/sphinx')
SPHINX_URL = 'https://bitbucket.org/birkenfeld/sphinx/issue/{0}/'

DEBIAN_URL = 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug={0}'

PYTOX = TrackerConfig('pytox')
PYTOX_URL = 'http://code.google.com/p/pytox/issues/detail?id={0}'

ISSUES = {
    'bitbucket': {
        'resolved': (SPHINX, Issue(
            id='478', title='Adapt py:decorator from Python docs', closed=True,
            uri=SPHINX_URL.format('478'))),
        'invalid': (SPHINX, Issue(
            id='327', title='Spaces at the end of console messages',
            closed=True, uri=SPHINX_URL.format('327'))),
        'duplicate': (SPHINX, Issue(
            id='733', title='byte/str conversion fails on Python 3.2',
            closed=True, uri=SPHINX_URL.format('733'))),
        'no project': (TrackerConfig('lunar/foobar'), '10'),
        'no issue': (SPHINX, '10000')},
    'debian': {
        'fixed': (TrackerConfig('ldb-tools'),
                  Issue(id='584227', title='ldb-tools: missing ldb(7) manpage',
                        closed=True, uri=DEBIAN_URL.format('584227'))),
        'no project': (TrackerConfig('release.debian.org'), '1')},
    'github': {
        'closed': (TrackerConfig('lunaryorn/pyudev'),
                   Issue(id='2', title=u'python 3 support', closed=True,
                         uri='https://github.com/lunaryorn/pyudev/issues/2')),
        'no project': (TrackerConfig('lunaryorn/foobar'), '10'),
        'no issue': (TrackerConfig('lunaryorn/pyudev'), '1000')},
    'google code': {
        'fixed': (PYTOX, Issue(
            id='2', title='Hudson exists with SUCCESS status even if tox '
            'failed with ERROR', closed=True, uri=PYTOX_URL.format('2'))),
        'invalid': (PYTOX, Issue(
            id='5', title='0.7: "error: File exists"', closed=True,
            uri=PYTOX_URL.format('5'))),
        'wontfix': (PYTOX, Issue(
            id='6', title='Copy modules from site packages', closed=True,
            uri=PYTOX_URL.format('6'))),
        'no issue': (PYTOX, '1000'),
        'no project': (TrackerConfig('foobar'), '1')},
    'launchpad': {
        'closed': (TrackerConfig('inkscape'), Issue(
            '647789', title='tries to install file(s) outside of '
            './configure\'s --prefix', closed=True,
            uri='https://bugs.launchpad.net/bugs/647789'))},
}


def pytest_generate_tests(metafunc):
    if not metafunc.function == test_builtin_resolver:
        return
    for tracker, tests in ISSUES.iteritems():
        for testname in tests:
            metafunc.addcall(param=(tracker, testname),
                             id='{0},{1}'.format(tracker, testname))


def pytest_funcarg__tracker(request):
    tracker, testname = request.param
    tracker_config = ISSUES[tracker][testname][0]
    request.applymarker(pytest.mark.confoverrides(
        issuetracker=tracker, issuetracker_project=tracker_config.project,
        issuetracker_expandtitle=True))
    return tracker


def pytest_funcarg__testname(request):
    _, testname = request.param
    return testname


def pytest_funcarg__testdata(request):
    tracker = request.getfuncargvalue('tracker')
    testname = request.getfuncargvalue('testname')
    return ISSUES[tracker][testname]


def pytest_funcarg__issue_id(request):
    testdata = request.getfuncargvalue('testdata')
    _, issue = testdata
    if isinstance(issue, basestring):
        return issue
    else:
        return issue.id


def pytest_funcarg__issue(request):
    testdata = request.getfuncargvalue('testdata')
    _, issue = testdata
    if isinstance(issue, basestring):
        return None
    else:
        return issue


def pytest_funcarg__srcdir(request):
    old_srcdir = request.getfuncargvalue('pytestconfig').srcdir
    if not hasattr(request, 'param'):
        # no change, if the test isn't parametrized
        return old_srcdir
    tmpdir = request.getfuncargvalue('tmpdir')
    srcdir = tmpdir.join('src')
    srcdir.ensure(dir=True)
    old_srcdir.join('conf.py').copy(srcdir)
    index = srcdir.join('index.rst')
    tracker = request.getfuncargvalue('tracker')
    issue_id = request.getfuncargvalue('issue_id')
    index.write("""\
Tracker test
============

Issue #{0} in tracker *{1}*""".format(issue_id, tracker))
    return srcdir


def pytest_funcarg__dependencies(request):
    tracker = request.getfuncargvalue('tracker')
    return TRACKER_DEPENDENCIES.get(tracker, [])


def test_builtin_resolver(app, issue_id, issue, dependencies):
    for dependency in dependencies:
        pytest.importorskip(dependency)
    app.build()
    doctree = pytest.get_doctree_as_pyquery(app, 'index')
    assert app.env.issuetracker_cache == {issue_id: issue}
    if not issue:
        assert not doctree.is_('reference')
    else:
        pytest.assert_issue_reference(doctree, issue, title=True)


@pytest.mark.confoverrides(issuetracker='github')
def test_github_missing_slash(app):
    with pytest.raises(ValueError) as excinfo:
        app.build()


@pytest.mark.confoverrides(issuetracker='bitbucket')
def test_bitbucket_missing_slash(app):
    with pytest.raises(ValueError) as excinfo:
        app.build()
