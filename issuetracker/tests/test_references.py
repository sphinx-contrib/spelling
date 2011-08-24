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

from sphinxcontrib.issuetracker import TrackerConfig, Issue


def pytest_funcarg__resolve(request):
    app = request.getfuncargvalue('app')
    resolve = Mock(name='resolve', return_value=None)
    app.connect(b'issuetracker-resolve-issue', resolve)
    return resolve


def pytest_funcarg__issue(request):
    issue = request.keywords.get('issue')
    if issue:
        return Issue(**issue.kwargs)
    return None


def pytest_funcarg__content(request):
    issue = request.getfuncargvalue('issue')
    issue_id = issue.id if issue else '10'
    return '#{0}'.format(issue_id)


def pytest_funcarg__build_app(request):
    app = request.getfuncargvalue('app')
    issue = request.getfuncargvalue('issue')
    resolve = request.getfuncargvalue('resolve')
    resolve.return_value = issue
    app.build()
    return app


def pytest_funcarg__doctree(request):
    build_app = request.getfuncargvalue('build_app')
    doctree = pytest.get_doctree_as_pyquery(build_app, 'index')
    return doctree


def test_no_issue(build_app, doctree):
    assert build_app.env.issuetracker_cache == {'10': None}
    assert not doctree.is_('reference')


@pytest.mark.issue(id='10', title='Spam', url='spam', closed=False)
def test_open_issue(build_app, doctree, issue):
    assert build_app.env.issuetracker_cache == {'10': issue}
    reference = pytest.assert_issue_reference(doctree, issue)


@pytest.mark.issue(id='10', title='Eggs', url='eggs', closed=True)
def test_closed_issue(build_app, doctree, issue):
    assert build_app.env.issuetracker_cache == {'10': issue}
    reference = pytest.assert_issue_reference(doctree, issue)


@pytest.mark.confoverrides(issuetracker_expandtitle=True)
@pytest.mark.issue(id='10', title='Eggs', url='eggs', closed=True)
def test_closed_issue_with_title(build_app, doctree, issue):
    assert build_app.env.issuetracker_cache == {'10': issue}
    reference = pytest.assert_issue_reference(doctree, issue, title=True)


def test_event_emitted(build_app, resolve):
    assert resolve.call_count == 1
    resolve.assert_called_with(
        build_app, TrackerConfig.from_sphinx_config(build_app.config), '10')
