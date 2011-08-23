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
from mock import Mock

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
        'resolved': (SPHINX, Issue(id='478', closed=True,
                                   uri=SPHINX_URL.format('478'))),
        'invalid': (SPHINX, Issue(id='327', closed=True,
                                  uri=SPHINX_URL.format('327'))),
        'duplicate': (SPHINX, Issue(id='733', closed=True,
                                    uri=SPHINX_URL.format('733')))},
    'debian': {
        'fixed': (TrackerConfig('ldb-tools'),
                  Issue(id='584227', closed=True,
                        uri=DEBIAN_URL.format('584227')))},
    'github': {
        'closed': (TrackerConfig('lunaryorn/pyudev'),
                   Issue(id='2', closed=True,
                         uri='https://github.com/lunaryorn/pyudev/issues/2'))},
    'google code': {
        'fixed': (PYTOX, Issue(id='2', closed=True,
                               uri=PYTOX_URL.format('2'))),
        'invalid': (PYTOX, Issue(id='5', closed=True,
                                 uri=PYTOX_URL.format('5'))),
        'wontfix': (PYTOX, Issue(id='6', closed=True,
                                 uri=PYTOX_URL.format('6')))},
    'launchpad': {
        'closed': (TrackerConfig('inkscape'),
                   Issue('647789', closed=True,
                         uri='https://bugs.launchpad.net/bugs/647789'))},
}


MISSING_ISSUES = {
    'bitbucket': {'non-existing project': (TrackerConfig('lunar/foobar'), '10'),
                  'non-existing issue': (SPHINX, '10000')},
    'debian': {'no such project':
               (TrackerConfig('release.debian.org'), '1')},
    'github': {'non-existing project':
               (TrackerConfig('lunaryorn/foobar'), '10'),
               'non-existing issue':
               (TrackerConfig('lunaryorn/pyudev'), '1000')},
    'google code': {'non-existing issue': (PYTOX, '1000'),
                    'non-existing project': (TrackerConfig('foobar'), '1')},
    'launchpad': {}
}


def pytest_generate_tests(metafunc):
    if not metafunc.function.__name__.startswith('test_resolver'):
        return
    for tracker in sorted(BUILTIN_ISSUE_TRACKERS):
        resolver = BUILTIN_ISSUE_TRACKERS[tracker]
        if metafunc.function == test_resolver_missing_issue:
            issues = MISSING_ISSUES.get(tracker)
        else:
            issues = ISSUES.get(tracker)
        if not issues:
            continue
        for test_id in sorted(issues):
            trackerconfig, issue = issues[test_id]
            dependencies = TRACKER_DEPENDENCIES.get(tracker, [])
            args = dict(resolver=resolver, trackerconfig=trackerconfig,
                        issue=issue, dependencies=dependencies)
            metafunc.addcall(funcargs=args,
                             id='{0},{1}'.format(tracker,test_id))


def test_resolver_existing_issue(app, resolver, trackerconfig, issue,
                                 dependencies):
    for dependency in dependencies:
        pytest.importorskip(dependency)
    resolved_issue = resolver(app, trackerconfig, issue.id)
    assert resolved_issue == issue


def test_resolver_missing_issue(app, resolver, trackerconfig, issue,
                                dependencies):
    for dependency in dependencies:
        pytest.importorskip(dependency)
    resolved_issue = resolver(app, trackerconfig, issue)
    assert resolved_issue is None


def test_github_bitbucket_missing_slash(app):
    trackerconfig = TrackerConfig('foobar')
    with pytest.raises(ValueError) as excinfo:
        BUILTIN_ISSUE_TRACKERS['github'](app, trackerconfig, '10')
    with pytest.raises(ValueError) as excinfo:
        BUILTIN_ISSUE_TRACKERS['bitbucket'](app, trackerconfig, '10')
