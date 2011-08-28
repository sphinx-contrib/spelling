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

"""
    test_builtin_resolvers
    ======================

    Test builtin issue resolvers.

    These tests are mainly intended to make sure that changes to the extension
    internals or to the public API of the issue trackers don't break resolval.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

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
    """
    Generate tests.

    Generate tests for all test functions with an ``issue`` argument by adding
    calls for each tests in testname in the ``issues`` attribute of the test
    class, the function is defined in.  The ``issues`` attribute is expected to
    be a mapping from test names to Issue objects which this test is expected
    to resolve to, or with issue ids as string, if the test is expected to be
    unable to resolve the issue.
    """
    if 'issue' in metafunc.funcargnames:
        for testname in sorted(metafunc.cls.issues):
            metafunc.addcall(id=testname, param=testname)


def pytest_funcarg__testname(request):
    """
    The testname as string, or ``None``, if no testname is known.

    This is the parameter added by the test generation hook, or ``None`` if no
    parameter was set, because test generation didn't add a call for this test.
    """
    return getattr(request, 'param', None)


def pytest_funcarg__tracker(request):
    """
    The tracker name as string, or ``None``, if no tracker is known.

    The tracker name is taken from the ``name`` attribute of the class this
    test is defined in.  If the test isn't defined in a class, ``None`` is
    returned.
    """
    if not request.cls:
        return None
    return request.cls.name


def pytest_funcarg__tracker_config(request):
    """
    The tracker configuration as ``TrackerConfig`` object, or ``None``, if
    there is no tracker configuration.

    Tracker configuration is taken from the class this test is defined in.  If
    there is a ``testname`` for this test, the tracker config is taken from the
    ``tracker_config`` map defined in the class, falling back to the
    ``default_tracker_config`` defined in the class.  If there is no
    ``testname``, the ``default_tracker_config`` is used right away.  If the
    test isn't defined in a class, ``None`` is returned.
    """
    cls = request.cls
    if cls is None:
        return None
    testname = getattr(request, 'param', None)
    if testname is None:
        return cls.default_tracker_config
    else:
        return cls.tracker_config.get(testname, cls.default_tracker_config)


def pytest_funcarg__confoverrides(request):
    """
    Confoverrides for this test as dictionary.

    Provides confoverrides for this test that include the tracker name and
    tracker configuration (as returned by the ``tracker`` and
    ``tracker_config`` funcargs).  The ``title_template`` setting is set to
    ``{issue.title}``.  The global ``confoverrides`` are included, and
    overwrite any configuration key set in this funcarg.
    """
    # configure tracker and enable title expansion to test the title retrieval
    # of builtin trackers, too
    tracker = request.getfuncargvalue('tracker')
    confoverrides = dict(issuetracker=tracker,
                         issuetracker_title_template='{issue.title}')
    tracker_config = request.getfuncargvalue('tracker_config')
    if tracker_config:
        # bring tracker configuration in
        confoverrides.update(issuetracker_project=tracker_config.project,
                             issuetracker_url=tracker_config.url)
    # bring test-class specific overrides in
    if request.cls:
        confoverrides.update(request.cls.confoverrides)
    # add overrides from the test itself
    confoverrides.update(request.getfuncargvalue('confoverrides'))
    return confoverrides


def pytest_funcarg__issue_id(request):
    """
    The issue id of this test as string, or ``None``, if this test doesn't have
    a ``testname``.

    The issue id is taken from the issue defined in the ``issues`` attribute of
    the class this test is defined in.
    """
    testname = request.getfuncargvalue('testname')
    if not testname:
        return None
    issue = request.cls.issues[testname]
    if isinstance(issue, basestring):
        return issue
    else:
        return issue.id


def pytest_funcarg__issue(request):
    """
    The issue object for this test, or ``None``, if the test is expected to be
    unable to resolve the issue.

    The issue id is taken from the issue defined in the ``issues`` attribute of
    the class this test is defined in.
    """
    testname = request.getfuncargvalue('testname')
    issue = request.cls.issues[testname]
    if isinstance(issue, basestring):
        return None
    else:
        return issue


class TrackerTest(object):
    """
    Base class for tests for builtin issue trackers.

    This class defines a single test which tests issue lookup.
    """

    #: the name of the issuetracker to use in this test
    name = None

    #: the default tracker configuration
    default_tracker_config = None

    #: test-specific tracker configuration
    tracker_config = {}

    #: issues to test. the key is a descriptive name for the issue
    #: (e.g. resolved, invalid or something the like of), the value is either a
    #: plain string, in which case the test is expected to not resolve the
    #: issue, or an ``Issue`` object, in which case the test is expected to
    #: resolve the issue id to exactly this issue object
    issues = {}

    #: confoverrides to use for tests defined in this class
    confoverrides = {}

    def test_lookup(self, cache, issue_id, issue):
        """
        Test that this tracker correctly looks up an issue.
        """
        assert cache == {issue_id: issue}


class ScopedProjectTrackerTest(TrackerTest):
    """
    Base class for tests for issue trackers which use scoped project names
    including the user name.

    Defines an additional tests which tests for exceptions raised if the
    username is missing.
    """

    @pytest.mark.with_content('#10')
    @pytest.mark.confoverrides(issuetracker_project='eggs')
    def test_project_missing_username(self, app):
        """
        Test that a project name without an username fails with a ValueError.
        """
        with pytest.raises(ValueError) as excinfo:
            app.build()
        assert str(excinfo.value) == \
            'username missing in project name: eggs'


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

    tracker_config = {'wrong project': TrackerConfig('foo'),
                      'invalid': TrackerConfig('launchpad')}

    issues = {
        'closed': Issue('647789', title='tries to install file(s) outside of '
                        './configure\'s --prefix', closed=True,
                        url='https://bugs.launchpad.net/bugs/647789'),
        'invalid': Issue('1000', closed=True,
                         title='There are too many bug reports in Malone',
                         url='https://bugs.launchpad.net/bugs/1000'),
        'wrong project': '1000',
        'no issue': '1000000',
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

    @pytest.mark.with_content('#FOO-15')
    def test_no_url(self, app):
        """
        Test that the jira tracker fails with a ValueError, if no URL was
        configured.
        """
        with pytest.raises(ValueError) as excinfo:
            app.build()
        assert str(excinfo.value) == 'URL required'
