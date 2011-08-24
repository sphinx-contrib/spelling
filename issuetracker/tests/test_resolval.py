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

from sphinxcontrib.issuetracker import TrackerConfig, Issue


def pytest_funcarg__app(request):
    """
    A *built* sphinx application with a mocked resolver.

    Overrides the global ``app`` funcarg to directly build the application.
    The application is build with a mocked resolver as returned by the
    ``mock_resolver`` funcarg.
    """
    # setup a mock resolver
    request.getfuncargvalue('mock_resolver')
    app = request.getfuncargvalue('app')
    app.build()
    return app


def pytest_funcarg__doctree(request):
    """
    The doctree of the built document as :class:`~pyquery.PyQuery` object.

    The doctree is converted into XML, parsed with lxml and then wrapped in a
    :class:`~pyquery.PyQuery` object for easy traversal and querying.
    """
    app = request.getfuncargvalue('app')
    doctree = pytest.get_doctree_as_pyquery(app, 'index')
    return doctree


@pytest.mark.with_content('#10')
def test_no_issue(app, doctree):
    """
    Test that no reference is created if an issue could not be resolved.
    """
    assert app.env.issuetracker_cache == {'10': None}
    assert not doctree.is_('reference')


@pytest.mark.with_issue(id='10', title='Spam', url='spam', closed=False)
def test_open_issue(app, doctree, issue):
    """
    Test resolval of an open issue.
    """
    assert app.env.issuetracker_cache == {'10': issue}
    pytest.assert_issue_reference(doctree, issue)


@pytest.mark.with_issue(id='10', title='Eggs', url='eggs', closed=True)
def test_closed_issue(app, doctree, issue):
    """
    Test resolval of a closed issue.
    """
    assert app.env.issuetracker_cache == {'10': issue}
    pytest.assert_issue_reference(doctree, issue)


@pytest.mark.confoverrides(issuetracker_expandtitle=True)
@pytest.mark.with_issue(id='10', title='Eggs', url='eggs', closed=True)
def test_closed_issue_with_title(app, doctree, issue):
    """
    Test resolval of an issue with title expansion enabled.
    """
    assert app.env.issuetracker_cache == {'10': issue}
    pytest.assert_issue_reference(doctree, issue, title=True)


@pytest.mark.with_content('#10')
def test_event_emitted(app, mock_resolver):
    """
    Test that issue resolval emits the event with the right arguments.
    """
    assert mock_resolver.call_count == 1
    mock_resolver.assert_called_with(
        app, TrackerConfig.from_sphinx_config(app.config), '10')


@pytest.mark.with_content('#10 #10 #11 #11')
@pytest.mark.with_issue(id='10', title='Eggs', closed=True, url='eggs')
def test_event_emitted_only_once(app, mock_resolver, issue):
    """
    Test that the resolval event is only emitted once for each issue id, and
    that subsequent lookups hit the cache.
    """
    assert mock_resolver.call_count == 2
    assert app.env.issuetracker_cache == {'10': issue, '11': None}
