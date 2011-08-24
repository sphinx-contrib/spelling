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

from sphinxcontrib.issuetracker import Issue, TrackerConfig

try:
    import debianbts
except ImportError:
    debianbts = None

try:
    import launchpadlib
except ImportError:
    launchpadlib = None


def pytest_generate_tests(metafunc):
    if 'issue' in metafunc.funcargnames:
        for testname in sorted(metafunc.cls.issues):
            metafunc.addcall(id=testname, param=testname)


def pytest_funcarg__tracker_config(request):
    cls = request.cls
    if cls is None:
        return None
    testname = getattr(request, 'param', None)
    if testname is None:
        return cls.default_tracker_config
    else:
        return cls.tracker_config.get(testname, cls.default_tracker_config)


def pytest_funcarg__tracker(request):
    tracker_config = request.getfuncargvalue('tracker_config')
    if tracker_config is None:
        return
    tracker = request.cls.name
    confoverrides = dict(issuetracker=tracker,
                         issuetracker_project=tracker_config.project,
                         issuetracker_url=tracker_config.url,
                         issuetracker_expandtitle=True)
    confoverrides.update(request.cls.confoverrides)
    if 'confoverrides' in request.keywords:
        marker = request.keywords['confoverrides']
        confoverrides.update(marker.kwargs)
    request.applymarker(pytest.mark.confoverrides(**confoverrides))
    return tracker


def pytest_funcarg__testname(request):
    return getattr(request, 'param', None)


def pytest_funcarg__issue_id(request):
    testname = request.getfuncargvalue('testname')
    if not testname:
        return None
    issue = request.cls.issues[testname]
    if isinstance(issue, basestring):
        return issue
    else:
        return issue.id


def pytest_funcarg__issue(request):
    testname = request.getfuncargvalue('testname')
    issue = request.cls.issues[testname]
    if isinstance(issue, basestring):
        return None
    else:
        return issue


def pytest_funcarg__content(request):
    tracker = request.getfuncargvalue('tracker')
    issue_id = request.getfuncargvalue('issue_id')
    if issue_id is None:
        # return default content
        return request.getfuncargvalue('content')
    return ("""\
Tracker test
============

Issue #{0} in tracker *{1}*""".format(issue_id, tracker))


class TrackerTest(object):

    name = None

    default_tracker_config = None

    tracker_config = {}

    issues = {}

    confoverrides = {}

    def test_lookup(self, app, issue_id, issue):
        app.build()
        doctree = pytest.get_doctree_as_pyquery(app, 'index')
        assert app.env.issuetracker_cache == {issue_id: issue}
        if not issue:
            assert not doctree.is_('reference')
        else:
            pytest.assert_issue_reference(doctree, issue, title=True)


class ScopedProjectTrackerTest(TrackerTest):

    @pytest.mark.confoverrides(issuetracker_project='eggs')
    def test_project_missing_slash(self, app):
        with pytest.raises(ValueError) as excinfo:
            app.build()


class TestBitBucket(ScopedProjectTrackerTest):

    name = 'bitbucket'

    default_tracker_config = TrackerConfig('birkenfeld/sphinx')

    tracker_config = {'no project': TrackerConfig('lunar/foobar')}

    SPHINX_URL = 'https://bitbucket.org/birkenfeld/sphinx/issue/{0}/'
    issues = {
        'resolved': Issue(id='478', closed=True, url=SPHINX_URL.format('478'),
                           title='Adapt py:decorator from Python docs'),
        'invalid': Issue(id='327', closed=True, url=SPHINX_URL.format('327'),
                         title='Spaces at the end of console messages'),
        'duplicate': Issue(id='733', closed=True, url=SPHINX_URL.format('733'),
                           title='byte/str conversion fails on Python 3.2'),
        'no project': '10',
        'no issue': '10000'
    }


class TestGitHub(ScopedProjectTrackerTest):

    name = 'github'

    default_tracker_config = TrackerConfig('lunaryorn/pyudev')

    tracker_config = {'no project': TrackerConfig('lunaryorn/foobar')}

    issues = {
        'closed': Issue(id='2', title=u'python 3 support', closed=True,
                        url='https://github.com/lunaryorn/pyudev/issues/2'),
        'no project': '10',
        'no issue': '1000',
    }


class TestGoogleCode(TrackerTest):

    name = 'google code'

    default_tracker_config = TrackerConfig('pytox')

    tracker_config = {'no project': TrackerConfig('foobar')}

    PYTOX_URL = 'http://code.google.com/p/pytox/issues/detail?id={0}'
    issues = {
        'fixed': Issue(id='2', closed=True, url=PYTOX_URL.format('2'),
                       title='Hudson exists with SUCCESS status even if tox '
                       'failed with ERROR'),
        'invalid': Issue(id='5', title='0.7: "error: File exists"',
                         closed=True, url=PYTOX_URL.format('5')),
        'wontfix': Issue(id='6', title='Copy modules from site packages',
                         closed=True, url=PYTOX_URL.format('6')),
        'no issue': '1000',
        'no project': '1',
    }


class TestDebian(TrackerTest):
    pytestmark = pytest.mark.skipif(b'debianbts is None')

    name = 'debian'

    tracker_config = {'fixed': TrackerConfig('ldb-tools'),
                      'no project': TrackerConfig('release.debian.org')}

    DEBIAN_URL = 'http://bugs.debian.org/cgi-bin/bugreport.cgi?bug={0}'
    issues = {
        'fixed': Issue(id='584227', title='ldb-tools: missing ldb(7) manpage',
                       closed=True, url=DEBIAN_URL.format('584227')),
        'no project': '1',
    }


class TestLaunchpad(TrackerTest):
    pytestmark = pytest.mark.skipif(b'launchpadlib is None')

    name = 'launchpad'

    default_tracker_config = TrackerConfig('inkscape')

    issues = {
        'closed': Issue('647789', title='tries to install file(s) outside of '
                        './configure\'s --prefix', closed=True,
                        url='https://bugs.launchpad.net/bugs/647789')
    }


class TestJira(TrackerTest):

    name = 'jira'

    issues = {
        'resolved': Issue('SHERPA-15', closed=True, title='Breadcrumbs and '
                          'page title missing from admin screens',
                          url='https://studio.atlassian.com/browse/SHERPA-15'),
        'open': Issue('PYO-84', closed=False,
                      title='Implement LLSD login in pyogp',
                      url='https://jira.secondlife.com/browse/PYO-84'),
    }

    tracker_config = {
        'resolved': TrackerConfig('Sherpa', 'https://studio.atlassian.com'),
        'open': TrackerConfig('Pyogp', 'https://jira.secondlife.com'),
    }

    confoverrides = dict(issuetracker_issue_pattern=r'#([A-Z]+-\d+)')
