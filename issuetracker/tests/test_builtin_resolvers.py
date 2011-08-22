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

from sphinxcontrib.issuetracker import Issue, BUILTIN_ISSUE_TRACKERS


TRACKER_DEPENDENCIES = {
    'debian': ['debianbts'],
    'launchpad': ['launchpadlib'],
}


SPHINX = 'birkenfeld/sphinx'
SPHINX_URL = 'https://bitbucket.org/{project}/issue/{{id}}/'.format(
    project=SPHINX)

DEBIAN_URL = 'http://bugs.debian.org/cgi-bin/bugreport.cgi?={id}'

PYTOX_URL = 'http://code.google.com/p/pytox/issues/detail?id={id}'

ISSUES = {
    'bitbucket': {
        'resolved': (SPHINX, Issue(id='478', closed=True,
                                   uri=SPHINX_URL.format(id='478'))),
        'invalid': (SPHINX, Issue(id='327', closed=True,
                                  uri=SPHINX_URL.format(id='327'))),
        'duplicate': (SPHINX, Issue(id='733', closed=True,
                                    uri=SPHINX_URL.format(id='733')))},
    'debian': {
        'fixed': ('ldb-tools', Issue(id='584227', closed=True,
                                     uri=DEBIAN_URL.format(id='584227'))),
        'open': ('xul-ext-sync', Issue(id='600890', closed=False,
                                       uri=DEBIAN_URL.format(id='600890')))},
    'github': {
        'closed': ('lunaryorn/pyudev',
                   Issue(id='2', closed=True,
                         uri='https://github.com/lunaryorn/pyudev/issues/2'))},
    'google code': {
        'fixed': ('pytox', Issue(id='2', closed=True,
                                 uri=PYTOX_URL.format(id='2'))),
        'invalid': ('pytox', Issue(id='5', closed=True,
                                   uri=PYTOX_URL.format(id='5'))),
        'wontfix': ('pytox', Issue(id='6', closed=True,
                                   uri=PYTOX_URL.format(id='6')))},
    'launchpad': {
        'closed': ('inkscape',
                   Issue(id='647789', closed=True,
                         uri='https://bugs.launchpad.net/bugs/647789'))},
}


MISSING_ISSUES = {
    'bitbucket': {'no slash': ('sphinx', '10'),
                  'non-existing project': ('lunar/foobar', '10'),
                  'non-existing issue': (SPHINX, '10000000')},
    'debian': {'no such project': ('release.debian.org', '1')},
    'github': {'no slash': ('pyudev', '10'),
               'non-existing project': ('lunaryorn/foobar', '10'),
               'non-existing issue': ('lunaryorn/pyudev', '1000')},
    'google code': {'non-existing issue': ('pytox', '1000'),
                    'non-existing project': ('foobar', '1')},
    'launchpad': {}
}


def pytest_generate_tests(metafunc):
    for tracker in sorted(BUILTIN_ISSUE_TRACKERS):
        resolver = BUILTIN_ISSUE_TRACKERS[tracker]
        if metafunc.function == test_resolver_missing_issue:
            issues = MISSING_ISSUES.get(tracker)
        else:
            issues = ISSUES.get(tracker)
        if not issues:
            continue
        for test_id in sorted(issues):
            project, issue = issues[test_id]
            args = dict(resolver=resolver, project=project, issue=issue,
                        dependencies=TRACKER_DEPENDENCIES.get(tracker, []))
            metafunc.addcall(funcargs=args,
                             id='{0},{1}'.format(tracker,test_id))


def test_resolver_existing_issue(app, resolver, project, issue, dependencies):
    for dependency in dependencies:
        pytest.importorskip(dependency)
    resolved_issue = resolver(app, project, issue.id)
    assert resolved_issue == issue


def test_resolver_missing_issue(app, resolver, project, issue, dependencies):
    for dependency in dependencies:
        pytest.importorskip(dependency)
    resolved_issue = resolver(app, project, issue)
    assert resolved_issue is None
